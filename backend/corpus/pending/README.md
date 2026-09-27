# `pending/` — candidate corpus sources, not yet reviewed

This directory is the landing zone for candidate source documents before a
human has reviewed them. **Nothing here is ever loaded.**
`app/ai/corpus/source_schema.load_source_file` refuses any path that does
not resolve under `backend/corpus/documents/`, and
`scripts/ingest_documents.py` only reads `backend/corpus/manifest.yaml`,
which in turn only lists files under `documents/`.

Today, files land here by hand. Later, an automated PubMed refresh (ADR-007
Options Considered, option C) can write candidate files here in exactly the
same source-file shape (`app/ai/corpus/source_schema.py`) without any code
change to the review gate below — that is the whole point of building A to
grow into C.

## The review gate

A human:

1. Reads the candidate file's `citation`, `source_url`, `source_tier` and
   `license` and confirms they are accurate.
2. Confirms `source_tier` is `guideline` or `systematic_review` and `license`
   is one of `CC0-1.0`, `CC-BY-4.0`, `public-domain` (ADR-007 decision 3–4).
3. Reads every `passages[].text` **verbatim against the original source**
   and confirms it is quoted accurately, not paraphrased or model-generated.
4. Fills in `reviewed_by` (their name or initials) and `reviewed_at` (today's
   date).
5. Moves the file to `backend/corpus/documents/` and adds its filename to
   `backend/corpus/manifest.yaml`'s `files` list.

Only then can `scripts/ingest_documents.py` load it. A file left in
`pending/` with `reviewed_by` already filled in is still refused — the
directory the file lives in is what the loader checks, not the field
values inside it.

## Running ingestion

```bash
python scripts/ingest_documents.py --manifest backend/corpus/manifest.yaml --dry-run
python scripts/ingest_documents.py --manifest backend/corpus/manifest.yaml
```

`--dry-run` validates every listed file and reports errors without writing
anything. Without it, a single transaction activates the manifest's
`corpus_version` and deactivates every other version. See
`docs/AI-02b-retrieval-corpus-plan.md` §16 for the full failure-mode table.
