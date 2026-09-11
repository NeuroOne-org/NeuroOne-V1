"""Deterministic stand-in for an MRI staging model (ADR-006).

The stage estimate is a pure function of the scan's own checksum: the same
scan always stages the same way, and two different scans stage differently,
which is the determinism property AGENTS.md section 8.1 requires of a mock
provider.

SIMULATED: no image is actually read. A live staging model would replace this
class behind ``ImagingStager``, unchanged everywhere else in the pipeline.
"""

import hashlib

from app.schemas.analysis import MAX_CONFIDENCE
from app.schemas.imaging import RegionContribution, StageLabel, StagingRequest, StagingResult


STAGES: tuple[StageLabel, ...] = ("CN", "MCI", "Mild", "Moderate", "Severe")

# Imaging is the primary signal now (ADR-006 decision 1), so a staged
# estimate never reads as a weak guess -- but it still stays clear of the
# certainty ceiling.
MIN_STAGING_CONFIDENCE = 0.55

REGIONS: tuple[str, ...] = (
    "Hippocampus",
    "Entorhinal cortex",
    "Lateral ventricles",
    "Temporal lobe cortex",
    "Parietal lobe cortex",
)


class MockImagingStager:
    """Deterministic stage estimate derived from the scan's checksum."""

    name = "mock-imaging-stager-v1"
    provenance = "simulated"

    def stage(self, request: StagingRequest) -> StagingResult:
        """Derive a stage, confidence and region breakdown from the checksum."""

        digest = hashlib.sha256(request.checksum.encode("utf-8")).digest()

        stage = STAGES[digest[0] % len(STAGES)]

        span = MAX_CONFIDENCE - MIN_STAGING_CONFIDENCE
        confidence = round(MIN_STAGING_CONFIDENCE + span * (digest[1] / 255), 4)

        weights = [byte / 255 for byte in digest[2 : 2 + len(REGIONS)]]
        total = sum(weights) or 1.0
        contributions = sorted(
            (
                RegionContribution(region=region, contribution=round(weight / total, 4))
                for region, weight in zip(REGIONS, weights)
            ),
            key=lambda contribution: -contribution.contribution,
        )[:3]

        return StagingResult(
            model_name=self.name,
            provenance=self.provenance,
            stage=stage,
            confidence=confidence,
            contributing_regions=contributions,
        )


__all__ = ["MIN_STAGING_CONFIDENCE", "MockImagingStager"]
