"""Storage for MRI scan bytes, outside the database (ADR-006 decision 5).

A PDF can be regenerated from its snapshot (ADR-004); a scan cannot, so the
bytes are source data rather than a derived artifact. ``ScanService`` persists
only the reference this module hands back, never the bytes themselves.
"""

from pathlib import Path
from typing import Protocol, runtime_checkable
from uuid import UUID, uuid4


@runtime_checkable
class ScanStorage(Protocol):
    """Where a scan's bytes live, addressed by an opaque storage key."""

    def save(self, visit_id: UUID, filename: str, content: bytes) -> str:
        """Persist ``content`` and return its storage key."""
        ...

    def delete(self, storage_key: str) -> None:
        """Remove previously saved content. Missing content is not an error."""
        ...


class LocalScanStorage:
    """Filesystem-backed storage under a configured base directory.

    The concrete backend for V1 ("a storage backend becomes a deployment
    dependency" -- ADR-006 consequences). Swapping to an object store later
    means a new class behind this same protocol, not a change to
    ``ScanService`` or anything upstream of it.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)

    def save(self, visit_id: UUID, filename: str, content: bytes) -> str:
        directory = self.base_dir / str(visit_id)
        directory.mkdir(parents=True, exist_ok=True)

        # Path(filename).name strips any directory component -- filename is
        # untrusted client input, and without this a name like "../../x"
        # would write outside base_dir. The uuid4() prefix also means two
        # uploads for the same visit can never collide.
        safe_name = Path(filename).name or "scan"
        key = f"{visit_id}/{uuid4()}-{safe_name}"
        (self.base_dir / key).write_bytes(content)
        return key

    def delete(self, storage_key: str) -> None:
        (self.base_dir / storage_key).unlink(missing_ok=True)


__all__ = ["LocalScanStorage", "ScanStorage"]
