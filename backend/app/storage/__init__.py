"""Storage backends for artifacts that do not belong in the database."""

from .scan_storage import LocalScanStorage, ScanStorage

__all__ = ["LocalScanStorage", "ScanStorage"]
