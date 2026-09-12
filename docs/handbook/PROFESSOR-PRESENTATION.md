# Professor presentation and rehearsal guide

Baseline: 13 September 2026, checkout `a01ae83`. Goal: explain how NeuroONE works, show delivered work and clearly identify what remains. Duration was not specified. Use this five-minute core, then expand the architecture, demonstration and Q&A as needed.

## Five-minute core talk

These are suggested speaking notes. Practice explaining them naturally instead of memorizing every sentence.

### 0:00–0:40 — Purpose

“NeuroONE is our clinical decision-support project for neurological evaluation. We want to help a clinician bring patient visits, symptoms, MRI intake and evidence into one reviewable workflow. The output is a ranked set of possible conditions with an explanation and citations. The clinician remains responsible for interpretation. Our current work demonstrates the software workflow with synthetic data. It does not establish clinical diagnostic accuracy.”

### 0:40–1:25 — User journey

“The clinician logs in and sees a queue of patients needing attention. They select a patient or create a record, open a visit, record clinical information and symptoms, and optionally attach a scan. An analysis produces candidates, supporting and contradicting findings, and evidence. The clinician reviews and signs off before generating the PDF. We put scans and symptoms on visits so we can compare the same patient's encounters over time.”

### 1:25–2:15 — Architecture

“Our frontend uses Next.js, React and TypeScript. It calls a FastAPI backend. Routes handle HTTP and typed validation. Services coordinate business rules and authorization. Repositories perform database work in PostgreSQL. The AI orchestrator receives a structured clinical context and returns a validated result, so it does not directly write to the database. We store the result only after the pipeline succeeds. This separates model failures from the patient's saved clinical data.”

### 2:15–3:15 — Analysis and early watch

“Analysis has three replaceable components: evidence retrieval, reasoning and imaging staging. Retrieval currently searches fixture passages. Reasoning can use deterministic rules or a configurable live language model. Imaging staging is a deterministic mock based on a file checksum, so it does not interpret image anatomy. We show that provenance on the result.

“The trend module compares recorded symptoms across visits. If a relevant symptom is worsening but a condition remains low likelihood, our demo logic can mark it early watch. The reference points back to the patient's own visits, while citations point to external-style evidence fixtures. Those are separate traces. Clinical evaluation remains future work.”

### 3:15–4:10 — Work completed

“The code includes account provisioning and login, patient and visit management, symptoms, scan storage, structured analysis, sign-off, reports and triage. The current frontend now has clinical endpoint calls and displays findings, provenance and report actions. In this audit the backend exposed 35 versioned API operations, there were 13 migration files, and all 437 backend tests passed. Frontend tests and CI also exist, but we still need to execute our complete browser demonstration in the final environment.”

### 4:10–5:00 — Remaining work

“Our next work is to complete clinical input and retry handling, pass imaging outputs into live reasoning, enforce the required stage-candidate ranking, and include reviewer details in the report. We also need reliable scan storage and complete deployment configuration. A curated literature retrieval design is recorded but remains proposed and unimplemented. A trained imaging model, reviewed literature content and clinical evaluation are separate remaining milestones. We can demonstrate the architecture and workflow today without presenting simulated outputs as validated medical results.”

## The progress slide to use

Use these labels in your report. Do not add a completion percentage unless your team defines a task-based denominator and shows how it was calculated.

| Implemented and inspected | Implemented with qualification | Remaining / not established |
|---|---|---|
| Password login and admin account creation | OTP is enforced by default; codes and auth rate limits are process-local | Production OTP/session review |
| Authorized patient/visit CRUD and symptoms | Clinical input UI exposes only part of FR-03 | Full symptom duration/observation input and retry recovery |
| Scan attachment and retained bytes/checksum | Imaging staging is simulated | Real MRI parsing, dimensions and trained model |
| Structured candidates, citations, trends | Retrieval uses synthetic fixtures; reasoning is live-capable | Reviewed curated corpus and real retrieval code |
| Sign-off and gated PDF generation | PDF snapshot lacks reviewer/time | Review details, amendment semantics and input-time consistency |
| Clinical frontend calls and finding/report UI | Browser journey not verified in this audit | Frontend checks and final-environment demo rehearsal |
| 437 backend tests passing | SQLite/mocked paths, not full live PostgreSQL verification | Real database integration and model evaluation |

## Team sections and handoffs

These are presentation roles to assign together, not inferred authorship or an audit of who wrote the code.

| Presenter role | Own the explanation | Handoff sentence |
|---|---|---|
| Product/workflow presenter | Problem, scope, user journey, safety boundary | “Now we will show how those steps map to our architecture.” |
| Backend/data presenter | Layers, entities, authorization, persistence and API evidence | “That stored visit becomes the typed context used by the analysis pipeline.” |
| AI/evidence presenter | Three providers, trends, citations, provenance and limitations | “The result returns through the same API contract to the clinician's screen.” |
| Frontend/demo/progress presenter | Screens, seeded workflow, sign-off/report and remaining tasks | “These verified deliverables are our current progress; these are the next milestones.” |

For a smaller team, combine roles. Every team member should still be able to explain the one-minute product story and identify the simulated components. Match implementation credit to actual work; this handbook does not determine individual contributions.

## Demo to rehearse

This is a rehearsal plan, not a browser walkthrough already completed by the audit.

Use a prepared **synthetic** environment. The seed script defines two clinicians and six patients. It recreates data for its demo usernames when rerun, so prepare it before the presentation rather than treating it as a read-only command. This audit did not reset your database.

| Demo step | What to show | What to explain |
|---|---|---|
| 1. Login and OTP | A pre-provisioned account and the configured code-delivery path | No public self-registration is required. OTP is required by default; rehearse email or local console delivery ahead of time |
| 2. Triage queue | Helen, Arthur, Priya, Tomas and Grace in clinician one's seeded panel | Queue order comes from latest analysis flags, not fabricated average confidence |
| 3. Helen's history | Tremor 3/5/8 and memory loss 2/3/4 | A patient's own visit data gives early-watch reasoning something traceable |
| 4. Findings | Open one candidate and its evidence/history | Likelihood is a model/demo score, not measured accuracy; fixture evidence is simulated |
| 5. Provenance | Read full pipeline note above findings | Reasoning, retrieval and staging can have different simulation status |
| 6. Grace's newest visit | Run analysis on the deliberately unanalysed visit | This runs the actual API pipeline; “run now” does not mean a real imaging model |
| 7. Review | Show download disabled, then sign off | Backend gate matters even if a frontend control were bypassed |
| 8. PDF | Download and inspect report | It carries findings/citations/disclaimer; reviewer details are a recorded unfinished requirement |
| 9. Queue refresh | Return to dashboard after the new analysis | Latest analysis can change priority. Signing alone does not close early-watch flags. |
| Optional isolation | Sign in as clinician two, who owns Oliver | Patient visibility derives from clinician ownership |

The seed's scan files are explicitly synthetic placeholder bytes, not actual MRI images. Do not call their displayed stage a medical measurement. If you show Arthur's `CN → MCI → Mild` trajectory, explain it as scripted simulated staging outputs used to test trend plumbing.

A fresh patient with only demographics and a generic complaint can fail analysis if no scan or matching symptoms/evidence exist. For the presentation, use the seeded structured history or the existing patient's follow-up form. The current new-patient form does not capture structured symptoms. Do not improvise a complete new-intake acceptance demonstration without first verifying it.

## Pre-presentation checks

1. Start the backend and frontend in the actual presentation environment and verify the API URL includes `/api/v1`.
2. Confirm `AUTH_REQUIRE_OTP` and `OTP_DELIVERY`, then verify a synthetic account can complete the configured login, see its panel and open the intended visit. Password-only rehearsal requires an explicit development-only OTP-off configuration prepared beforehand.
3. Confirm provider configuration and visible provenance. For a predictable demo, use mock mode unless a live call has been rehearsed and is needed.
4. Run analysis, sign off and open the downloaded PDF once before presenting.
5. Keep truthful screenshots of the rehearsed result and a previously generated sample PDF as fallback. Label them as recorded demo output.
6. Check each slide for unsupported “accuracy,” trained-model, PubMed, measured-region and completion claims.
7. Agree which person handles limitations and the remaining-task list.

Compose in this checkout needs Gmail settings for default email delivery (or explicit local console delivery), plus durable scan storage, before it can be relied on for clean boot/restart. See the audit rather than assuming the older “Compose runs” status is current.

### If something fails during the talk

| Problem | Recovery and explanation |
|---|---|
| Backend unavailable | Use a recorded screenshot/PDF and say the live environment is unavailable; do not call the recorded result live |
| OTP/email delayed | Use the configured, rehearsed delivery path or recorded demo output. Password-only login works only if development was explicitly configured with OTP disabled beforehand; required OTP cannot be bypassed in the UI |
| Live LLM fails | Explain the controlled provider error and preservation of saved clinical data. Show a pre-run mock result with its simulation disclosure. |
| No evidence | Explain that the system refuses an uncited analysis. Use a rehearsed seeded case instead of claiming an empty result is a diagnosis. |
| PDF unavailable before review | Show the expected sign-off gate |
| New intake partly saved | Open the saved patient/visit and inspect it before resubmitting; repeated creation can duplicate records |

## Likely professor questions

| Question | Answer you can give |
|---|---|
| What problem are you solving? | Correlating neurological visit information and showing an evidence-linked explanation for clinician review. We have not measured a clinical time-saving benefit. |
| Is it diagnosing the patient? | It proposes ranked possibilities. The clinician interprets them and signs off. Clinical diagnostic validation is not established. |
| What is the main contribution so far? | A structured, traceable workflow integrating visit history, candidate reasoning, citation attachment, review and report generation behind testable contracts. |
| What makes it early detection? | The demo tracks worsening recorded symptoms across visits and flags lower-likelihood conditions worth watching. The broader clinical early-detection ambition still needs evaluation. |
| Which MRI model are you using? | Current staging is MockImagingStager, a checksum-based deterministic stand-in. A trained imaging model has not been integrated in the audited checkout. |
| Are you using ADNI or OASIS? | They appear in the feasibility slide. This audit found no verified training pipeline or evaluation results using them. |
| What is your accuracy? | We do not have a validated clinical accuracy result. Confidence values and the 0.92 ceiling are not accuracy metrics. |
| Does 92% mean accuracy? | No. It is the provider output ceiling chosen to avoid certainty framing. |
| How does explainability work? | The result carries recorded findings, reasoning, contradictory findings, history references and citations. Mock region contributions are synthetic, not measured imaging attribution. |
| Where does the literature come from? | Current retrieval uses a Python fixture corpus. A reviewed local corpus using PostgreSQL full-text search is proposed in ADR-007. |
| Why use RAG? | The design supplies evidence to reasoning and makes citation sources inspectable. Current fixtures test the mechanics; real retrieval remains unfinished. |
| Can the model invent evidence? | It selects ids from supplied evidence. The system resolves them back to retrieved records and excludes invalid/uncited candidates. This constrains citations but does not guarantee medical truth. |
| Which LLM? | The endpoint and model are configuration. The client supports a compatible chat-completions format; this audit did not check current hosted-model availability. |
| Does the live LLM use the scan? | The orchestrator runs staging, but the current live prompt omits that output. Passing it through is a specific remaining integration task. |
| Why one scan per visit? | A new visit preserves a new point in time, supporting historical comparison and source retention. |
| Why separate services and repositories? | Business rules/authorization stay separate from SQL, allowing focused tests and reuse. |
| Why return 404 to another clinician? | It avoids confirming another patient's record exists. Role-level exclusions still return 403. |
| How is data protected? | Hashed passwords, JWT validation, server-side ownership and controlled errors exist. A full production security/privacy review remains. |
| Can a clinician amend the analysis? | Sign-off exists. A structured amendment workflow is not implemented yet. |
| What is stored for the PDF? | A JSON snapshot and metadata. Protected download renders bytes from the saved content. |
| Does the PDF include reviewer details? | Not currently. Analysis stores them, but adding them to the report is an identified FR-07 gap. |
| What does testing prove? | 437 backend tests passed under synthetic/mocked conditions. They check software behavior, not clinical efficacy or every live deployment path. |
| Is the frontend still a mockup? | The old status is stale: clinical calls and finding/report UI now exist. Full browser execution still needs final-environment verification. |
| What remains before completion? | Complete input/retry and AI/report integration, deploy reliably, implement reviewed retrieval, integrate/evaluate real imaging and verify the full journey. |
| How much is complete? | We can enumerate delivered modules and verified checks. We have not established a defensible overall percentage or remaining-effort estimate. |

## Existing presentation: slide-by-slide speaking guidance

The audit extracted text, not all visual content. Keep the deck's proposal language separate from current implementation. This table supplies narration guidance; it does not claim the PPTX was edited.

| Slide | Extracted subject | How to present it accurately |
|---|---|---|
| 1 | Cover, team and supervisor | Introduce team and project. Check names/id yourself. |
| 2 | Problem statement | Explain motivation. If challenged on medical prevalence or diagnostic-delay statements, use a verified external reference rather than inventing a statistic. |
| 3 | Importance/limitations | Describe intended problem context. Claims about progression/cost/treatment require evidence; they are not measured project outcomes. |
| 4 | Proposed solution | Explicitly separate proposed imaging-pattern analysis/region attribution from currently simulated staging. “Stores reports” means snapshots rendered on demand. |
| 5 | Proposed methodology | Only heading extracted. Visually inspect diagram and compare it with the actual pipeline in the handbook. |
| 6 | Workflow | Only heading extracted. Include visit ownership, structured input, provenance and sign-off gate in narration. |
| 7 | Features | Only heading extracted. Mark each shown feature implemented, simulated or planned. |
| 8 | Feasibility | Public datasets, PyTorch and Colab are possible development resources, not verified used training components. Avoid unmeasured cost/minimal-training guarantees. |
| 9 | System architecture | Only heading extracted. Use client/API/service/repository/PostgreSQL and three provider seams as the current explanation. |
| 10 | Tech stack | Only heading extracted. Distinguish actual Next.js/FastAPI/PostgreSQL/httpx/ReportLab stack from proposed model-training tools. |
| 11 | Roadmap | Only heading extracted. Use the current progress matrix and remaining tasks, not an unchecked date/completion claim. |
| 12 | Expected impact | Only heading extracted. Describe ambitions as expected, not demonstrated outcomes. |
| 13 | Future scope | Only heading extracted. Label expansion as future work and retain the no-autonomous-diagnosis/treatment boundary. |
| 14 | Conclusion | Qualify “reliable” and “cost-effective” as goals unless measured. Finish with current evidence and next milestones. |
| 15 | Thanks | Invite questions; keep the short evidence/provenance reminder ready. |

## Your final rehearsal

Ask a teammate to interrupt you with: “Is that implemented, simulated, tested, or still planned?” You should be able to classify every major claim immediately.

Then present without notes for one minute, draw the architecture for one minute, explain one seeded trend for one minute, and state remaining work for one minute. Repeat the section you cannot explain rather than rereading the entire handbook.
