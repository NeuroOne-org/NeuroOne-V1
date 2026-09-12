# Handbook authoring plan

MODE: PLAN

Date: 2026-09-13. User-authorized deliverable: audit and create a learning handbook for a professor-facing team project report. This plan governs documentation authoring only.

## 1. Objective

Explain how NeuroONE works, what the team has implemented, what remains, and how to rehearse accurate answers using Claude Code or Codex.

## 2. Current State

Inspected checkout: `5d391b1`. Backend has 35 versioned API operations and 13 migration files. Current frontend contains clinical endpoint calls and six test files. Root Graphify graph predates HEAD and does not index ADR-007. Detailed findings go in `AUDIT.md`.

## 3. Relevant Requirements

PRD FR-01–FR-08, current PRD §8 journey, clinical safety boundary, APP-FLOW, TRD, scope decisions, ADR-001–ADR-007, and repository inspection rules.

## 4. Questions / Resolved Decisions

Audience confirmed by user: professor reviewing how the project works, completed work and remaining work. Format: portable Markdown for both coding agents. Presentation duration unspecified, so provide a five-minute core with expandable technical Q&A.

## 5. Assumptions

Readers need plain explanations plus code pointers. Demo data remains a flagged synthetic-data assumption in governing documents. No clinical efficacy claims or external medical advice are necessary.

## 6. Scope

Learning entry point, comprehensive project reference, professor presentation and demo guide, AI tutoring prompts, dated audit, source links and factual verification.

## 7. Out of Scope

Production fixes, schema changes, dependency installation, deployment, resetting demo data, editing the existing presentation, approving ADR-007, and reconciling disputed product behavior.

## 8. Architecture Impact

N/A: app architecture remains unchanged. The handbook describes it and flags deviations.

## 9. Design Options

One long document is searchable but difficult to rehearse. A deck alone omits engineering detail and is less useful to coding agents. A linked Markdown handbook with a short presentation guide supports both depth and recall.

## 10. Recommended Design

`README.md` as study entry point, `PROJECT-HANDBOOK.md` as detailed reference, `PROFESSOR-PRESENTATION.md` for narration/demo/Q&A, `STUDY-WITH-AI.md` for repeatable learning, and `AUDIT.md` for evidence and limitations.

## 11. Data / Schema Impact

N/A: no application data or schema changes. Documents must distinguish source records, reasoning snapshots, and simulated fixture literature.

## 12. API / Contract Impact

N/A: no contract changes. Describe observed routes and wire shapes, including absent amendment and reviewer-in-PDF behavior.

## 13. AI / RAG Impact

No provider changes. Explain three provider seams, deterministic mocks, live reasoning capability, citation resolution and proposed retrieval work. Save a concise audit memory through Graphify's supported CLI.

## 14. Security / Privacy Impact

Do not read or reproduce real credentials. Use public example configuration and synthetic fixture descriptions. Do not seed or modify a running database. Explain security mechanisms without asserting production readiness.

## 15. Clinical Safety Impact

Every learning aid uses clinician-assist framing. Distinguish model likelihood from measured accuracy. State that simulated staging does not interpret image anatomy and fixture citations are not verified literature.

## 16. Failure / Recovery Behavior

Record verification failures honestly. Retest environment-dependent failures in a permitted temporary directory. If source documents conflict, record exact sections and recommended reconciliation without implementing the disputed behavior.

## 17. Implementation Tasks

### TASK REPORT-HB-01 — Evidence audit

**Goal:** establish presentation facts. **Why:** stale records can mislead the presenter. **Dependencies:** relevant source documents and existing graph. **Files / Components:** Graphify reports/memory, ADRs, backend/frontend contracts, tests, Compose, existing PPTX. **Implementation:** query graph, inspect current code, run backend tests, inspect slide text, probe critical discrepancies. **Contracts:** no changes. **Failure Cases:** stale graph, image-only slide content, unavailable frontend dependencies, sandbox temp permissions. **Tests:** full existing backend suite and small isolated probes. **Documentation:** `AUDIT.md`. **Definition of Done:** dated claims have sources and verification limits.

### TASK REPORT-HB-02 — Author and verify learning aids

**Goal:** help the user explain and recall the project. **Why:** a technical inventory alone does not support presentation practice. **Dependencies:** REPORT-HB-01. **Files / Components:** the five linked learning documents in this folder. **Implementation:** write layered explanations, decisions, progress matrix, demo script, likely professor questions, active-recall prompts and update workflow. **Contracts:** no changes. **Failure Cases:** overstated readiness, unsupported medical claims, broken links, prompts encouraging unauthorized fixes. **Tests:** verify local links and Markdown structure, cross-check repeated facts. **Documentation:** these files and this plan. **Definition of Done:** another reader can explain the current implementation and limitations, and launch a grounded tutoring session.

## 18. Task Dependencies

Evidence audit precedes factual authoring. Link/content verification follows authoring. Graphify session memory follows final verified findings.

## 19. Testing Strategy

Run existing backend pytest suite under synthetic test configuration. Inspect frontend tests and CI, but do not claim they passed locally without execution. Validate document links and source claims. Browser walkthrough, full PostgreSQL migration execution and PPT visual audit remain explicitly unperformed.

## 20. Acceptance Criteria

Handbook covers product, current PRD journey, stack, layers, entities, contracts, providers, trends, provenance, authorization, reports, ADR rationale, verified progress and remaining work. Short guide includes professor narration, team handoffs, demo recovery and Q&A. Tutoring prompts require source-backed correction and preserve unknowns.

## 21. Documentation Updates

Create only `docs/handbook/` documents and one supported Graphify memory record. Existing sources of truth and the PPTX remain available as audited sources.

## 22. Risks / Open Issues

Presentation time and actual team responsibilities are unknown. Main risks are stale documentation, unverified UI execution, absent live imaging integration, unguaranteed stage-first ranking, missing reviewer details in PDFs and incomplete retrieval implementation.

## Authoring result

Documentation tasks completed. Created the five linked learning/audit documents plus this plan. Original backend validation: 414 tests passed. PR preparation fast-forwarded to `a01ae83`, refreshed auth/configuration and upstream graph metadata, and reran the suite: 437 tests passed in 7.68 seconds. Document validation: 151 local links resolved and code fences paired. Frontend execution, live PostgreSQL verification and visual slide inspection remain disclosed limitations. No production implementation was performed.

## 23. Build Readiness

The user's request explicitly authorizes authoring the handbook. No unresolved decision prevents this documentation work. Production fixes need their own plan.

BUILD READY
