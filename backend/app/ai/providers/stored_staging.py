"""Serve a scan's stored stage before asking the stager again (ADR-008).

The orchestrator re-stages every prior scan on each analysis. Without a
durable store, a live vision model is paid N times per run, and a prior
visit's stage can drift between runs or after a restart. Wraps any
`ImagingStager`; the store itself lives outside `app/ai/`
(`app/services/staging_store.py`), like `ScanImages`.
"""

from app.ai.providers.base import ImagingStager, StagingStore
from app.schemas.imaging import StagingRequest, StagingResult


class StoredImagingStager:
    """An `ImagingStager` that stages each (checksum, model) once."""

    def __init__(self, inner: ImagingStager, store: StagingStore):
        self.name = inner.name
        self.provenance = inner.provenance
        self._inner = inner
        self._store = store

    def stage(self, request: StagingRequest) -> StagingResult:
        stored = self._store.get(request.checksum, self.name)
        if stored is not None:
            return stored

        result = self._inner.stage(request)
        self._store.put(request.checksum, result)
        return result


__all__ = ["StoredImagingStager"]
