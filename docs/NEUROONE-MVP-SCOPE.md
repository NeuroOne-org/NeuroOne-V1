# NeuroONE — MVP Scope Definition (locked)

MODE: PLAN
STATUS: Scope decisions confirmed; feeds the next PLAN cycle (SEC-01 + AUTH-01)

## Purpose of this MVP
Investor/stakeholder demo. The bar is "demonstrates the full product concept convincingly end-to-end," not "production-grade clinical deployment." This changes rigor expectations for AI/RAG specifically, but does **not** relax security, layering, or safety-boundary requirements — those apply regardless of audience.

## MVP definition
Full PRD §8 acceptance journey, unphased at the product level:

```
Login → Patient → Case → Symptoms → AI Analysis →
Differential Diagnosis + Evidence/Citations → Clinician Review → PDF Report
```

All of FR-01 through FR-07 are in scope for this MVP. Nothing is cut — but FR-04/05/06 (the AI/RAG requirements) are phased at the *implementation* level, described below.

## AI phasing decision (new — governs AI-01)

**MVP-AI (this phase):**
- The AI orchestrator interface and the structured Diagnosis/Evidence output contract (TRD §9) are real and enforced — not skipped, not free-text.
- The retrieval corpus and the LLM call are **mocked/deterministic**: they return schema-valid synthetic results.
- Everything downstream of that — ranking, citation attachment, clinician review, PDF assembly — is exercised for real, against real (mocked-sourced) data flowing through a real contract.

**AI-02 (later phase, post-demo) — split in two, because the two protocols swap independently:**

- **AI-02a — live LLM (done, [ADR-004](decisions/ADR-004-live-llm-provider.md)).** `MockLLMClient` is joined by `LiveLLMClient`, reasoning through any OpenAI-compatible endpoint selected by config. It was a provider swap, not a pipeline rewrite — the contract, ranking, citation attachment, validation and persistence were untouched, which is what building the contract first bought. `AI_PROVIDER` still defaults to `mock`.
- **AI-02b — real retrieval corpus (deferred).** The mock retriever stays until a trusted-literature corpus, an index and a source-tier policy are decided. That is a larger scope decision than the model swap, and it is where the prompt-injection exposure actually lands: a retrieved passage is untrusted text in a way a symptom field is not.

Live reasoning over a still-simulated corpus is a real state and is labelled as one — every analysis carries `pipeline_note = "pipeline complete, live model reasoning, evidence retrieval simulated"`.

## Roles (confirmed)
`ADMIN`, `CLINICIAN`. `RECEPTIONIST` deferred — not in MVP, and not yet defined in PRD §4 (Users) if it returns later.

## Exclusions (confirmed, unchanged from PRD §7)
No MRI/image analysis, no autonomous-diagnosis framing, no automated treatment decisions. This holds independently of any future roadmap conversation about the README's language — that conversation is still parked.

## Assumption flagged for confirmation
**Demo data:** assuming synthetic/seed patient and case data for the demo environment, not real PHI — the system hasn't been through a security review and shouldn't hold real patient records yet. Flagging this as an assumption rather than deciding it silently.

## Risk to carry forward
A mocked AI backend that returns schema-valid diagnoses will *look* real in a demo. Internally this needs to stay clearly labeled as "pipeline complete, evidence retrieval simulated" — not presented as clinically validated output. This is a credibility/optics risk with an investor audience as much as a technical footnote, and should be reflected in how the demo is narrated, not just in code comments.

## Revised roadmap
```
SEC-01        housekeeping (.env untracking, SQL echo, /health exception exposure)
AUTH-01       CLINICIAN rename, real auth endpoints, soft-delete fix, DB rollback/error handling
PAT-01        authorized patient CRUD vertical slice
CASE-01       clinical case / symptom domain (currently a broken stub)
AI-01 (mock)  structured AI contract + mocked retriever/LLM + evidence/citation shape
REPORT-01     PDF assembly — full acceptance journey becomes demoable end-to-end
AI-02a        real LLM swap-in behind the AI-01 interface (done, ADR-004)
AI-02b        real RAG corpus behind the same interface (deferred)
```

## Early-detection design (confirmed — governs CASE-01 and AI-01, not SEC-01/AUTH-01)

**USP framing:** "Deep learning + ML + LLM enabled system detects neurodegenerative diseases in initial stages so they can be treated before it's too late" is confirmed as **vision/marketing narrative wrapping a clinician-assist tool**, not a literal autonomous-diagnosis claim. The safety boundary (assists, does not autonomously diagnose) stays intact.

**Mechanism for this MVP:** trend-aware reasoning over clinician-entered data across a patient's visit history, plus confidence-tiered output — not imaging/biomarkers. Imaging/biomarker analysis is confirmed out of scope for MVP ("both, eventually" — imaging is a later, separate phase, consistent with PRD §7's existing MRI exclusion).

**Design:**
1. Clinical context building (TRD §8) uses the patient's prior visits/cases, not just the currently open case. APP-FLOW §3 already models "Patient Profile → Cases / History" — this uses data that was always intended to exist.
2. The Diagnosis output contract (TRD §9) gains:
   - `category`: `differential_diagnosis` | `early_watch`
   - `trend_basis`: references to which prior visits/findings drove an `early_watch` flag, traceable to the patient's own history (distinct from external literature evidence)
   - all existing fields (confidence, supporting/contradicting findings, explanation, evidence[]) are unchanged
3. This is the concrete implementation of FR-04's existing "uncertainty" requirement — not a new functional requirement, so PRD does not need a rewrite.
4. AI-01's mocked/deterministic provider must simulate at least one multi-visit trend so an `early_watch` flag has something to point at in the demo.

**Unaffected:** the clinician journey (no new flow stage), the safety boundary, and the V1 exclusions (still no imaging, no autonomous diagnosis, no automated treatment).

**Downstream effect:** CASE-01 must implement real cross-visit history retrieval (the audit found the Visit model is currently a broken stub, so this was already required — now it has an explicit "must support cross-visit comparison" requirement). AI-01 must design its mock data with a multi-visit trend, not a single snapshot.

## Definition of "demo-ready MVP"
The full PRD §8 journey works end-to-end through the actual API/UI with synthetic data: a clinician logs in, creates a patient and case, enters symptoms, triggers analysis, sees a ranked differential diagnosis with evidence and citations (schema-correct, mock-sourced) — including at least one `early_watch` flag traced to a simulated prior-visit trend — reviews it, and downloads a PDF report. No real LLM/RAG call is required to hit this milestone.
