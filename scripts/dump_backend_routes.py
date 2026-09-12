"""Regenerate backend-routes.json from the live FastAPI application.

The file is the OpenAPI schema, committed at the repository root so the API
contract is reviewable in a diff and readable without running the server.

It was previously produced by hand, which is why it drifted: by the time the
ADR-006 work merged it was missing scan intake, clinician sign-off, the triage
queue and the entire OTP/password-reset surface -- seven paths that existed in
code and were absent from the document people were reading as the contract.

Run this after any change to a router, schema or response model:

    python scripts/dump_backend_routes.py

Output is sorted and two-space indented so the diff shows what actually
changed rather than a reordering.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
OUTPUT = REPO_ROOT / "backend-routes.json"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402


def main() -> None:
    schema = app.openapi()
    rendered = json.dumps(schema, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)}: {len(schema['paths'])} paths")


if __name__ == "__main__":
    main()
