"""Adapter binding scan storage to the `ScanImages` protocol (ADR-008).

What `app/api/dependencies.py` passes to `build_providers()` when
`AI_STAGING_PROVIDER=live-vision`. The stager only ever sees the checksum and
the rendered PNG, never the storage key, filename or file headers.
"""

import gzip
import io

import nibabel
import numpy as np
import pydicom
from PIL import Image

from app.core.database import SessionLocal
from app.repositories.scan_repository import ScanRepository
from app.services.scan_service import _scan_extension
from app.storage.scan_storage import ScanStorage


def _to_uint8(pixels: np.ndarray) -> np.ndarray:
    """Window to the 1st-99th percentile and scale to 8-bit greyscale."""

    pixels = np.asarray(pixels, dtype=np.float64)
    low, high = np.percentile(pixels, (1, 99))
    if high <= low:
        return np.zeros(pixels.shape, dtype=np.uint8)
    return (np.clip((pixels - low) / (high - low), 0, 1) * 255).astype(np.uint8)


def _nifti_slice(content: bytes, extension: str) -> np.ndarray:
    if extension == ".nii.gz":
        content = gzip.decompress(content)
    volume = np.asanyarray(nibabel.Nifti1Image.from_bytes(content).dataobj)
    # Drop any time/channel axes, then take the middle axial slice.
    while volume.ndim > 3:
        volume = volume[..., 0]
    if volume.ndim == 3:
        volume = np.rot90(volume[:, :, volume.shape[2] // 2])
    return volume


def _dicom_slice(content: bytes) -> np.ndarray:
    # Pixel data only: the dataset's headers carry PHI and are never read
    # further or forwarded.
    pixels = pydicom.dcmread(io.BytesIO(content)).pixel_array
    while pixels.ndim > 2:
        pixels = pixels[pixels.shape[0] // 2]
    return pixels


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


__all__ = ["StorageScanImages", "render_png"]
