"""Adapter binding scan storage to the `ScanImages` protocol (ADR-008).

What `app/api/dependencies.py` passes to `build_providers()` when
`AI_STAGING_PROVIDER=live-vision`. The stager only ever sees the checksum and
the rendered PNG, never the storage key, filename or file headers.
"""

import gzip
import io
from pathlib import Path

import nibabel
import numpy as np
import pydicom
from PIL import Image

from app.core.database import SessionLocal
from app.repositories.scan_repository import ScanRepository
from app.storage.scan_storage import ScanStorage


def _scan_extension(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".nii.gz"):
        return ".nii.gz"
    return Path(name).suffix


def _to_uint8(pixels: np.ndarray) -> np.ndarray:
    """Window to the 1st-99th percentile and scale to 8-bit greyscale."""

    pixels = np.asarray(pixels, dtype=np.float64)
    # NaN-aware: one NaN voxel would make np.percentile NaN and the whole
    # slice render black (audit HB-21).
    if np.isnan(pixels).all():
        return np.zeros(pixels.shape, dtype=np.uint8)
    low, high = np.nanpercentile(pixels, (1, 99))
    if not high > low:
        return np.zeros(pixels.shape, dtype=np.uint8)
    scaled = np.clip((np.nan_to_num(pixels, nan=low) - low) / (high - low), 0, 1)
    return (scaled * 255).astype(np.uint8)


# Clinical MRI slices are at most ~1024x1024. The cap stops a header that
# lies about its size from making us read gigabytes for one slice.
_MAX_SLICE_PIXELS = 2048 * 2048


def _nifti_slice(content: bytes, extension: str) -> np.ndarray:
    # Stream, never inflate the whole upload: a small .nii.gz can expand
    # ~1000x. Slicing the proxy reads only the bytes of the slice we keep.
    stream = io.BytesIO(content)
    if extension == ".nii.gz":
        stream = gzip.GzipFile(fileobj=stream)
    holder = nibabel.FileHolder(fileobj=stream)
    image = nibabel.Nifti1Image.from_file_map({"header": holder, "image": holder})

    shape = image.shape
    if len(shape) >= 2 and shape[0] * shape[1] > _MAX_SLICE_PIXELS:
        raise ValueError(f"scan slice is too large to render: {shape[:2]}")

    # The middle axial slice of the first time/channel volume.
    index = (slice(None), slice(None), *((shape[2] // 2,) if len(shape) > 2 else ()))
    index += (0,) * (len(shape) - len(index))
    pixels = np.asanyarray(image.dataobj[index])
    return np.rot90(pixels) if len(shape) > 2 else pixels


def _dicom_slice(content: bytes) -> np.ndarray:
    # Pixel data only: the dataset's headers carry PHI and are never read
    # further or forwarded.
    pixels = pydicom.dcmread(io.BytesIO(content)).pixel_array
    while pixels.ndim > 2:
        pixels = pixels[pixels.shape[0] // 2]
    return pixels


def read_dimensions(content: bytes, filename: str) -> dict[str, int]:
    """Parse the file's header for its geometry; raise if it isn't that format.

    Headers only: DICOM stops before pixel data and PHI is not kept.
    """

    extension = _scan_extension(filename)
    if extension in {".nii", ".nii.gz"}:
        # Stream the header only: a small .nii.gz can inflate ~1000x, so
        # never decompress the whole upload just to read its shape.
        stream = io.BytesIO(content)
        if extension == ".nii.gz":
            stream = gzip.GzipFile(fileobj=stream)
        shape = nibabel.Nifti1Header.from_fileobj(stream).get_data_shape()
        width, height, slices = (tuple(shape[:3]) + (1, 1))[:3]
    elif extension == ".dcm":
        header = pydicom.dcmread(io.BytesIO(content), stop_before_pixels=True)
        width, height = header.Columns, header.Rows
        slices = header.get("NumberOfFrames", 1)
    else:
        (width, height), slices = Image.open(io.BytesIO(content)).size, 1
    return {"width": int(width), "height": int(height), "slices": int(slices)}


def render_png(content: bytes, filename: str) -> bytes:
    """Render a scan file to one greyscale PNG slice."""

    extension = _scan_extension(filename)
    if extension in {".nii", ".nii.gz"}:
        image = Image.fromarray(_to_uint8(_nifti_slice(content, extension)))
    elif extension == ".dcm":
        image = Image.fromarray(_to_uint8(_dicom_slice(content)))
    else:
        # PNG/JPEG: re-encoding drops EXIF and any other metadata chunks.
        image = Image.open(io.BytesIO(content)).convert("L")

    # A single-value slice carries no anatomy. Staging it would store
    # whatever the model guesses for a blank image, so refuse it; the
    # orchestrator reports a staging_error and nothing is stored.
    low, high = image.getextrema()
    if low == high:
        raise ValueError("scan slice is blank; nothing to stage")

    out = io.BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()


class StorageScanImages:
    """Opens one short-lived session per lookup, like `SessionCorpusSearch`."""

    def __init__(self, storage: ScanStorage, repository: ScanRepository | None = None):
        self._storage = storage
        self._repository = repository or ScanRepository()

    def preview_png(self, checksum: str) -> bytes | None:
        with SessionLocal() as db:
            scan = self._repository.get_by_checksum(db, checksum)
            if scan is None:
                return None
            storage_key, filename = scan.storage_key, scan.original_filename

        return render_png(self._storage.load(storage_key), filename)


__all__ = ["StorageScanImages", "read_dimensions", "render_png"]
