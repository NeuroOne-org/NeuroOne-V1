"""Cross-visit symptom trend detection.

This is the mechanism behind AGENTS.md section 8.3's early-detection design:
trend-aware reasoning over clinician-entered data across a patient's visit
history. It computes no diagnosis and makes no clinical judgement -- it reports
how a recorded severity moved, and carries the ids it moved between so the
reasoning stays traceable.

Pure: no database, no ORM, no I/O.
"""

from collections.abc import Collection, Sequence
from datetime import datetime
from uuid import UUID

from app.schemas.analysis import TrendBasisRef
from app.schemas.clinical_context import (
    ContextVisit,
    ScanTrend,
    ScanTrendPoint,
    SymptomTrend,
    TrendDirection,
    TrendPoint,
)
from app.schemas.imaging import STAGE_ORDER, StagingResult


# A symptom seen once is a snapshot, not a direction.
MIN_VISITS_FOR_TREND = 2


def normalize_symptom_name(name: str) -> str:
    """Group key for a symptom, so "Tremor" and "tremor " are one series."""

    return " ".join(name.split()).casefold()


def _direction(severities: Sequence[int]) -> TrendDirection:
    """Classify a severity series ordered oldest-first."""

    deltas = [
        later - earlier
        for earlier, later in zip(severities, severities[1:])
    ]

    rose = any(delta > 0 for delta in deltas)
    fell = any(delta < 0 for delta in deltas)

    if rose and fell:
        return "fluctuating"
    if rose:
        return "worsening"
    if fell:
        return "improving"
    return "stable"


def detect_trends(visits: Sequence[ContextVisit]) -> list[SymptomTrend]:
    """Detect per-symptom severity trends across a patient's visits.

    ``visits`` must be ordered oldest-first -- CASE-01's history retrieval
    already provides that ordering, so nothing is re-sorted here.

    Only symptoms recorded at two or more distinct visits yield a trend.
    Results are ordered by symptom name so the output is reproducible.
    """

    series: dict[str, list[tuple[ContextVisit, TrendPoint]]] = {}

    for visit in visits:
        for symptom in visit.symptoms:
            key = normalize_symptom_name(symptom.symptom_name)
            series.setdefault(key, []).append(
                (
                    visit,
                    TrendPoint(
                        visit_id=visit.id,
                        symptom_id=symptom.id,
                        visit_date=visit.visit_date,
                        severity=symptom.severity,
                    ),
                )
            )

    trends: list[SymptomTrend] = []

    for key, entries in series.items():
        distinct_visits = {visit.id for visit, _ in entries}
        if len(distinct_visits) < MIN_VISITS_FOR_TREND:
            continue

        points = [point for _, point in entries]
        severities = [point.severity for point in points]

        trends.append(
            SymptomTrend(
                symptom_name=key,
                direction=_direction(severities),
                first_severity=severities[0],
                latest_severity=severities[-1],
                visit_span=len(distinct_visits),
                points=points,
            )
        )

    return sorted(trends, key=lambda trend: trend.symptom_name)


def worsening_symptom_names(trends: Sequence[SymptomTrend]) -> set[str]:
    """Normalized names of symptoms that are getting worse across visits.

    This is the set that qualifies a candidate for an ``early_watch`` flag.
    """

    return {
        trend.symptom_name
        for trend in trends
        if trend.direction == "worsening"
    }


def trend_basis_refs(
    trends: Sequence[SymptomTrend],
    matched_names: Collection[str],
) -> list[TrendBasisRef]:
    """Build history references for the matched worsening symptoms.

    Every reference points at a real visit and symptom row, which is what
    makes an early_watch flag traceable (AGENTS.md section 8.2).

    Shared by both providers deliberately: under AI-02 a live model names the
    symptoms it reasoned over, and these ids are resolved here from the
    patient's own context rather than authored by the model. A fabricated id
    would be indistinguishable from a stale one, which is the premise ADR-003
    relied on to accept soft references (ADR-005).

    ``matched_names`` holds normalized names -- see ``normalize_symptom_name``.
    """

    refs: list[TrendBasisRef] = []
    for trend in trends:
        if trend.direction != "worsening" or trend.symptom_name not in matched_names:
            continue

        observation = (
            f"{trend.symptom_name} severity {trend.first_severity} -> "
            f"{trend.latest_severity} across {trend.visit_span} visits"
        )
        for point in trend.points:
            refs.append(
                TrendBasisRef(
                    visit_id=point.visit_id,
                    symptom_id=point.symptom_id,
                    symptom_name=trend.symptom_name,
                    visit_date=point.visit_date,
                    severity=point.severity,
                    observation=observation,
                )
            )
    return refs


def detect_stage_trend(
    observations: Sequence[tuple[UUID, datetime, StagingResult]],
) -> ScanTrend | None:
    """Detect how an imaging-derived stage moved across a patient's visits.

    Mirrors ``detect_trends``, but over the ordinal ``STAGE_ORDER`` scale
    rather than a clinician-entered severity (ADR-006 consequence: without
    this, the scan contributes nothing to trend-aware early detection).

    Deliberately takes already-staged results rather than scans: staging is a
    provider call, and this module stays pure (no database, no ORM, no I/O).
    The caller -- the orchestrator, which already holds the stager -- is
    responsible for staging every scanned visit first.

    ``observations`` must be ordered oldest-first and contain only visits
    that actually had a scan. Fewer than two produces no trend, same as a
    symptom observed once.
    """

    distinct_visits = {visit_id for visit_id, _, _ in observations}
    if len(distinct_visits) < MIN_VISITS_FOR_TREND:
        return None

    ordinals = [STAGE_ORDER[result.stage] for _, _, result in observations]

    return ScanTrend(
        direction=_direction(ordinals),
        first_stage=observations[0][2].stage,
        latest_stage=observations[-1][2].stage,
        visit_span=len(distinct_visits),
        points=[
            ScanTrendPoint(visit_id=visit_id, visit_date=visit_date, stage=result.stage)
            for visit_id, visit_date, result in observations
        ],
    )


def stage_trend_basis_ref(trend: ScanTrend | None) -> list[TrendBasisRef]:
    """Build history references for a worsening imaging-derived stage trend.

    Mirrors ``trend_basis_refs``, but for the scan rather than a symptom. Used
    to attach traceable trend history to the staged candidate (ADR-006);
    unlike a symptom's trend_basis, this never changes the candidate's
    category -- the stage estimate stays a differential_diagnosis regardless
    (ADR-006 decision 3), and the reference only enriches its traceability.
    """

    if trend is None or trend.direction != "worsening":
        return []

    observation = (
        f"MRI-derived stage {trend.first_stage} -> {trend.latest_stage} "
        f"across {trend.visit_span} visits"
    )

    return [
        TrendBasisRef(
            visit_id=point.visit_id,
            symptom_id=None,
            symptom_name="MRI-derived stage",
            visit_date=point.visit_date,
            severity=STAGE_ORDER[point.stage] + 1,
            observation=observation,
        )
        for point in trend.points
    ]


__all__ = [
    "MIN_VISITS_FOR_TREND",
    "detect_stage_trend",
    "detect_trends",
    "normalize_symptom_name",
    "stage_trend_basis_ref",
    "trend_basis_refs",
    "worsening_symptom_names",
]
