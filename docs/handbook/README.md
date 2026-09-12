# NeuroONE learning and presentation handbook

Prepared for your professor-facing team project report. Audited on **13 September 2026**, against checkout **`a01ae83`**. The original audit used `5d391b1`; PR preparation refreshed auth, graph metadata and backend tests against `a01ae83`. Historical findings remain dated in the audit. This is a learning reference, not a new product specification.

## Start here

Your aim is to explain the project accurately, including its unfinished parts. You do not need to memorize every filename. Learn the product story and the data flow first. Use the detailed reference when someone asks how a particular part works.

| Document | Use it for |
|---|---|
| [Project handbook](PROJECT-HANDBOOK.md) | Learn the product, architecture, database, AI pipeline, decisions and roadmap |
| [Professor presentation guide](PROFESSOR-PRESENTATION.md) | Rehearse the talk, divide team sections, walk through the demo and answer questions |
| [Study with Claude Code or Codex](STUDY-WITH-AI.md) | Launch a tutor, practice active recall and maintain your knowledge |
| [Dated audit](AUDIT.md) | Check evidence, contradictions, verification results and unfinished work |
| [Authoring plan](PLAN.md) | Understand the scope and validation of this handbook |

## The explanation to remember

> NeuroONE is a clinical decision-support project for neurological evaluation. It organizes patient visits, MRI scan intake and structured clinical information, then produces ranked possibilities with findings, reasoning and citations. It compares a patient's visits to surface changes worth reviewing. A clinician signs off before generating a PDF. The application workflow is implemented in the backend and the current frontend has been wired to clinical endpoints. Literature retrieval and MRI staging are simulated, while reasoning has both a deterministic mock and a configurable live LLM provider. We still need to close integration gaps, implement reviewed literature retrieval and validate the real imaging component.

The last sentence is part of your explanation, not something to hide until asked.

## Seven facts you should know without notes

1. **Purpose:** support clinicians evaluating neurological cases. Clinical responsibility stays with the clinician.
2. **Unit of clinical work:** a visit belonging to a patient. Each visit can carry symptoms and one scan.
3. **Journey:** login, patient, visit with scan and symptoms, analysis, ranked differential and evidence, review/sign-off, PDF.
4. **Backend layers:** client, API, service, repository, PostgreSQL. The AI orchestrator produces structured results; the service persists them.
5. **AI has three components:** retrieval, reasoning and imaging staging. They can have different provenance.
6. **Current evidence:** 35 versioned API operations, 13 migration files, 437 backend tests passed in this audit. Frontend tests and CI exist, but this audit did not execute them locally.
7. **Current limits:** MRI staging uses checksums rather than anatomy, retrieval uses fixture passages, live reasoning currently omits imaging results, and a full browser demo was not verified by this audit.

## Your learning route

| Time available | What to do |
|---|---|
| 10 minutes | Read this page and the opening script in the presentation guide. Explain the three simulated/live components aloud. |
| 30 minutes | Add handbook sections 1–5, 8–11 and 14. Answer the first ten professor questions without reading. |
| 60 minutes | Read the full handbook. Draw the ownership chain and AI pipeline from memory. Rehearse the seeded demo and its disclosures. |
| Several days | Use the tutor prompt for one topic per session. Keep an error log and rehearse the entire report with your team. |

After each section, close the file and answer: **What does this part do? Why did we build it this way? What can fail? What proves it works?** If you can answer those four questions, you understand more than a memorized slide.

## Important reading rules

Status labels in this handbook mean:

- **Implemented:** inspected source contains the behavior.
- **Verified:** this audit executed a relevant check or isolated probe.
- **Simulated:** a deterministic stand-in exercises the software contract.
- **Proposed:** recorded future design, without implementation or acceptance being assumed.
- **Unverified:** inspection does not establish execution, deployment, clinical validity or completeness.

The graph is a navigation tool and a record of context. Its edges can describe old or inferred relationships. Current source code establishes implementation facts. PRD and approved decisions establish requirements. When those disagree, the audit records both.

Do not quote the old “frontend is disconnected” status or the old “MRI is excluded” sentence as current state. Conversely, a merged branch called `ai-02b-retrieval-corpus` does not prove real retrieval exists: the merged work currently consists of the proposed decision and plan. See the audit for exact evidence.

## When you get a question you cannot answer

Say: “I can explain what we have verified. That part is still planned or needs another check, so I don't want to give you an unsupported result.” Then explain the relevant current mechanism and the next verification step.

Avoid inventing model accuracy, dataset training results, performance improvements, regulatory compliance or a completion percentage. None was established by this audit.

## Maintaining this handbook

Open the repository in Claude Code or Codex and use the refresh prompt in [Study with AI](STUDY-WITH-AI.md). The agent should compare the audited commit with current HEAD, inspect changed code and update both the learning reference and audit. A new graph date alone is insufficient evidence of freshness.

For requirements, return to [PRD](../PRD.md), [APP-FLOW](../APP-FLOW.md), [TRD](../TRD.md), [MVP scope](../NEUROONE-MVP-SCOPE.md) and [decision records](../decisions/). Those retain their authority. This handbook explains them and records observed differences.
