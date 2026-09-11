# ADR-006: MRI Becomes a Primary Input, With Symptoms as Context

## Status

Accepted. Revises PRD §7 and §8, AGENTS.md §15 and §19, and the MVP definition in `NEUROONE-MVP-SCOPE.md`. Extends [ADR-003](ADR-003-ai-analysis-contract-and-provider-seam.md) with a third provider seam and constrains how a stage estimate may be expressed under FR-04.

## Context

PRD §7 listed `MRI / image analysis` as a V1 hard exclusion, and AGENTS.md §19 required that such an exclusion only leave V1 if "the product documents are deliberately revised." The frontend, meanwhile, was built around MRI staging: a scan dropzone, an upload flow, contributing-region bars, a confidence dial, and a single stage badge reading `CN / MCI / Mild / Moderate / Severe`.

That divergence was found while auditing the dashboard, and the natural assumption was drift from the redesign branch — that the UI had wandered and should be repointed at the documented symptom-driven journey. **That assumption was wrong.** The MRI direction is deliberate product intent. The documents, not the interface, were stale.

This ADR is the deliberate revision §19 asks for. Without it, the exclusion stands and any contributor reading §19 would be correct to refuse to build scan intake.

## Problem

Admitting MRI is not a one-line edit to an exclusions list. It collides with three things that are already built and already load-bearing:

1. A complete symptom → case → differential → evidence → PDF pipeline exists and is tested. Does the scan replace it or join it?
2. FR-04 forbids representing output as a definitive diagnosis, in the schema, in API field naming, **in UI copy**, and in the PDF. A lone stage badge beside a confidence dial is exactly the framing FR-04 exists to prevent — and the dashboard was displaying confidences of 96% and 97% against a `MAX_CONFIDENCE` ceiling of 0.92 that exists precisely so output never expresses certainty.
3. The stated USP is trend-aware early detection across a patient's visit history. Where a scan attaches in the data model decides whether that survives.

## Constraints

- The clinical safety boundary (AGENTS.md §2.1) is not negotiable and is not revised here. NeuroONE assists; it does not autonomously diagnose.
- FR-04's prohibition on definitive-diagnosis framing continues to apply to the stage estimate.
- `MAX_CONFIDENCE = 0.92` continues to apply. No displayed confidence may exceed it.
- Ownership and enumeration rules ([ADR-001](ADR-001-ownership-violation-status-code.md), [ADR-002](ADR-002-visit-ownership-derivation.md)) apply unchanged to any new entity.
- Binary payloads stay out of the database ([ADR-004](ADR-004-clinical-report-snapshot-and-rendering.md)).
- Demo data remains synthetic. A scan is imaging PHI, which raises the cost of that assumption being violated.

## Decision

**1. MRI is a primary input; symptoms are supporting context; there is one analysis per visit.**

A visit becomes *scan + symptoms + chief complaint at a point in time*. One analysis consumes all of it. The symptom pipeline is not replaced and not duplicated.

**2. The scan attaches to a Visit, not to a Patient.**

Cross-visit scan comparison then costs nothing structurally, because `detect_trends` already consumes per-visit data and the visit ownership rules already exist. Attaching a single current scan to a Patient would have been simpler and would have destroyed the trend story.

**3. The stage estimate is the top-ranked candidate, never a lone verdict.**

Output stays a ranked list with likelihood bands, supporting *and* contradicting findings, and citations. `CN / MCI / Mild / Moderate / Severe` may appear as the highest-ranked candidate; it may not appear as a single headline answer with a certainty figure. The word "certainty" does not appear in UI copy.

**4. The staging model is mocked behind its own provider seam.**

A third seam alongside the retriever and the reasoning client, following the pattern that has now worked twice ([ADR-003](ADR-003-ai-analysis-contract-and-provider-seam.md), [ADR-005](ADR-005-live-llm-provider.md)): schema-real, provider-mocked, deterministic, labelled as simulated. Because provenance is now three-dimensional — simulated retrieval, live reasoning, simulated staging — `AI_PROVIDER` as a single literal no longer stretches, and staging needs its own setting.

**5. The scan file is retained outside the database.**

A PDF can be regenerated from its snapshot; a scan cannot. The bytes live in file or object storage, with a reference, dimensions and a checksum in the database. This keeps ADR-004's no-binary-column rule while accepting that imaging is source data rather than a derived artifact.

**6. Clinician sign-off gates the report.**

No PDF is produced until a clinician has accepted or amended the analysis, and the report records who signed and when. This makes the safety boundary structural rather than a disclaimer: nothing leaves the system as a document that a human did not accept.

**7. The dashboard is a triage queue.**

Ordered by open `early_watch` flags, then worsening trends, then analyses awaiting sign-off. No stat tiles — the queue is itself the answer to "what needs attention", and an aggregate confidence average across patients is both clinically meaningless and a step back toward the framing FR-04 warns about.

**8. Intake splits into New Patient and New Visit.**

Patient creation takes demographics only, matching the real `PatientCreate` contract. Visit creation takes scan, symptoms and complaint. Creating a patient offers their first visit immediately. The previous single combined form could not express "an existing patient returns for a follow-up scan" — which is the only case that produces a trend.

**9. Provenance is stated per analysis, not per environment.**

Each analysis carries a line describing what was real and what was simulated, derived from `pipeline_note`, and it travels into the PDF. A screenshot of a result cannot then be mistaken for validated clinical output.

## Why

**MRI primary with symptoms as context, rather than replacing the pipeline**, because the alternative discards a tested backend and the literature-citation differentiator to save UI work. The scan becomes the strongest signal in an analysis that still explains itself through findings and evidence — which is the product described in PRD §1, not a different one.

**Stage as a ranked candidate** because this is the whole substance of the safety boundary. A stage label is a conclusion; a ranked differential with contradicting findings is decision support. The distinction is not cosmetic, and it is the reason FR-04 names UI copy explicitly rather than only the schema.

**A scan on the Visit** because the USP is a trajectory, and a trajectory needs more than one point.

**Sign-off gating the report** because "a clinician reviews it" is otherwise unfalsifiable. If an unreviewed AI document can be printed and circulated, the review step is decoration.

**No stat tiles** because every tile on the audited dashboard was derived from a hardcoded array, and the honest replacement for fabricated summary numbers at this data volume is not better fabricated numbers — it is the queue.

## Consequences

- **PRD §7 loses one exclusion, and only one.** `Uploaded diagnostic-report analysis`, `autonomous diagnosis` and `automated treatment decisions` remain hard exclusions. Admitting MRI is not a precedent for admitting the others.
- **A new entity and migration.** A scan per visit, with storage metadata and a checksum. Ownership derives from the parent visit, and therefore from the parent patient, per ADR-002.
- **A storage backend becomes a deployment dependency.** The application no longer runs on a database alone.
- **`detect_trends` must be extended.** It reads symptom severities today. Unless scan-derived metrics feed it, the trend story stays symptom-only and the scan contributes nothing to `early_watch`.
- **A triage query is required.** Ordering across all of a clinician's patients by flag, trend and review state cannot be assembled from the existing per-patient routes.
- **New analysis state.** Reviewer identity and timestamp, plus the gate on the PDF endpoint. ADR-004's render-before-persist behaviour is unchanged.
- **The current upload page is broken and must be rebuilt, not adapted.** It posts `multipart/form-data` with `mri_scan`, `mmse_score` and `family_history` to `POST /patients`, which accepts `PatientCreate` JSON. It cannot ever have worked, and its comment describes a "kicks off the AI pipeline" contract that does not exist.
- **Existing UI must be removed, not repointed:** the single stage badge, `stageLabel` as a headline, "Model certainty" copy, any confidence above 92%, the `Critical`/`Stable` severity vocabulary with no backing in the model, and the scan-volume chart that measures nothing.

## Risks

- **A staging UI backed by a mocked model is more convincing than a mocked text pipeline.** A brain region with a percentage looks like measurement. Decision 9 is the mitigation and is not optional.
- **Imaging PHI raises the stakes on the synthetic-data assumption.** That assumption is still unconfirmed in `NEUROONE-MVP-SCOPE.md` and should be confirmed before any real scan is loaded.
- **Scope creep pressure.** Region attribution, segmentation and longitudinal registration are adjacent, individually reasonable, and collectively a different project. They are not admitted here.
- **Two signals can disagree.** Symptoms may point one way and the scan another. This ADR makes them one analysis, so disagreement surfaces as contradicting findings on a candidate rather than as two competing verdicts — but the reasoning prompt has to actually do that.

## Alternatives Rejected

**MRI replaces the symptom pipeline.** Simplest interface, and it deletes a tested backend, the evidence/citation differentiator, ADR-003, ADR-005 and the trend detection that carries the USP. Rejected as paying in capability for a saving in UI work.

**Two independent analyses side by side.** Complete, and it doubles the output surface while leaving a clinician to arbitrate between two machine opinions with no stated basis for preferring either. Rejected because the arbitration is the clinical work, and handing it over unstructured is worse than one analysis that shows its tensions.

**A single definitive stage with a confidence figure.** What the dashboard did. Rejected: it requires revising §2.1 and FR-04, which is a materially different product decision from admitting an input type, and it was not the intent behind the MRI direction.

**One current scan per patient.** Rejected — it removes the second data point that early detection requires.

**A persistent environment-level demo banner.** Unmissable, and it says nothing about which parts of a specific result were simulated, which is the thing a stakeholder actually needs to know when looking at one analysis.

## Migration / Rollback Impact

No data migration for existing records: visits without a scan remain valid, and an analysis can still run on symptoms alone. This is additive.

Rollback means dropping the scan entity and its storage configuration, reverting the staging seam, and restoring the PRD §7 exclusion. Any analysis already produced from a scan would lose the input it was derived from, so rollback after real use is a data-retention decision rather than a code revert.
