"""Ingest source documents into the curated retrieval corpus (ADR-007).

Validates every file listed in the manifest before writing anything; only
if every file passes does it load them in one transaction
(`CorpusRepository.replace_version`), which activates the manifest's
`corpus_version` and deactivates every other version. Never prints passage
text (AGENTS.md section 12) -- only counts and file paths.

Usage:
    python scripts/ingest_documents.py --dry-run
    python scripts/ingest_documents.py

See backend/corpus/pending/README.md for the human review gate this CLI
assumes already happened: it only ever reads backend/corpus/documents/,
never backend/corpus/pending/.
"""

import argparse
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.ai.corpus.source_schema import (  # noqa: E402
    CorpusSourceError,
    load_manifest,
    load_source_file,
)
from app.core.database import SessionLocal  # noqa: E402
from app.repositories.corpus_repository import CorpusRepository  # noqa: E402


DEFAULT_MANIFEST = BACKEND_DIR / "corpus" / "manifest.yaml"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to manifest.yaml (default: backend/corpus/manifest.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate every listed file and report errors; write nothing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest_path = args.manifest.resolve()
    documents_dir = manifest_path.parent / "documents"

    try:
        manifest = load_manifest(manifest_path)
    except CorpusSourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    files = []
    errors = []
    for filename in manifest.files:
        file_path = documents_dir / filename
        try:
            files.append(load_source_file(file_path, documents_dir=documents_dir))
        except CorpusSourceError as exc:
            errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(
            f"{len(errors)} file(s) failed validation; nothing was written.",
            file=sys.stderr,
        )
        return 1

    print(
        f"Validated {len(files)} file(s) for corpus_version="
        f"{manifest.corpus_version!r}."
    )

    if args.dry_run:
        print("Dry run: nothing written.")
        return 0

    repository = CorpusRepository()
    try:
        with SessionLocal() as db:
            result = repository.replace_version(db, manifest, files)
    except Exception as exc:  # noqa: BLE001 -- reported to the operator, not raised
        print(f"error: ingestion failed and was rolled back: {exc}", file=sys.stderr)
        return 2

    print(
        f"Ingested corpus_version={manifest.corpus_version!r}: "
        f"{result.inserted} inserted, {result.unchanged} unchanged, "
        f"{result.deactivated} deactivated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
