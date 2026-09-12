"""The demo seed's scenarios produce the triage flags they claim to.

The seed's whole purpose is a queue with something to rank (ADR-006 decision
7), so the load-bearing property is that each scripted patient really lands
in its stated queue state when the real mock pipeline runs over it. This
replays every scenario through the actual orchestrator and the triage
service's own flag mapping, without a database: Patient cannot be created on
SQLite (postgresql.ARRAY), and nothing here needs persistence.
"""

import hashlib
from datetime import datetime, timedelta, timezone
from importlib import util
from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.ai.context import build_clinical_context
from app.ai.providers.mock_staging import STAGES
from app.models.patient import Patient
from app.models.scan import Scan
from app.models.symptom import Symptom
from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.services.analysis_service import AnalysisService
from app.services.triage_service import TriageService


SEED_PATH = Path(__file__).resolve().parents[2] / "scripts" / "seed_demo_case.py"
NOW = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)


def _load_seed():
    spec = util.spec_from_file_location("seed_demo_case", SEED_PATH)
    assert spec is not None and spec.loader is not None
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


seed = _load_seed()

ALL_PATIENTS = [
    patient for clinician in seed.CLINICIANS for patient in clinician.patients
]


def _visit(patient_id, spec_visit, label: str) -> Visit:
    content = seed.synthetic_scan(label, spec_visit.stage)
    visit = Visit(
        id=uuid4(),
        patient_id=patient_id,
        visit_date=NOW - timedelta(days=spec_visit.days_ago),
        chief_complaint=spec_visit.complaint,
        vitals={},
        status=VisitStatus.SUBMITTED,
        symptoms=[
            Symptom(
                id=uuid4(),
                symptom_name=symptom.name,
                severity=symptom.severity,
                onset=symptom.onset,
                duration_days=30,
                is_deleted=False,
            )
            for symptom in spec_visit.symptoms
        ],
    )
    visit.scan = Scan(
        checksum=hashlib.sha256(content).hexdigest(),
        content_type=seed.SCAN_CONTENT_TYPE,
        dimensions={},
    )
    return visit


@pytest.mark.parametrize("stage", STAGES)
def test_synthetic_scan_stages_as_requested_and_is_deterministic(stage):
    first = seed.synthetic_scan("label", stage)

    assert first == seed.synthetic_scan("label", stage)
    assert first.startswith(b"SYNTHETIC-DEMO-SCAN")


@pytest.mark.parametrize("spec", ALL_PATIENTS, ids=lambda spec: spec.key)
def test_scenario_lands_in_its_stated_queue_state(spec):
    orchestrator = seed.mock_orchestrator()
    analysis_service = AnalysisService(Mock(), Mock(), Mock(), orchestrator)
    clinician = User(id=uuid4(), role=UserRole.CLINICIAN)
    patient = Patient(id=uuid4(), dob=spec.dob, gender=spec.gender)

    history: list[Visit] = []
    latest = None
    for index, spec_visit in enumerate(spec.visits):
        visit = _visit(patient.id, spec_visit, f"{spec.key}-{index + 1}")

        # Same order as the seed: a visit only ever sees earlier visits.
        if spec_visit.analyse:
            context = build_clinical_context(visit, history, patient=patient)
            latest = analysis_service._to_analysis(
                orchestrator.run(context),
                clinician,
                context.model_dump(mode="json"),
            )
            latest.id = uuid4()
            if spec_visit.sign_off:
                latest.reviewed_at = NOW

        history.append(visit)

    assert latest is not None, "every scenario analyses at least one visit"
    assert latest.provider_mode == "simulated"

    entry = TriageService(Mock(), Mock())._to_entry(
        Patient(id=patient.id, first_name=spec.first_name, last_name=spec.last_name),
        latest,
    )
    assert seed.Flags(
        early_watch=entry.has_open_early_watch,
        worsening=entry.has_worsening_trend,
        sign_off=entry.awaiting_sign_off,
    ) == spec.expected


def test_primary_panel_covers_every_queue_state_in_ranking_order():
    primary = seed.CLINICIANS[0]
    flags = [patient.expected for patient in primary.patients]

    assert any(f.early_watch for f in flags)
    assert any(f.worsening and not f.early_watch for f in flags)
    assert any(f.sign_off and not (f.worsening or f.early_watch) for f in flags)
    assert any(not (f.sign_off or f.worsening or f.early_watch) for f in flags)

    def priority(f):
        return (not f.early_watch, not f.worsening, not f.sign_off)

    assert flags == sorted(flags, key=priority)


def test_one_follow_up_visit_is_left_for_the_live_demo():
    unanalysed = [
        visit
        for patient in seed.CLINICIANS[0].patients
        for visit in patient.visits
        if not visit.analyse
    ]
    assert len(unanalysed) == 1


def test_second_clinician_exists_for_the_isolation_check():
    assert [c.username for c in seed.CLINICIANS] == [
        "demo-clinician",
        "demo-clinician-2",
    ]
