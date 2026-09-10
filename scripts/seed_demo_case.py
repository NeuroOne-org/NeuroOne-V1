"""Seed a demo patient whose history contains a multi-visit trend.

AGENTS.md section 8.1 requires the mock pipeline to be able to surface an
``early_watch`` flag with something real to point at. That is a property of the
DATA, not of the provider -- a patient with no history correctly produces no
early-watch flag. This script creates the case that satisfies it.

The shape is deliberate:

  * the presenting complaint (tremor 3 -> 5 -> 8) worsens loudly and lands in
    the differential, and
  * a second signal (memory loss 2 -> 3 -> 4) worsens quietly and is flagged
    early_watch, traced back to these visits.

That contrast is the feature being demonstrated.

Synthetic data only -- per AGENTS.md section 12 the demo environment must not
hold real patient records.

Usage:
    python scripts/seed_demo_case.py
"""

import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.models.patient import Patient, PhoneNumber  # noqa: E402
from app.models.symptom import Symptom  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.models.visit import Visit, VisitStatus  # noqa: E402


DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "DemoClinician!2026")

# (days_offset, tremor severity, memory-loss severity)
VISIT_SERIES = (
    (0, 3, 2),
    (120, 5, 3),
    (240, 8, 4),
)


def seed(db) -> dict:
    suffix = uuid4().hex[:6]
    first_visit = datetime.now(timezone.utc) - timedelta(days=260)

    clinician = User(
        username=f"demo-clinician-{suffix}",
        email=f"demo-clinician-{suffix}@example.com",
        first_name="Demo",
        last_name="Clinician",
        hashed_password=hash_password(DEMO_PASSWORD),
        role=UserRole.CLINICIAN,
        is_active=True,
        is_verified=True,
    )
    db.add(clinician)
    db.commit()

    patient = Patient(
        doctor_id=clinician.id,
        first_name="Demo",
        last_name="Patient",
        gender="F",
        dob=date(1962, 4, 9),
        email=f"demo-patient-{suffix}@example.com",
        address="1 Example Street",
        blood_group="O+",
        allergies=[],
        emergency_contact="5550000000",
        phone=[PhoneNumber(phone_number="5551110000")],
    )
    db.add(patient)
    db.commit()

    visits = []
    for offset, tremor, memory in VISIT_SERIES:
        visit = Visit(
            patient_id=patient.id,
            visit_date=first_visit + timedelta(days=offset),
            chief_complaint="intermittent hand tremor",
            history="Gradual onset, no acute events reported.",
            vitals={"heart_rate": 74, "bp_systolic": 128, "bp_diastolic": 82},
            notes=None,
            status=VisitStatus.SUBMITTED,
            symptoms=[
                Symptom(
                    symptom_name="tremor",
                    severity=tremor,
                    duration_days=30 + offset,
                    onset="gradual",
                ),
                Symptom(
                    symptom_name="memory loss",
                    severity=memory,
                    duration_days=30 + offset,
                    onset="insidious",
                ),
            ],
        )
        db.add(visit)
        visits.append(visit)

    db.commit()

    return {
        "username": clinician.username,
        "password": DEMO_PASSWORD,
        "patient_id": patient.id,
        "visit_ids": [visit.id for visit in visits],
    }


def main() -> None:
    with SessionLocal() as db:
        seeded = seed(db)

    print("Seeded demo case (synthetic data).")
    print(f"  clinician : {seeded['username']}")
    print(f"  password  : {seeded['password']}")
    print(f"  patient   : {seeded['patient_id']}")
    for index, visit_id in enumerate(seeded["visit_ids"]):
        offset, tremor, memory = VISIT_SERIES[index]
        print(
            f"  visit {index + 1}   : {visit_id}  "
            f"(tremor {tremor}, memory loss {memory})"
        )
    print()
    print("Trigger analysis on the latest visit:")
    print(f"  POST /api/v1/visits/{seeded['visit_ids'][-1]}/analyses")


if __name__ == "__main__":
    main()
