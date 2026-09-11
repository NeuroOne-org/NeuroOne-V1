"""Persisted AI analysis, its ranked findings, and their citations.

Naming is constrained by AGENTS.md section 8.2, which forbids representing
output as a definitive diagnosis "not in the schema, not in API field naming".
Hence a table called ``analysis_findings`` with a ``condition_name`` column, and
the deliberate absence of ``final_diagnosis`` and ``doctor_verified`` -- the two
columns the abandoned Diagnosis stub carried. See ADR-003.
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any
import uuid

from sqlalchemy import (
    JSON,
    UUID,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .visit import Visit


class FindingCategory(str, Enum):
    """Whether a ranked condition sits in the differential or is flagged early.

    ``EARLY_WATCH`` requires a non-empty ``trend_basis`` -- the flag must be
    traceable to the patient's own visit history (AGENTS.md section 8.2).
    """

    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    EARLY_WATCH = "early_watch"


class Analysis(BaseModel):
    """One run of the AI pipeline against one clinical case.

    Re-running creates a new row rather than overwriting: re-analysing after
    adding symptoms is the natural clinician action, and overwriting would
    destroy prior traceable output.
    """

    __tablename__ = "analyses"

    __table_args__ = (
        Index("ix_analyses_visit_created", "visit_id", "created_at"),
    )

    # ForeignKeys
    visit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )
    visit: Mapped["Visit"] = relationship("Visit")

    requested_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Provenance. Surfaced on the wire as well as stored: a consumer must be
    # able to tell simulated evidence from live evidence (AGENTS.md 8.1).
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    pipeline_note: Mapped[str] = mapped_column(Text, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # The exact context the model reasoned over, so traceability survives later
    # edits to the visit.
    context_snapshot: Mapped[dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=dict,
    )

    # Sign-off (ADR-006 decision 6). Both null until a clinician reviews the
    # analysis; a report cannot be generated until they are set (see
    # ReportService.generate_report). This is what makes "a clinician
    # reviewed it" structural rather than a disclaimer: nothing leaves the
    # system as a document that a human did not accept.
    reviewed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    findings: Mapped[list["AnalysisFinding"]] = relationship(
        "AnalysisFinding",
        back_populates="analysis",
        cascade="all, delete-orphan",
        order_by="AnalysisFinding.rank",
    )


class AnalysisFinding(BaseModel):
    """One ranked candidate condition.

    Decision support, never a definitive diagnosis: the column is
    ``condition_name`` and the number is a ``confidence``, not a certainty.
    """

    __tablename__ = "analysis_findings"

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="confidence_range",
        ),
        UniqueConstraint("analysis_id", "rank"),
    )

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id"),
        nullable=False,
        index=True,
    )
    analysis: Mapped["Analysis"] = relationship(
        "Analysis",
        back_populates="findings",
    )

    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[FindingCategory] = mapped_column(
        SQLEnum(FindingCategory),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    supporting_findings: Mapped[list[str]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=list,
    )
    contradicting_findings: Mapped[list[str]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=list,
    )
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    # A snapshot of reasoning rather than a live relation: foreign keys would
    # let a later severity edit rewrite what a past analysis said. The ids
    # inside are real visits.id / symptoms.id values, but they are soft
    # references by design (ADR-003).
    trend_basis: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=list,
    )

    evidence: Mapped[list["AnalysisEvidence"]] = relationship(
        "AnalysisEvidence",
        back_populates="finding",
        cascade="all, delete-orphan",
        order_by="AnalysisEvidence.rank",
    )


class AnalysisEvidence(BaseModel):
    """One citation supporting one ranked finding.

    Scoped to a finding rather than to a report, so a citation can say which
    recommendation it supports (AGENTS.md section 8.4.6).
    """

    __tablename__ = "analysis_evidence"

    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analysis_findings.id"),
        nullable=False,
        index=True,
    )
    finding: Mapped["AnalysisFinding"] = relationship(
        "AnalysisFinding",
        back_populates="evidence",
    )

    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    # The three fields of the section 8.2 evidence contract.
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    citation: Mapped[str] = mapped_column(String(500), nullable=False)
    relevant_passage: Mapped[str] = mapped_column(Text, nullable=False)

    # Source metadata preserved per section 8.4.4.
    document_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    chunk_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_tier: Mapped[str | None] = mapped_column(String(30), nullable=True)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)


__all__ = ["Analysis", "AnalysisEvidence", "AnalysisFinding", "FindingCategory"]
