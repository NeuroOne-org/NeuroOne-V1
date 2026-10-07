"""Live MRI staging through a vision model on the chat-completions endpoint.

The ADR-008 counterpart to ``mock_staging``: one rendered 2D slice of the scan
goes to a general-purpose vision model, which returns a stage estimate. It is
a general model, not a validated radiology classifier -- its output stays one
candidate inside the cited differential (ADR-006 decision 3), never a verdict.

Model output is untrusted, as in ``live_llm``: the payload is validated here,
confidence is clamped to the certainty ceiling, and region names outside the
mock's fixed vocabulary are dropped rather than passed on.
"""

import base64
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field

from app.ai.providers.base import ScanImages
from app.ai.providers.live_llm import chat_completion_text
from app.ai.providers.mock_staging import REGIONS, STAGES
from app.core.config import Settings
from app.schemas.analysis import MAX_CONFIDENCE
from app.schemas.imaging import RegionContribution, StagingRequest, StagingResult


SYSTEM_PROMPT = f"""You are a decision-support assistant estimating a \
dementia stage from one 2D slice of a brain MRI. Your estimate is one input \
for a clinician, never a diagnosis.

Return JSON only, in exactly this shape:

{{
  "stage": one of {list(STAGES)},
  "confidence": 0.0 to {MAX_CONFIDENCE},
  "contributing_regions": [
    {{"region": one of {list(REGIONS)}, "contribution": 0.0 to 1.0}}
  ]
}}

Hard rules:
- At most 3 contributing_regions, the regions whose appearance (atrophy, \
ventricular enlargement) most informed the stage.
- confidence is a likelihood, never a certainty. It must not exceed \
{MAX_CONFIDENCE}. A single slice is limited evidence, so be conservative.
- If the image is not a brain MRI, still return the shape with stage "CN" \
and confidence 0.0."""


class LiveRegionPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    region: str
    contribution: float


class LiveStagingPayload(BaseModel):
    """The model's response. Structural violations raise at the seam."""

    model_config = ConfigDict(extra="forbid")

    stage: str
    confidence: float
    contributing_regions: list[LiveRegionPayload] = Field(default_factory=list)


class LiveImagingStager:
    """Stager backed by a vision model behind ``ImagingStager``."""

    provenance = "live"

    def __init__(
        self,
        config: Settings,
        scan_images: ScanImages,
        *,
        client: httpx.Client | None = None,
    ):
        self.name = config.AI_VISION_MODEL
        self._config = config
        self._scan_images = scan_images
        self._client = client
        # The orchestrator re-stages every prior scan on each analysis
        # (orchestrator._stage); without this, each run costs N paid calls and
        # a prior visit's stage could change between runs.
        # ponytail: per-process cache, persist StagingResult per scan if
        # restarts or multiple workers make the drift matter.
        self._cache: dict[str, StagingResult] = {}

    def _request_body(self, png: bytes) -> dict[str, Any]:
        image_url = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
        return {
            "model": self.name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Estimate the stage for this slice."},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                },
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": self._config.AI_LLM_MAX_OUTPUT_TOKENS,
            "temperature": 0,
        }

    def _to_result(self, payload: LiveStagingPayload) -> StagingResult:
        if payload.stage not in STAGES:
            raise ValueError("live staging provider returned an unknown stage")

        regions = {
            item.region: max(item.contribution, 0.0)
            for item in payload.contributing_regions
            if item.region in REGIONS
        }
        total = sum(regions.values()) or 1.0
        contributions = sorted(
            (
                RegionContribution(region=region, contribution=round(weight / total, 4))
                for region, weight in regions.items()
            ),
            key=lambda contribution: -contribution.contribution,
        )[:3]

        return StagingResult(
            model_name=self.name,
            provenance=self.provenance,
            stage=payload.stage,
            confidence=round(min(max(payload.confidence, 0.0), MAX_CONFIDENCE), 4),
            contributing_regions=contributions,
        )

    def stage(self, request: StagingRequest) -> StagingResult:
        """Stage one scan, reusing the result for a checksum already seen."""

        cached = self._cache.get(request.checksum)
        if cached is not None:
            return cached

        png = self._scan_images.preview_png(request.checksum)
        if png is None:
            raise ValueError("no renderable image for this scan")

        text = chat_completion_text(
            self._config,
            self._request_body(png),
            client=self._client,
            purpose="staging",
            model=self.name,
            ref=request.checksum[:12],
        )
        result = self._to_result(LiveStagingPayload.model_validate_json(text))
        self._cache[request.checksum] = result
        return result


__all__ = ["LiveImagingStager", "LiveStagingPayload"]
