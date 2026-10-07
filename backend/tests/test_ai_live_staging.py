"""Tests for the live vision staging provider and its scan renderer (ADR-008).

No network: the chat-completions endpoint is an ``httpx.MockTransport``, the
same convention as ``test_ai_live_llm.py``.
"""

import gzip
import io
import json

import httpx
import nibabel
import numpy as np
import pytest
from PIL import Image
from pydantic import ValidationError

from app.ai.providers import build_providers
from app.ai.providers.live_staging import LiveImagingStager
from app.ai.providers.mock_staging import MockImagingStager
from app.core.config import Settings
from app.schemas.analysis import MAX_CONFIDENCE
from app.schemas.imaging import StagingRequest
from app.services.scan_images import render_png


PNG = b"\x89PNG-test-bytes"
REQUEST = StagingRequest(checksum="a" * 64, content_type="image/png")


def _settings(**overrides) -> Settings:
    defaults = {
        "AI_STAGING_PROVIDER": "live-vision",
        "AI_LLM_BASE_URL": "https://llm.test/v1",
        "AI_VISION_MODEL": "test-vision-v1",
        "AI_LLM_API_KEY": "test-key",
    }
    return Settings(**{**defaults, **overrides})


class FakeImages:
    def __init__(self, png=PNG):
        self.png = png

    def preview_png(self, checksum):
        return self.png


def _stager(content, requests=None, images=None) -> LiveImagingStager:
    def handler(request: httpx.Request) -> httpx.Response:
        if requests is not None:
            requests.append(json.loads(request.content))
        body = content if isinstance(content, str) else json.dumps(content)
        return httpx.Response(200, json={"choices": [{"message": {"content": body}}]})

    return LiveImagingStager(
        _settings(),
        images or FakeImages(),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_stages_from_model_output_and_sends_the_image():
    requests = []
    result = _stager(
        {
            "stage": "MCI",
            "confidence": 0.6,
            "contributing_regions": [
                {"region": "Hippocampus", "contribution": 3},
                {"region": "Lateral ventricles", "contribution": 1},
            ],
        },
        requests,
    ).stage(REQUEST)

    assert (result.stage, result.confidence, result.provenance) == ("MCI", 0.6, "live")
    assert result.model_name == "test-vision-v1"
    assert [(r.region, r.contribution) for r in result.contributing_regions] == [
        ("Hippocampus", 0.75),
        ("Lateral ventricles", 0.25),
    ]
    image_part = requests[0]["messages"][1]["content"][1]
    assert image_part["image_url"]["url"].startswith("data:image/png;base64,")
    assert requests[0]["model"] == "test-vision-v1"


def test_clamps_confidence_and_drops_unknown_regions():
    result = _stager(
        {
            "stage": "Severe",
            "confidence": 0.99,
            "contributing_regions": [{"region": "Patient name: X", "contribution": 1}],
        }
    ).stage(REQUEST)

    assert result.confidence == MAX_CONFIDENCE
    assert result.contributing_regions == []


@pytest.mark.parametrize(
    "content, error",
    [
        ("not json", ValidationError),
        ({"stage": "MCI", "confidence": 0.5, "verdict": "x"}, ValidationError),
        ({"stage": "Alzheimer's", "confidence": 0.5}, ValueError),
    ],
)
def test_malformed_output_raises(content, error):
    with pytest.raises(error):
        _stager(content).stage(REQUEST)


def test_missing_image_raises():
    with pytest.raises(ValueError):
        _stager({"stage": "CN", "confidence": 0.1}, images=FakeImages(None)).stage(REQUEST)


def test_same_scan_is_only_sent_once():
    requests = []
    stager = _stager({"stage": "Mild", "confidence": 0.7}, requests)

    assert stager.stage(REQUEST) == stager.stage(REQUEST)
    assert len(requests) == 1


def test_registry_builds_and_refuses_live_vision():
    _, _, stager = build_providers(_settings(), scan_images=FakeImages())
    assert isinstance(stager, LiveImagingStager)

    with pytest.raises(ValueError, match="AI_LLM_API_KEY"):
        build_providers(_settings(AI_LLM_API_KEY=None), scan_images=FakeImages())
    with pytest.raises(ValueError, match="scan_images"):
        build_providers(_settings())

    _, _, stager = build_providers(_settings(AI_STAGING_PROVIDER="mock"))
    assert isinstance(stager, MockImagingStager)


def _decoded(png: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(png))
    assert image.format == "PNG"
    return image


def test_render_png_reencodes_jpeg_to_greyscale_png():
    source = io.BytesIO()
    Image.new("RGB", (8, 6), (200, 10, 10)).save(source, format="JPEG")

    image = _decoded(render_png(source.getvalue(), "scan.jpg"))
    assert (image.size, image.mode) == ((8, 6), "L")


@pytest.mark.parametrize("filename", ["brain.nii", "brain.nii.gz"])
def test_render_png_takes_middle_slice_of_nifti(filename):
    volume = np.zeros((10, 12, 5), dtype=np.float32)
    volume[:, :, 2] = np.arange(120).reshape(10, 12)
    content = nibabel.Nifti1Image(volume, np.eye(4)).to_bytes()
    if filename.endswith(".gz"):
        content = gzip.compress(content)

    pixels = np.asarray(_decoded(render_png(content, filename)))
    # rot90 of a 10x12 slice; a non-middle slice would render all black.
    assert pixels.shape == (12, 10)
    assert pixels.max() == 255
