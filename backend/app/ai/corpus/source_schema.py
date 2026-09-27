"""Source-file schema for the curated retrieval corpus (ADR-007).

Validates and normalizes a human-authored corpus document without touching a
database, so every check here runs before ingestion writes anything
(`scripts/ingest_documents.py`). This module never imports SQLAlchemy or
opens a session -- `app/ai/` stays database-free (ADR-003, ADR-007 decision
5).
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from app.ai.corpus.policy import (
    ALLOWED_LICENSES,
    ALLOWED_TIERS,
    INJECTION_PATTERNS,
    MAX_PASSAGE_CHARS,
)


_DOCUMENT_ID_RE = re.compile(chr(94) + "[a-z0-9-]{3,100}" + chr(36))

# Control characters (Unicode category Cc, codepoints 0-8, 11-31,
# 127-159) and common zero-width / BOM characters (Cf: U+200B-U+200F,
# U+2028, U+2029, U+FEFF). Built from codepoints via chr() rather than
# backslash-escape sequences: some editing pipelines in this project
# silently decode literal hex/unicode escapes into real control
# characters, corrupting the file with actual null/zero-width bytes.
_CONTROL_CODEPOINTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159]
_ZERO_WIDTH_CODEPOINTS = [8203, 8204, 8205, 8206, 8207, 8232, 8233, 65279]
_STRIP_CHARS = "".join(chr(codepoint) for codepoint in _CONTROL_CODEPOINTS + _ZERO_WIDTH_CODEPOINTS)
_STRIP_CHARS_RE = re.compile("[" + re.escape(_STRIP_CHARS) + "]")


def normalize_passage(text: str) -> str:
    """NFC-normalize, strip control/zero-width characters, collapse whitespace.

    Applied before hashing and before the injection check, so two source
    files that differ only in whitespace or Unicode form produce the same
    `content_sha256` and the same pass/fail outcome.
    """

    normalized = unicodedata.normalize("NFC", text)
    stripped = _STRIP_CHARS_RE.sub("", normalized)
    return " ".join(stripped.split())


def content_sha256(passage_text: str) -> str:
    """Stable hash of an already-normalized passage, used to skip unchanged
    rows on re-ingestion (ADR-007 decision 1: idempotent re-run)."""

    return hashlib.sha256(passage_text.encode("utf-8")).hexdigest()


def _check_injection(text: str, *, where: str) -> None:
    for name, pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            raise ValueError(
                f"{where} matches the {name!r} rejected pattern; a human "
                "must review this passage before it can be ingested"
            )


class CorpusPassage(BaseModel):
    """One quoted, reviewed passage within a source document."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def _normalize_and_check(cls, value: str) -> str:
        normalized = normalize_passage(value)
        if not normalized:
            raise ValueError("passage text is empty after normalization")
        if len(normalized) > MAX_PASSAGE_CHARS:
            raise ValueError(
                f"passage exceeds MAX_PASSAGE_CHARS={MAX_PASSAGE_CHARS} "
                "characters after normalization"
            )
        _check_injection(normalized, where="passage text")
        return normalized


class CorpusSourceFile(BaseModel):
    """One YAML file under `backend/corpus/documents/` (ADR-007 decision 1)."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    source: str = Field(min_length=1, max_length=255)
    citation: str = Field(min_length=1, max_length=500)
    source_url: str | None = Field(default=None, max_length=500)
    source_tier: str
    published_year: int | None = Field(default=None, ge=1800, le=2200)
    license: str
    keywords: list[str] = Field(min_length=1)
    reviewed_by: str = Field(min_length=1)
    reviewed_at: date
    passages: list[CorpusPassage] = Field(min_length=1)

    @field_validator("document_id")
    @classmethod
    def _valid_document_id(cls, value: str) -> str:
        if not _DOCUMENT_ID_RE.match(value):
            raise ValueError("document_id must match [a-z0-9-]{3,100}")
        return value

    @field_validator("source_tier")
    @classmethod
    def _valid_tier(cls, value: str) -> str:
        if value not in ALLOWED_TIERS:
            raise ValueError(
                f"source_tier must be one of {sorted(ALLOWED_TIERS)}, got {value!r}"
            )
        return value

    @field_validator("license")
    @classmethod
    def _valid_license(cls, value: str) -> str:
        if value not in ALLOWED_LICENSES:
            raise ValueError(
                f"license must be one of {sorted(ALLOWED_LICENSES)}, got {value!r}"
            )
        return value

    @field_validator("reviewed_by")
    @classmethod
    def _non_empty_reviewer(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("reviewed_by must not be blank")
        return value

    @field_validator("reviewed_at")
    @classmethod
    def _not_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("reviewed_at cannot be in the future")
        return value

    @field_validator("citation")
    @classmethod
    def _check_citation_injection(cls, value: str) -> str:
        _check_injection(value, where="citation")
        return value

    @model_validator(mode="after")
    def _check_chunk_ids(self) -> "CorpusSourceFile":
        prefix = f"{self.document_id}#c"
        seen: set[str] = set()
        for passage in self.passages:
            if not passage.chunk_id.startswith(prefix):
                raise ValueError(
                    f"chunk_id {passage.chunk_id!r} must start with {prefix!r}"
                )
            if passage.chunk_id in seen:
                raise ValueError(f"duplicate chunk_id {passage.chunk_id!r}")
            seen.add(passage.chunk_id)
        return self


class CorpusManifest(BaseModel):
    """`backend/corpus/manifest.yaml`: the active corpus version and its files."""

    model_config = ConfigDict(extra="forbid")

    corpus_version: str = Field(min_length=1, max_length=40)
    description: str = ""
    files: list[str] = Field(default_factory=list)


class CorpusSourceError(ValueError):
    """A source file failed validation or violates the loading policy.

    Distinct from `pydantic.ValidationError` so a caller (the ingestion CLI)
    can catch one exception type regardless of whether the failure was a
    schema violation or a path-policy refusal, while still carrying the
    file path in the message.
    """


def load_manifest(path: Path) -> CorpusManifest:
    """Load and validate `manifest.yaml`."""

    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    try:
        return CorpusManifest.model_validate(raw)
    except ValidationError as exc:
        raise CorpusSourceError(f"{path}: {exc}") from exc


def load_source_file(path: Path, *, documents_dir: Path) -> CorpusSourceFile:
    """Load and validate one corpus source document.

    Refuses any path that does not resolve under `documents_dir` --
    `backend/corpus/pending/` in particular is where a future automated
    fetcher writes candidates, and the loader must never read it directly
    (ADR-007 decision 1: a human moving the file into `documents/` and
    filling `reviewed_by` *is* the review gate).
    """

    resolved = path.resolve()
    documents_root = documents_dir.resolve()
    if documents_root != resolved and documents_root not in resolved.parents:
        raise CorpusSourceError(
            f"{path} is not under {documents_root}; only reviewed files in "
            "documents/ may be loaded"
        )

    try:
        with resolved.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
    except OSError as exc:
        raise CorpusSourceError(f"{path}: {exc}") from exc

    try:
        return CorpusSourceFile.model_validate(raw)
    except ValidationError as exc:
        raise CorpusSourceError(f"{path}: {exc}") from exc


__all__ = [
    "CorpusManifest",
    "CorpusPassage",
    "CorpusSourceError",
    "CorpusSourceFile",
    "content_sha256",
    "load_manifest",
    "load_source_file",
    "normalize_passage",
]
