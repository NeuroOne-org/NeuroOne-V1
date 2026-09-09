"""Create NeuroONE's first administrator without a public endpoint."""

from getpass import getpass
import os
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.api.dependencies import get_auth_service, get_user_service  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.models.user import UserRole  # noqa: E402
from app.schemas.user import UserCreate  # noqa: E402
from app.utils.exceptions import UserAlreadyExistsError  # noqa: E402


def _value(name: str, prompt: str, *, secret: bool = False) -> str:
    value = os.getenv(name)
    if value:
        return value
    return getpass(prompt) if secret else input(prompt).strip()


def main() -> int:
    payload = UserCreate(
        email=_value("NEUROONE_ADMIN_EMAIL", "Admin email: "),
        username=_value("NEUROONE_ADMIN_USERNAME", "Admin username: "),
        password=_value("NEUROONE_ADMIN_PASSWORD", "Admin password: ", secret=True),
        first_name=_value("NEUROONE_ADMIN_FIRST_NAME", "First name: "),
        last_name=_value("NEUROONE_ADMIN_LAST_NAME", "Last name: "),
        role=UserRole.ADMIN,
    )

    with SessionLocal() as db:
        try:
            admin = get_auth_service(get_user_service()).bootstrap_admin(db, payload)
        except UserAlreadyExistsError:
            print("An administrator already exists; no account was created.")
            return 0

    print(f"Administrator created: {admin.email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
