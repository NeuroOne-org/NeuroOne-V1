"""Seed a synthetic demo panel that exercises the ADR-006 triage queue.

The dashboard is a ranked queue (ADR-006 decision 7): open ``early_watch``
flags first, then worsening trends, then analyses awaiting sign-off. A queue
of one patient has nothing to rank, so this seeds one patient per queue state
for ``demo-clinician``, each visit carrying an MRI scan and symptoms:

  A  tremor 3 -> 5 -> 8 worsens loudly; memory loss 2 -> 3 -> 4 worsens
     quietly and is flagged early_watch       -> early_watch, worsening, sign-off
  B  stable symptoms, MRI stage CN -> MCI -> Mild -> worsening (imaging), sign-off
  C  a single visit, analysed                 -> awaiting sign-off only
  D  a single visit, analysed and signed off  -> no open signals
  E  two analysed visits (the latest signed off) plus a follow-up visit that
     is deliberately NOT analysed, so the demo can run the pipeline live and
     watch the patient move up the queue

``demo-clinician-2`` owns one analysed patient, so a second login can confirm
it cannot see the first clinician's records (ADR-001/ADR-002).

Seeded analyses always use the mock providers, whatever ``AI_PROVIDER`` says:
the seed must be deterministic, offline and free. A live "Run analysis" from
the UI still uses the configured provider.

Scans are small synthetic placeholder files, never images. The mock stager
derives a stage from the scan checksum, so each file's content is chosen to
stage as the scenario needs -- identically on every run.

Re-running is idempotent: everything owned by the two demo usernames is
deleted (reports, analyses, patients, visits, scans and their files, the
accounts) and recreated. Nothing owned by any other account is touched.

Synthetic data only -- per AGENTS.md section 12 the demo environment must not
hold real patient records.

Usage:
    python scripts/seed_demo_case.py
"""

import os
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import select  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.ai.orchestrator import AnalysisOrchestrator  # noqa: E402
from app.ai.providers.mock_llm import MockLLMClient  # noqa: E402
from app.ai.providers.mock_retriever import MockEvidenceRetriever  # noqa: E402
from app.ai.providers.mock_staging import MockImagingStager  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.models.analysis import Analysis  # noqa: E402
from app.models.patient import Patient, PhoneNumber  # noqa: E402
from app.models.report import Report  # noqa: E402
from app.models.scan import Scan  # noqa: E402
from app.models.symptom import Symptom  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.models.visit import Visit, VisitStatus  # noqa: E402
from app.repositories.analysis_repository import AnalysisRepository  # noqa: E402
from app.repositories.patient_repository import PatientRepository  # noqa: E402
from app.repositories.scan_repository import ScanRepository  # noqa: E402
from app.repositories.symptom_repository import SymptomRepository  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.repositories.visit_repository import VisitRepository  # noqa: E402
from app.schemas.imaging import StagingRequest  # noqa: E402
from app.services.analysis_service import AnalysisService  # noqa: E402
from app.services.patient_service import PatientService  # noqa: E402
from app.services.scan_service import ScanService  # noqa: E402
from app.services.triage_service import TriageService  # noqa: E402
from app.services.visit_service import VisitService  # noqa: E402
from app.storage.scan_storage import LocalScanStorage  # noqa: E402


DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "DemoClinician!2026")

SCAN_CONTENT_TYPE = "application/octet-stream"


# -- scenario ------------------------------------------------------------


@dataclass(frozen=True)
class DemoSymptom:
    name: str
    severity: int
    onset: str


@dataclass(frozen=True)
class DemoVisit:
    days_ago: int
    complaint: str
    symptoms: tuple[DemoSymptom, ...]
    # The stage the synthetic scan is chosen to stage as.
    stage: str
    analyse: bool = True
    sign_off: bool = False


@dataclass(frozen=True)
class Flags:
    early_watch: bool
    worsening: bool
    sign_off: bool


@dataclass(frozen=True)
class DemoPatient:
    key: str
    first_name: str
    last_name: str
    gender: str
    dob: date
    visits: tuple[DemoVisit, ...]
    # What the triage queue should say about this patient once seeded.
    expected: Flags


@dataclass(frozen=True)
class DemoClinician:
    username: str
    first_name: str
    last_name: str
    patients: tuple[DemoPatient, ...]


def _tremor_memory(tremor: int, memory: int) -> tuple[DemoSymptom, ...]:
    return (
        DemoSymptom("tremor", tremor, "gradual"),
        DemoSymptom("memory loss", memory, "insidious"),
    )


CLINICIANS: tuple[DemoClinician, ...] = (
    DemoClinician(
        username="demo-clinician",
        first_name="Demo",
        last_name="Clinician",
        patients=(
            DemoPatient(
                key="A",
                first_name="Helen",
                last_name="Marsh",
                gender="F",
                dob=date(1958, 4, 9),
                visits=(
                    DemoVisit(260, "intermittent hand tremor", _tremor_memory(3, 2), "CN"),
                    DemoVisit(140, "intermittent hand tremor", _tremor_memory(5, 3), "CN"),
                    DemoVisit(20, "intermittent hand tremor", _tremor_memory(8, 4), "MCI"),
                ),
                expected=Flags(early_watch=True, worsening=True, sign_off=True),
            ),
            DemoPatient(
                key="B",
                first_name="Arthur",
                last_name="Lin",
                gender="M",
                dob=date(1951, 11, 2),
                visits=tuple(
                    DemoVisit(
                        days_ago,
                        "routine cognitive clinic follow-up",
                        (DemoSymptom("memory loss", 3, "insidious"),),
                        stage,
                    )
                    for days_ago, stage in ((300, "CN"), (160, "MCI"), (30, "Mild"))
                ),
                expected=Flags(early_watch=False, worsening=True, sign_off=True),
            ),
            DemoPatient(
                key="C",
                first_name="Priya",
                last_name="Raman",
                gender="F",
                dob=date(1970, 7, 21),
                visits=(
                    DemoVisit(
                        10,
                        "numbness in both feet",
                        (
                            DemoSymptom("numbness", 4, "gradual"),
                            DemoSymptom("paresthesia", 3, "gradual"),
                        ),
                        "CN",
                    ),
                ),
                expected=Flags(early_watch=False, worsening=False, sign_off=True),
            ),
            DemoPatient(
                key="D",
                first_name="Tomas",
                last_name="Berg",
                gender="M",
                dob=date(1966, 1, 30),
                visits=(
                    DemoVisit(
                        45,
                        "tremor when holding a cup",
                        (DemoSymptom("action tremor", 3, "gradual"),),
                        "CN",
                        sign_off=True,
                    ),
                ),
                expected=Flags(early_watch=False, worsening=False, sign_off=False),
            ),
            DemoPatient(
                key="E",
                first_name="Grace",
                last_name="Adeyemi",
                gender="F",
                dob=date(1955, 9, 14),
                visits=(
                    DemoVisit(
                        200,
                        "mild forgetfulness",
                        (DemoSymptom("memory loss", 2, "insidious"),),
                        "CN",
                    ),
                    DemoVisit(
                        90,
                        "mild forgetfulness",
                        (DemoSymptom("memory loss", 2, "insidious"),),
                        "CN",
                        sign_off=True,
                    ),
                    # Left unanalysed on purpose: the live demo runs this one.
                    DemoVisit(
                        3,
                        "forgetfulness getting worse",
                        (
                            DemoSymptom("memory loss", 4, "insidious"),
                            DemoSymptom("word-finding difficulty", 3, "insidious"),
                        ),
                        "MCI",
                        analyse=False,
                    ),
                ),
                expected=Flags(early_watch=False, worsening=False, sign_off=False),
            ),
        ),
    ),
    DemoClinician(
        username="demo-clinician-2",
        first_name="Second",
        last_name="Clinician",
        patients=(
            DemoPatient(
                key="Z",
                first_name="Oliver",
                last_name="Grant",
                gender="M",
                dob=date(1962, 3, 3),
                visits=(
                    DemoVisit(
                        15,
                        "unsteady balance",
                        (DemoSymptom("ataxia", 4, "subacute"),),
                        "CN",
                    ),
                ),
                expected=Flags(early_watch=False, worsening=False, sign_off=True),
            ),
        ),
    ),
)


# -- synthetic scans -----------------------------------------------------


def synthetic_scan(label: str, stage: str) -> bytes:
    """Placeholder scan bytes that the mock stager stages as ``stage``.

    Asks the real ``MockImagingStager`` rather than re-deriving its hash, so
    this cannot drift from the provider. Deterministic: the same label and
    stage always return the same bytes.
    """

    import hashlib

    stager = MockImagingStager()
    for counter in range(10_000):
        content = f"SYNTHETIC-DEMO-SCAN (not an image)\n{label}\n{counter}\n".encode()
        request = StagingRequest(
            checksum=hashlib.sha256(content).hexdigest(),
            content_type=SCAN_CONTENT_TYPE,
            dimensions={},
        )
        if stager.stage(request).stage == stage:
            return content

    raise RuntimeError(f"No synthetic scan content stages as {stage!r}")


# -- wiring --------------------------------------------------------------


@dataclass
class Services:
    patients: PatientService
    visits: VisitService
    scans: ScanService
    analyses: AnalysisService
    triage: TriageService


def mock_orchestrator() -> AnalysisOrchestrator:
    """The mock pipeline, regardless of AI_PROVIDER in backend/.env."""

    return AnalysisOrchestrator(
        MockEvidenceRetriever(),
        MockLLMClient(),
        MockImagingStager(),
        max_candidates=settings.AI_MAX_CANDIDATES,
        evidence_per_candidate=settings.AI_EVIDENCE_PER_CANDIDATE,
    )


def build_services(storage: LocalScanStorage) -> Services:
    # Mirrors app/api/dependencies.py, except for the pinned mock orchestrator.
    patient_service = PatientService(PatientRepository(), UserRepository())
    visit_service = VisitService(VisitRepository(), SymptomRepository(), patient_service)
    return Services(
        patients=patient_service,
        visits=visit_service,
        scans=ScanService(
            ScanRepository(),
            visit_service,
            storage,
            max_size_bytes=settings.MAX_SCAN_SIZE_BYTES,
        ),
        analyses=AnalysisService(
            AnalysisRepository(), visit_service, patient_service, mock_orchestrator()
        ),
        triage=TriageService(patient_service, AnalysisRepository()),
    )


# -- reset ---------------------------------------------------------------


def reset(db: Session, storage: LocalScanStorage) -> int:
    """Delete everything owned by the demo usernames. Returns users removed.

    ORM deletes rather than bulk deletes, so the relationship cascades
    (findings -> evidence, patient -> visits -> symptoms/scan, phones) run.
    Soft-deleted rows are included: they still hold foreign keys.
    """

    usernames = [clinician.username for clinician in CLINICIANS]
    users = db.scalars(select(User).where(User.username.in_(usernames))).all()
    if not users:
        return 0

    user_ids = [user.id for user in users]
    patient_ids = select(Patient.id).where(Patient.doctor_id.in_(user_ids))
    visit_ids = select(Visit.id).where(Visit.patient_id.in_(patient_ids))
    analysis_ids = select(Analysis.id).where(Analysis.visit_id.in_(visit_ids))

    storage_keys = list(
        db.scalars(select(Scan.storage_key).where(Scan.visit_id.in_(visit_ids)))
    )

    for model, clause in (
        (Report, Report.analysis_id.in_(analysis_ids)),
        (Analysis, Analysis.id.in_(analysis_ids)),
        (Patient, Patient.id.in_(patient_ids)),
    ):
        for row in db.scalars(select(model).where(clause)).all():
            db.delete(row)
        db.flush()

    for user in users:
        db.delete(user)
    db.commit()

    # Files last: a failed transaction above must not leave rows pointing at
    # scans that no longer exist.
    for key in storage_keys:
        storage.delete(key)

    return len(users)


# -- seed ----------------------------------------------------------------


def _seed_patient(
    db: Session,
    services: Services,
    clinician: User,
    spec: DemoPatient,
    now: datetime,
) -> Patient:
    patient = Patient(
        doctor_id=clinician.id,
        first_name=spec.first_name,
        last_name=spec.last_name,
        gender=spec.gender,
        dob=spec.dob,
        email=f"demo-patient-{spec.key.lower()}@example.com",
        address="1 Example Street",
        blood_group="O+",
        allergies=[],
        emergency_contact="5550000000",
        phone=[PhoneNumber(phone_number="5551110000")],
    )
    db.add(patient)
    db.commit()

    # Visit by visit, analysing each before the next exists: the pipeline
    # reads every other visit as history, so a visit analysed after a later
    # one was recorded would trend against its own future.
    for index, spec_visit in enumerate(spec.visits):
        visit = Visit(
            patient_id=patient.id,
            visit_date=now - timedelta(days=spec_visit.days_ago),
            chief_complaint=spec_visit.complaint,
            history="Synthetic demo history. No acute events reported.",
            vitals={"heart_rate": 74, "bp_systolic": 128, "bp_diastolic": 82},
            notes=None,
            status=VisitStatus.SUBMITTED,
            symptoms=[
                Symptom(
                    symptom_name=symptom.name,
                    severity=symptom.severity,
                    duration_days=30,
                    onset=symptom.onset,
                )
                for symptom in spec_visit.symptoms
            ],
        )
        db.add(visit)
        db.commit()

        services.scans.upload_scan(
            db,
            visit.id,
            clinician,
            filename=f"demo-{spec.key.lower()}-visit{index + 1}.nii",
            content_type=SCAN_CONTENT_TYPE,
            content=synthetic_scan(f"{spec.key}-{index + 1}", spec_visit.stage),
        )

        if not spec_visit.analyse:
            continue

        analysis = services.analyses.analyze_visit(db, visit.id, clinician)
        if spec_visit.sign_off:
            services.analyses.sign_off_analysis(db, analysis.id, clinician)

    return patient


def seed(db: Session, storage: LocalScanStorage) -> list[tuple[DemoClinician, User]]:
    services = build_services(storage)
    now = datetime.now(timezone.utc)
    seeded = []

    for spec in CLINICIANS:
        clinician = User(
            username=spec.username,
            email=f"{spec.username}@example.com",
            first_name=spec.first_name,
            last_name=spec.last_name,
            hashed_password=hash_password(DEMO_PASSWORD),
            role=UserRole.CLINICIAN,
            is_active=True,
            is_verified=True,
        )
        db.add(clinician)
        db.commit()

        for patient_spec in spec.patients:
            _seed_patient(db, services, clinician, patient_spec, now)

        seeded.append((spec, clinician))

    return seeded


def _flag_line(early_watch: bool, worsening: bool, sign_off: bool) -> str:
    names = [
        name
        for name, on in (
            ("early_watch", early_watch),
            ("worsening", worsening),
            ("awaiting sign-off", sign_off),
        )
        if on
    ]
    return ", ".join(names) or "no open signals"


def report_queue(db: Session, storage: LocalScanStorage, seeded) -> bool:
    """Print each clinician's actual queue; return False on any surprise."""

    services = build_services(storage)
    all_match = True

    for spec, clinician in seeded:
        expected = {
            f"{p.first_name} {p.last_name}": p.expected for p in spec.patients
        }
        entries, _ = services.triage.list_queue(db, clinician)

        print(f"\n  {spec.username} / {DEMO_PASSWORD}")
        for position, entry in enumerate(entries, start=1):
            name = f"{entry.patient_first_name} {entry.patient_last_name}"
            actual = Flags(
                early_watch=entry.has_open_early_watch,
                worsening=entry.has_worsening_trend,
                sign_off=entry.awaiting_sign_off,
            )
            marker = ""
            if expected.get(name) != actual:
                all_match = False
                marker = "   <-- differs from the scenario"
            print(
                f"    {position}. {name:<16} "
                f"{_flag_line(actual.early_watch, actual.worsening, actual.sign_off)}"
                f"{marker}"
            )

    return all_match


def main() -> None:
    storage = LocalScanStorage(settings.SCAN_STORAGE_DIR)

    with SessionLocal() as db:
        removed = reset(db, storage)
        seeded = seed(db, storage)

        print("Seeded the ADR-006 demo panel (synthetic data, mock providers).")
        if removed:
            print(f"  Replaced {removed} existing demo account(s).")
        print("\nTriage queue, as the API ranks it:")
        all_match = report_queue(db, storage, seeded)

    print(
        "\n  Grace Adeyemi's latest visit is unanalysed -- run it from the UI "
        "to watch her move up the queue."
    )
    if not all_match:
        print("\nWARNING: the queue does not match the scenario definitions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
