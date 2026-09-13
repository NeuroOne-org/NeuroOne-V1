---
type: "query"
date: "2026-09-12T22:15:12.991967+00:00"
question: "audit and understant\\ help me build a handbook so that i could remember every detail of the project using claude code or codex\\ i have been using graphify thus context of project, chats, decision is stored in graphify-out/\\ this handbook is supposed to help me learn so that i do not mess up the presentation i have"
contributor: "graphify"
outcome: "useful"
source_nodes: ["AnalysisOrchestrator", "DiagnosisCandidate", "MRI as a Primary Input With Symptoms as Context", "ReportService", "Current Development Status Table"]
---

# Q: audit and understant\ help me build a handbook so that i could remember every detail of the project using claude code or codex\ i have been using graphify thus context of project, chats, decision is stored in graphify-out/\ this handbook is supposed to help me learn so that i do not mess up the presentation i have

## Answer

Expanded from original query via graph vocabulary: [architecture, clinical, decision, demo, evidence, history, llm, mri, provider, report, review]. Queried root graph first, then inspected current source and product documents to audit NeuroONE for a professor-facing team project report. Handbook baseline is 5d391b1, 2026-09-13.

Created docs/handbook/README.md, PROJECT-HANDBOOK.md, PROFESSOR-PRESENTATION.md, STUDY-WITH-AI.md, AUDIT.md and PLAN.md. Start at README for study/navigation, professor guide for narration/demo/Q&A, and STUDY-WITH-AI for grounded Claude Code/Codex tutoring. AUDIT records source conflicts and verification limits. All 151 local handbook links resolved.

Current app OpenAPI under synthetic test configuration has 35 /api/v1 operations. There are 13 migration files and 10 mapped tables. Full existing backend suite passed: 414 tests, after replacing the sandbox-denied default tmp_path directory with a fresh permitted basetemp. Frontend has clinical endpoint wrappers and real page/hook callers, six test files and a frontend CI definition. Old README/progress report says unconnected frontend and no frontend tests; those historical statements are stale. Local frontend dependencies were absent, so this audit did not execute frontend checks or the browser journey.

Source-verified limitations: MockImagingStager hashes a checksum and reads no image anatomy. MockEvidenceRetriever uses synthetic fixtures; registry always returns it. ADR-007 is Proposed and the merged AI-02b work is a plan/decision record, not a live retriever implementation. LiveLLMClient._render_case omits ReasoningRequest imaging/scan_trend and scan metadata. rank_candidates sorts confidence/name, so required stage-first rank is not guaranteed (synthetic counterexample: Parkinsonian syndrome 0.83 above Cognitively normal 0.7444). ReportSnapshot lacks reviewer/time although analysis stores sign-off and report generation is gated. No amendment API/editor exists. Review allows authorized active admins as well as clinicians.

Further source observations: new-patient intake sends no structured symptoms and retries creation after partial failure; follow-up captures symptom name/severity/onset but not duration/observation. History excludes current id but not later visit dates and takes oldest other visits by default. Report snapshot takes current source inputs at report-generation time rather than analysis context time. Compose lacks required Gmail settings and scan mounting. OTP uses process-local state. Scan upload does not parse MRI geometry and saves empty dimensions. See AUDIT for details and source pointers before proposing fixes.

Current root graph built_at_commit is 7c1308ee, with 2875 nodes/6754 links; 2026-09-13 snapshot is older at 9ab89749. Neither indexes ADR-007. Only two prior query memory files were found, not a complete chat archive. No graph rebuild was performed. This memory retains the verified audit outcome, not authoritative product decisions.

The professor report should distinguish implemented, verified, simulated, proposed and unverified. Do not convert confidence/0.92 ceiling into clinical accuracy, fixture citations into reviewed literature, or synthetic stage-region values into measured explainability. Keep clinician-assist framing. Synthetic demo data remains a flagged assumption in governing scope documents. No live database reset, external model call, email or application code change was performed. Future fixes need their own repository plan/decision cycle.

## Outcome

- Signal: useful

## Source Nodes

- AnalysisOrchestrator
- DiagnosisCandidate
- MRI as a Primary Input With Symptoms as Context
- ReportService
- Current Development Status Table

## PR preparation follow-up — 2026-09-13

Baseline advanced from 5d391b1 to a01ae83 (PR #41). Updated the handbook auth/configuration and upstream graph metadata. Full backend suite: 437 passed in 7.68 seconds. OTP is enforced by default, production refuses disabled OTP, login/reset OTP purpose keys are isolated, and auth endpoints now use process-local rate limits. Gmail configuration is conditional on email delivery; console delivery is for local synthetic-data rehearsal. Upstream root graph now has 3,041 nodes and 7,116 links, includes ADR-007, and records build commit 5d391b1, still older than the auth update. Historical audit findings remain dated rather than silently rewritten. No application code changed.
