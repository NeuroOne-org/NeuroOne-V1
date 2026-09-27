"""Ingestion policy for the curated retrieval corpus (ADR-007).

Every constant here is enforced more than once downstream: tier by the
`corpus_documents` CHECK constraint and again by the retriever's own
re-filter; licence at ingestion only, since it is not part of the wire
contract. Widening either list is a one-line change and a recorded decision
(ADR-007 "Why"), not a silent edit.
"""

import re


ALLOWED_TIERS = frozenset({"guideline", "systematic_review"})

ALLOWED_LICENSES = frozenset({"CC0-1.0", "CC-BY-4.0", "public-domain"})

MAX_PASSAGE_CHARS = 2000

# Tripwires, not a guarantee (ADR-007 Risks: "incomplete by nature"). A match
# sends the file back to the human reviewer instead of being silently
# stripped, which would hide from them the very thing they should see.
INJECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "role-marker",
        re.compile(r"(?im)^\s*(system|assistant|user)\s*:"),
    ),
    (
        "ignore-instructions",
        re.compile(
            r"(?i)\b(ignore|disregard)\b[^.\n]{0,40}\b(previous|prior|above|all)\b"
            r"[^.\n]{0,40}\b(instructions?|prompt|rules?)\b"
        ),
    ),
    (
        "chat-template-token",
        re.compile(r"<\|[a-zA-Z_]+\|>|\[/?(?:INST|SYS)\]|<<SYS>>|<</SYS>>"),
    ),
    (
        "fenced-code",
        re.compile(r"```"),
    ),
)


__all__ = [
    "ALLOWED_LICENSES",
    "ALLOWED_TIERS",
    "INJECTION_PATTERNS",
    "MAX_PASSAGE_CHARS",
]
