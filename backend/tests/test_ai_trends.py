"""Tests for cross-visit trend detection.

A trend is what an early_watch flag points at, so these assertions are about
traceability as much as arithmetic: the points must carry the real visit and
symptom ids they were derived from.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.ai.trends import (
    detect_trends,
    normalize_symptom_name,
    worsening_symptom_names,
)
from app.schemas.clinical_context import ContextSymptom, ContextVisit


BASE_DATE = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)


def _visit(*symptoms, days_offset=0, complaint="tremor"):
    """symptoms: (name, severity) tuples."""
    return ContextVisit(
        id=uuid4(),
        visit_date=BASE_DATE + timedelta(days=days_offset),
        chief_complaint=complaint,
        symptoms=[
            ContextSymptom(id=uuid4(), symptom_name=name, severity=severity)
            for name, severity in symptoms
        ],
    )


def _series(*severities, name="tremor"):
    """One visit per severity, 30 days apart, oldest-first."""
    return [
        _visit((name, severity), days_offset=index * 30)
        for index, severity in enumerate(severities)
    ]


def test_rising_severity_is_worsening() -> None:
    trends = detect_trends(_series(3, 5, 8))

    assert len(trends) == 1
    trend = trends[0]
    assert trend.direction == "worsening"
    assert trend.first_severity == 3
    assert trend.latest_severity == 8
    assert trend.visit_span == 3


def test_falling_severity_is_improving() -> None:
    assert detect_trends(_series(8, 5, 3))[0].direction == "improving"


def test_mixed_severity_is_fluctuating() -> None:
    assert detect_trends(_series(5, 8, 5))[0].direction == "fluctuating"


def test_unchanged_severity_is_stable() -> None:
    assert detect_trends(_series(4, 4, 4))[0].direction == "stable"


def test_a_single_visit_yields_no_trend() -> None:
    """One observation is a snapshot, not a direction."""
    assert detect_trends(_series(7)) == []


def test_repeated_symptom_within_one_visit_yields_no_trend() -> None:
    """Two rows on the same visit still span only one visit."""
    single = _visit(("tremor", 3), ("tremor", 8))

    assert detect_trends([single]) == []


def test_symptom_names_are_normalized_into_one_series() -> None:
    visits = [
        _visit(("Tremor", 3), days_offset=0),
        _visit(("  tremor  ", 8), days_offset=30),
    ]

    trends = detect_trends(visits)

    assert len(trends) == 1
    assert trends[0].symptom_name == "tremor"
    assert trends[0].direction == "worsening"


def test_points_carry_the_real_visit_and_symptom_ids_oldest_first() -> None:
    visits = _series(3, 5, 8)
    expected_visit_ids = [visit.id for visit in visits]
    expected_symptom_ids = [visit.symptoms[0].id for visit in visits]

    points = detect_trends(visits)[0].points

    assert [point.visit_id for point in points] == expected_visit_ids
    assert [point.symptom_id for point in points] == expected_symptom_ids
    assert [point.severity for point in points] == [3, 5, 8]
    assert [point.visit_date for point in points] == sorted(
        point.visit_date for point in points
    )


def test_distinct_symptoms_produce_distinct_trends_ordered_by_name() -> None:
    visits = [
        _visit(("tremor", 3), ("aphasia", 2), days_offset=0),
        _visit(("tremor", 8), ("aphasia", 6), days_offset=30),
    ]

    trends = detect_trends(visits)

    assert [trend.symptom_name for trend in trends] == ["aphasia", "tremor"]


def test_only_symptoms_seen_more_than_once_produce_a_trend() -> None:
    visits = [
        _visit(("tremor", 3), days_offset=0),
        _visit(("tremor", 8), ("headache", 5), days_offset=30),
    ]

    trends = detect_trends(visits)

    assert [trend.symptom_name for trend in trends] == ["tremor"]


def test_worsening_names_selects_only_rising_trends() -> None:
    visits = [
        _visit(("tremor", 3), ("aphasia", 8), days_offset=0),
        _visit(("tremor", 8), ("aphasia", 2), days_offset=30),
    ]

    assert worsening_symptom_names(detect_trends(visits)) == {"tremor"}


def test_no_visits_yields_no_trends() -> None:
    assert detect_trends([]) == []


def test_normalize_collapses_case_and_internal_whitespace() -> None:
    assert normalize_symptom_name("  Resting   Tremor ") == "resting tremor"
