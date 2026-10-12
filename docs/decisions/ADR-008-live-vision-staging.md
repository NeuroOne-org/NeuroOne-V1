# ADR-008: Live Vision Staging Behind the ADR-006 Seam

## Status
Proposed (2026-10-07).

## Context
[ADR-006](ADR-006-mri-primary-with-symptoms-as-context.md) put MRI staging behind its own `ImagingStager` seam, and only `MockImagingStager` filled it. That mock derives a stage from a sha256 of the scan's checksum and never reads a pixel. Reasoning ([ADR-005](ADR-005-live-llm-provider.md)) and retrieval ([ADR-007](ADR-007-curated-retrieval-corpus.md)) already have live providers. Staging was the last seam that could only be simulated.

## Decision
1. **A general-purpose vision model on the existing endpoint.** `AI_STAGING_PROVIDER=live-vision` selects `LiveImagingStager` (`app/ai/providers/live_staging.py`). It sends one rendered slice to `AI_VISION_MODEL` through the same OpenAI-compatible `/chat/completions` endpoint and API key as `AI_LLM_*`. Transport, retry and logging are shared with `LiveLLMClient` through `chat_completion_text`.
2. **Pixels reach the provider through a new `ScanImages` seam** (`app/ai/providers/base.py`). It follows the same shape as `CorpusSearch`: the adapter (`app/services/scan_images.py`) looks the scan up by checksum and renders a PNG, so the storage key and filename never enter `app/ai/`.
3. **One 2D greyscale slice only, with no headers.**
   - NIfTI: the middle axial slice.
   - DICOM: `pixel_array` only. Headers carry PHI and are never forwarded.
   - PNG/JPEG: re-encoded, which drops EXIF.
4. **Output is untrusted.** It is validated against a narrow payload model. Confidence is clamped to `MAX_CONFIDENCE`, and regions outside the mock's fixed vocabulary are dropped. *(Amended 2026-10-12: a blank, single-value slice is refused before the call, and the model declines an unreadable image with stage `NOT_MRI` rather than a guessed `CN`. A `NOT_MRI` answer or a confidence of 0 raises, so it is never stored or pinned as a stage.)* A failure becomes `AIError(staging_error)` through the orchestrator, as before.
5. **Results are persisted per checksum and model.** The orchestrator re-stages every prior scan on each analysis. Without a store, each run would cost N paid calls and a prior visit's stage could drift between runs. *(Amended 2026-10-12: originally an in-memory cache. Results now live in the `staging_results` table, keyed on (checksum, model_name), behind a `StagingStore` seam wrapped around the stager by `StoredImagingStager`. A changed `AI_VISION_MODEL` stages again rather than serving the old model's answer. `build_providers()` refuses `live-vision` without a store.)*
6. **The default stays `mock`.** `build_providers()` refuses `live-vision` at startup when there is no API key or no `ScanImages`.

## Why
It needs no new infrastructure, no model weights and no GPU, and it fills the seam ADR-006 designed for exactly this swap. Nothing downstream changes, and the pipeline note already reports "imaging staging live".

## Risks
- **Not a validated radiology model.** A general vision model reading one slice is weak evidence. The output stays one candidate inside a cited differential (ADR-006 decision 3) and is never a lone verdict, but the label "live" says only that a real model ran, not that the estimate is clinically validated.
- **Scan pixels go to a third party.** This is acceptable only under the same synthetic-demo-data assumption as ADR-005.
- **A stored stage is never re-read from the image.** A bad first answer sticks for that model until its row is deleted. That is the price of a stable cross-visit trend.
- **Some DICOM transfer syntaxes need extra pixel handlers** that aren't installed. Those scans fail with `staging_error` instead of being mis-staged.

## Alternatives Rejected
- **A pretrained CNN (ADNI/OASIS) in the API container.** Heavy dependencies, weights and preprocessing. It remains the upgrade path behind the same seam.
- **A hosted inference endpoint.** It would only move the same model question somewhere else.

## Testing Impact
`tests/test_ai_live_staging.py`, using `httpx.MockTransport` with no network: the happy path, confidence clamping, unknown regions, malformed output, declined reads, blank and NaN slices, the stored stage, registry refusals, and PNG/NIfTI rendering.
