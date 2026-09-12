# Study NeuroONE with Claude Code or Codex

Use either agent with this repository open. Both can read the same Markdown handbook and project files. This guide provides copyable project-specific prompts. It does not depend on any particular app UI or claim a new tool has been installed.

## Launch a grounded tutor

Paste this as your first message:

```text
MODE: PLAN

Act as my NeuroONE project tutor for a report to my professor. My team must explain how the project works, what is completed, and what remains.

Read AGENTS.md and docs/handbook/README.md first. Then use PROJECT-HANDBOOK.md, PROFESSOR-PRESENTATION.md and AUDIT.md in that folder. The handbook was audited at commit a01ae83 on 2026-09-13. Check current HEAD before calling its status current.

For codebase questions, follow the installed graphify instructions and query the existing graph first. Check graph built_at_commit, distinguish extracted/inferred/ambiguous links, and inspect the cited source file when a fact matters. Use docs/PRD.md, APP-FLOW.md, TRD.md, NEUROONE-MVP-SCOPE.md and decision records to determine requirements. If graph or old documentation disagrees with current code, explain both and flag the conflict.

Teach me in plain language. Start with the product story, then visits/data relationships, architecture, API contracts, AI providers, trends, citations, review/reports, testing, progress and remaining tasks. Explain one topic at a time and ask one recall question, then wait for my answer. Do not dump a full questionnaire.

Mark factual statements as implemented, verified, simulated, proposed or unverified. Do not turn confidence scores into accuracy, simulated imaging into anatomical inference, fixture citations into reviewed literature, or a merged planning branch into a working provider. Preserve the difference between a patient's trend_basis and external evidence.

For every correction, give the corrected explanation and a source file/section or symbol. If a fact cannot be established, say so. Keep an error log during this conversation. After each topic, give one 20-second presentation answer and one likely professor question. Revisit missed concepts later.

This is a study session. Do not edit application code, change schemas, install dependencies, seed/reset a live database, send email, call a live model, approve ADRs or change product scope. Ask before writing a persistent study log unless I request one. Begin by asking me to explain NeuroONE in my own words in 30 seconds.
```

The agent should wait after asking a recall question. Learning happens when you attempt an answer before seeing the reference explanation.

## Focused learning prompts

| Topic | Prompt to paste |
|---|---|
| Architecture | “Teach me one analysis request from browser to persisted result. Explain why each layer owns its step, then ask me to reconstruct the path.” |
| Database | “Help me draw Patient → Visit → Scan/Symptoms → Analysis → Findings/Evidence → Report. Quiz me on cardinality and where ownership lives.” |
| AI truth | “Test whether I understand simulated retrieval, mock/live reasoning and simulated imaging. Give me one ambiguous claim at a time to correct.” |
| Early watch | “Use Helen's seeded tremor and memory-loss history. Ask me why a worsening trend and low confidence together can create early_watch, and why low confidence alone cannot.” |
| Citations | “Explain provider selects/system resolves. Quiz me on why evidence ids and history UUIDs should come from source records.” |
| Safety and auth | “Ask me to distinguish diagnosis assistance, authentication, role authorization, per-record ownership and clinician sign-off.” |
| Reports | “Quiz me on analysis snapshot versus report snapshot, sign-off gating, missing reviewer fields and what happens after a clinical-input edit.” |
| Progress | “Ask what is complete and what remains. Mark my answer against the dated audit. Do not let me give a completion percentage without a denominator.” |
| Decisions | “Pick one accepted ADR, explain its problem/options/choice/cost, then ask me to defend it against the rejected alternative.” |
| Demo | “Walk me verbally through the seeded demonstration. Stop at each point where I might overstate a simulated capability.” |

## Professor mock viva

```text
Conduct a mock professor viva using docs/handbook/. Ask one question at a time and wait. Mix product, architecture, database, AI, testing and progress questions. Start simple and become more technical.

After each answer, score it 0–3:
0 = incorrect or unsupported claim
1 = partly correct but missing a major distinction
2 = correct explanation with minor gaps
3 = correct, concise, source-grounded explanation with relevant limits

Correct errors using current source code and governing documents. Pay special attention to MRI staging being checksum-based, mock literature, live prompt imaging omission, early_watch requiring a trend, sign-off versus amendments, missing reviewer details in PDF, and the scope of the passing tests. If the code has changed, verify before repeating an old limitation.

After ten questions, summarize my weak topics and give a short targeted revision plan. Keep the assessment about my understanding. Do not modify the project.
```

## Rehearse the team report

```text
Review the project explanation I paste next as speaking notes for our professor. Classify each technical/progress claim as supported, overstated, outdated or needs verification. Cite sources for corrections.

Keep my natural speaking style. Make the explanation concise and preserve required disclosures. Do not invent team contributions, model metrics, dataset use, remaining dates or a percentage complete. Then ask the three questions a professor is most likely to raise. Wait for my draft.
```

## Maintain a study log

If you want a persistent record, explicitly ask:

```text
Create or update docs/handbook/MY-STUDY-LOG.md with topics I have learned, questions I missed, corrected short answers, supporting source pointers and the next revision topics. Record current date and HEAD. Keep it separate from authoritative project decisions. Do not include patient data or secrets.
```

Suggested fields: topic, attempted answer, misconception, corrected answer, source, confidence in recall and revisit date. A strong recall score does not establish product completeness.

## Refresh the handbook after development

```text
MODE: PLAN

Audit and refresh docs/handbook/ for the current NeuroONE checkout. I authorize documentation updates only.

Read AGENTS.md and the handbook audit. Compare current HEAD with baseline a01ae83. Query Graphify first, check its built_at_commit and inspect relevant changes in source. Verify old limitations before carrying them forward. Read current requirements and ADR status. Distinguish accepted/implemented decisions from proposals and unresolved questions.

Run appropriate existing checks only under synthetic/offline test settings. Do not touch a live clinical database, reset demo accounts, expose secrets, send email or make live model calls. If checks cannot run, record the exact limitation.

Update the reference, professor guide and audit together: completed work, remaining work, counts, provider capabilities, tests, contradictions and new audit date/commit. Preserve historical evidence rather than claiming old findings were always false. Validate document links. Save a concise supported Graphify session memory using its CLI; do not hand-edit graph.json or silently rebuild semantic context.

Do not fix application code or approve scope/ADRs as part of this refresh. End with the important factual changes and verification limits.
```

## Useful local Graphify commands

Run these from the repository root when the installed Graphify CLI is available:

```powershell
graphify query "AnalysisOrchestrator DiagnosisCandidate"
graphify explain "AnalysisOrchestrator"
graphify path "AnalysisService" "ReportService"
graphify reflect --if-stale
git rev-parse HEAD
```

A relationship path is navigation, not proof of a runtime call. Queries may be truncated. Root graph can be newer than a dated snapshot directory. Compare `built_at_commit` and source content.

When development actually changes source, the repository instructions call for `graphify update .`. Follow the installed skill for that operation. A code-oriented refresh does not automatically guarantee every conversation or new document has been semantically captured. Use supported query-memory saving to retain concise verified outcomes, and keep accepted architectural decisions in `docs/decisions/`.

## A repeatable study routine

1. Explain yesterday's topic aloud before opening the file.
2. Read the relevant handbook section and verify one source pointer.
3. Answer three questions without notes.
4. Correct the mistake in your own words.
5. Finish with the 20-second version you would say to your professor.

Aim to reconstruct the system from its responsibilities and data flow. Source-backed explanations are more useful than memorizing isolated filenames or slide slogans.
