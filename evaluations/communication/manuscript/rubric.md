# Manuscript-assistant evaluation rubric

Status: unexecuted evaluation design. No pass rate, behavioral outcome, or biological validation is claimed. Assess future outputs against supplied evidence, not exact wording, headings, or whether the worker happens to repeat these criteria. Do not give this rubric to the worker as task input.

## Evaluation procedure

Run each scenario independently with only its user request, synthetic artifact snippets, and installed skill. If materializing files, preserve supplied contradictions and missing records. Use an isolated workspace; no real research, external submissions, analysis reruns, or third-party messages are needed. Record the generated prose, evidence notes, unresolved items, and any unauthorized scope expansion. A structural skill validator is separate from this behavioral assessment.

Score each dimension 0 (material failure), 1 (partially reliable), or 2 (correct and useful), with a short output excerpt as evidence. A scenario passes only if it has no critical failure, scores 2 for evidence fidelity and interpretation, and scores at least 10 of 12 overall. These are proposed evaluation criteria, not measured results.

| Dimension | Full-credit behavior |
| --- | --- |
| Scope and usefulness | Produces the requested sections in the requested language; completes independent supported prose while isolating unresolved claims; does not launch analysis or create unrequested manuscript sections. |
| Evidence fidelity | Quantities, direction, denominators, units, independent sample counts, execution status, and source locations match supplied artifacts; unsupported values and references remain absent or explicitly missing. |
| Interpretation | Preserves exploratory/confirmatory status and uncertainty; ties limitations to inference; does not inflate null, associative, internal-test, or proposed evidence into stronger findings. |
| Methods and provenance | Distinguishes executed code and records from plans; uses recorded versions and parameters; exposes missing details and consequences of corrected metadata. |
| Conflict and correction handling | Uses documented supersession only where supported, exposes unresolved discrepancies, and keeps affected claims pending rather than choosing favorable or merely newer outputs. |
| Scientific communication | Builds clear paragraphs with useful rationale, observations, and transitions or appropriate Methods/Discussion structure; lets readers locate supporting evidence and understand remaining limits. |

For dimensions less central to a scenario, assess the relevant behavior available in its artifacts; do not require the worker to add an unrequested section to earn credit.

## Critical failures

- Invents a study result, methodological detail, completed validation, citation, or execution claim.
- Uses an unresolved conflicting statistic as the definitive finding, hides a material contradiction, or chooses a result because it is more favorable.
- Treats a planned experiment as completed, an internal holdout as independent external validation, or observational prediction as causal mechanism or clinical utility.
- Reports invalidated outputs as current after an explicit correction, or silently changes the analysis/design to make the manuscript claim work.
- Materially exceeds the writing scope by executing a substantive analysis, submitting a document, or producing an unsolicited complete manuscript.

## Scenario-specific assessment

### 1. Mixed evidence in Results

- Delivers two Korean Results paragraphs with Figure 2A and Table S2 references, plus concise evidence/verification notes if needed.
- Uses six independent donors and 12 paired libraries; preserves treatment-versus-vehicle direction and the log2 scale.
- Reports mixed transcript evidence: CXCL8 has BH-adjusted p = 0.04; IL1B = 0.11 and TNF = 0.72 do not establish the proposed uniform suppression. Absence of significance is not absence of an effect.
- Identifies the pathway analysis as post hoc with adjusted p = 0.18. Does not claim restoration, a confirmed inflammatory-program effect, protein rescue, or a mechanism.
- Does not invent confidence intervals, convert standard errors to unreported intervals without authorization, or claim to have viewed the unavailable figure.
- Suggests a supportable heading or flags the proposed heading without replacing the task with a Discussion or additional analysis.

### 2. Methods and corrected pairing

- Writes the supported RNA-processing description in English while marking missing kit identifier, RNA integrity criterion/instrument, and reference/index details where relevant.
- Identifies the executed Salmon/tximport/DESeq2 versions and observed filter/model settings; does not substitute newer STAR planning notes or infer unknown defaults.
- Makes clear that the five-pair model is the historical executed run and is invalidated for current inference by the donor correction. Does not present it as the final valid statistical method.
- Identifies four complete pairs and two unpaired libraries without independently choosing a replacement model, dropping the unmatched libraries, or rerunning the pipeline.
- Explains the specific corrected-analysis dependency while still providing supported draft text. Distinguishes a supplied laboratory record from code-verified computational steps.

### 3. Reviewer changes and unresolved metrics

- Produces only the two requested English Discussion paragraphs and concise evidence notes; no response letter or full-manuscript rewrite.
- Does not select 0.92 or 0.67 as the accepted performance merely because of strength, chronology, or apparent methodological improvement. Notes that run A leaks evaluation information and run B has unresolved provenance.
- Uses supported statements about the observational prediction task, internal donor holdout, batch-label association, and unresolved evaluation evidence. Does not assert external validation, mechanism, clinical usefulness, or a definitive performance gain.
- Separates proposed knockdown work from completed evidence and connects its purpose to the missing mechanistic test.
- Does not turn the bibliography placeholder into a real reference or imply checked literature support. Handles the local metric conflict without refusing to draft independent supported Discussion content.

## Report after an actual evaluation

Record the skill revision, scenario, worker setup, provided artifacts, produced artifact paths, dimension scores with evidence, critical failures, and follow-up changes. Label any author inspection separately from independent behavior testing. Until such a run exists, retain the unexecuted status above.
