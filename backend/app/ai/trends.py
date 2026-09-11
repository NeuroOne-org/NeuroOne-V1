"""Cross-visit symptom trend detection.

This is the mechanism behind AGENTS.md section 8.3's early-detection design:
trend-aware reasoning over clinician-entered data across a patient's visit
history. It computes no diagnosis and makes no clinical judgement -- it reports
how a recorded severity moved, and carries the ids it moved between so the
reasoning stays traceable.

Pure: no database, no ORM, no I/O.
"""

from collections.abc import Collection, Sequence

from app.schemas.analysis import TrendBasisRef
from app.schemas.clinical_context import (
    ContextVisit,
    SymptomTrend,
    TrendDirection,
    TrendPoint,
)


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
    relied on to accept soft references (ADR-004).

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


__all__ = [
    "MIN_VISITS_FOR_TREND",
    "detect_trends",
    "normalize_symptom_name",
    "trend_basis_refs",
    "worsening_symptom_names",
]
