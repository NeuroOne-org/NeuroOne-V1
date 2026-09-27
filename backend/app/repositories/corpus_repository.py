"""SQL for the curated retrieval corpus (ADR-007, AI-02b-4).

Every statement here is a bound parameter; no clinician text and no corpus
text is ever concatenated into SQL (a hostile-complaint test in the
Postgres suite covers this). `app/ai/` never imports this module directly
-- `app/services/corpus_search.py` adapts it to the `CorpusSearch` protocol
declared in `app/ai/providers/base.py` (ADR-007 decision 5, AGENTS.md
section 7: SQL only in the repository layer).

Exercised for real only by the Postgres-marked test suite
(`tests/postgres/test_corpus_repository.py`): `ts_rank_cd`, `plainto_tsquery`
and the generated `search_vector` column do not exist on SQLite.
"""

from dataclasses import dataclass

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.ai.corpus.source_schema import CorpusManifest, CorpusSourceFile, content_sha256
from app.ai.providers.base import CorpusHit, CorpusSearchTerms
from app.models.corpus import CorpusDocument


# Clinician text is unbounded; the retriever already caps each field at 20
# tokens (AI-02b-5), and this cap is a second, independent bound on the SQL
# side so the query shape never depends on retriever behavior alone.
_MAX_QUERY_TERMS = 20


def _tsquery_fragment(terms: tuple[str, ...], *, prefix: str, params: dict[str, object]) -> str:
    """SQL for `plainto_tsquery(term_0) || plainto_tsquery(term_1) || ...`.

    OR-combines one `plainto_tsquery` call per term -- "any of these
    condition names" -- rather than a single call over all terms, which
    would AND them together instead. An empty group becomes `''::tsquery`,
    a valid Postgres literal that matches nothing (ADR-007 section 10).

    Every term becomes a named bind parameter; the returned string is SQL
    *shape* (repeated `:cond0`, `:cond1`, ... placeholders), never term text,
    so building it with an f-string does not reintroduce string-built SQL.
    """

    capped = terms[:_MAX_QUERY_TERMS]
    if not capped:
        return "''::tsquery"

    pieces = []
    for index, term in enumerate(capped):
        key = f"{prefix}{index}"
        params[key] = term
        pieces.append(f"plainto_tsquery('english', :{key})")
    return " || ".join(pieces)


@dataclass(frozen=True)
class ReplaceVersionResult:
    """Counts reported by `replace_version`, never passage text (section 12)."""

    inserted: int
    unchanged: int
    deactivated: int


class CorpusRepository:
    """Search and versioned replace for `corpus_documents`."""

    def search(
        self,
        db: Session,
        terms: CorpusSearchTerms,
        *,
        tiers: frozenset[str],
        limit: int,
    ) -> list[CorpusHit]:
        """Return active, in-policy rows ranked by relevance, most relevant first.

        Ranking mirrors the mock retriever's weights (ADR-007 decision 6):
        0.5 * condition match + 0.3 * symptom match + 0.2 * complaint match,
        via `ts_rank_cd` against the generated `search_vector` column.
        """

        params: dict[str, object] = {}
        q_cond = _tsquery_fragment(terms.conditions, prefix="cond", params=params)
        q_sym = _tsquery_fragment(terms.symptoms, prefix="sym", params=params)
        q_cmp = _tsquery_fragment(terms.complaint_terms, prefix="cmp", params=params)

        params["tiers"] = list(tiers)
        params["result_limit"] = limit

        statement = text(
            f"""
            SELECT document_id, chunk_id, source, citation, relevant_passage,
                   source_url, source_tier, published_year, keywords,
                   (0.5 * ts_rank_cd(search_vector, {q_cond})
                  + 0.3 * ts_rank_cd(search_vector, {q_sym})
                  + 0.2 * ts_rank_cd(search_vector, {q_cmp})) AS rank
            FROM corpus_documents
            WHERE is_active
              AND source_tier = ANY(:tiers)
              AND search_vector @@ ({q_cond} || {q_sym} || {q_cmp})
            ORDER BY rank DESC, document_id, chunk_id
            LIMIT :result_limit
            """
        )

        rows = db.execute(statement, params).mappings().all()

        return [
            CorpusHit(
                document_id=row["document_id"],
                chunk_id=row["chunk_id"],
                source=row["source"],
                citation=row["citation"],
                relevant_passage=row["relevant_passage"],
                source_url=row["source_url"],
                source_tier=row["source_tier"],
                published_year=row["published_year"],
                keywords=tuple(
                    keyword for keyword in row["keywords"].split(";") if keyword
                ),
                rank=float(row["rank"] or 0.0),
            )
            for row in rows
        ]

    def replace_version(
        self,
        db: Session,
        manifest: CorpusManifest,
        files: list[CorpusSourceFile],
    ) -> ReplaceVersionResult:
        """Upsert every passage in `files`, then activate this version and
        deactivate every other version, all in one transaction.

        Upsert key is `(document_id, chunk_id)`. A passage whose
        `content_sha256` is unchanged from what is stored is left alone
        apart from being marked active, so a re-run of an unchanged manifest
        reports every row as `unchanged` (AI-02b-7's idempotence
        requirement).
        """

        inserted = 0
        unchanged = 0

        try:
            for source_file in files:
                for passage in source_file.passages:
                    digest = content_sha256(passage.text)
                    existing = db.scalar(
                        select(CorpusDocument).where(
                            CorpusDocument.document_id == source_file.document_id,
                            CorpusDocument.chunk_id == passage.chunk_id,
                        )
                    )

                    if existing is not None and existing.content_sha256 == digest:
                        existing.is_active = True
                        unchanged += 1
                        continue

                    if existing is None:
                        existing = CorpusDocument(
                            document_id=source_file.document_id,
                            chunk_id=passage.chunk_id,
                        )
                        db.add(existing)
                        inserted += 1

                    existing.source = source_file.source
                    existing.citation = source_file.citation
                    existing.relevant_passage = passage.text
                    existing.source_url = source_file.source_url
                    existing.source_tier = source_file.source_tier
                    existing.published_year = source_file.published_year
                    existing.keywords = ";".join(source_file.keywords)
                    existing.corpus_version = manifest.corpus_version
                    existing.content_sha256 = digest
                    existing.license = source_file.license
                    existing.reviewed_by = source_file.reviewed_by
                    existing.reviewed_at = source_file.reviewed_at
                    existing.is_active = True

                db.flush()

            deactivated = (
                db.query(CorpusDocument)
                .filter(CorpusDocument.corpus_version != manifest.corpus_version)
                .filter(CorpusDocument.is_active.is_(True))
                .update({"is_active": False}, synchronize_session=False)
            )

            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

        return ReplaceVersionResult(
            inserted=inserted, unchanged=unchanged, deactivated=deactivated
        )


__all__ = ["CorpusRepository", "ReplaceVersionResult"]
