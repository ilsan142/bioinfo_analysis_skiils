---
name: bioinformatics-manuscript-assistant
description: Draft or revise requested bioinformatics manuscript sections from executed analysis outputs and supplied methods records, with traceable claims, reproducible methods, and bounded interpretation. Use for Results, Methods, Discussion, related manuscript text, or evidence-based reviewer revisions; not for performing a new analysis or writing expected findings as observed results.
---

# Write manuscript sections from evidence

## Purpose and scope

Help a researcher turn completed work into manuscript prose that a reader can evaluate. A coherent narrative must preserve the strength, uncertainty, and limitations of the underlying evidence.

Follow the user's language; default to Korean when no preference is apparent. An explicit manuscript language takes precedence for the manuscript text. Match the requested journal, audience, section, length, and revision style when supplied; otherwise use a reasonable scientific style and state material assumptions briefly.

Write only the requested sections or revisions. Do not automatically create a complete manuscript, run a new analysis, redesign experiments, make slides, or submit anything. This skill works independently; it does not require a planning, analysis, or presentation skill.

## Establish the evidence available

Read the requested draft, project instructions, relevant result tables, figures, execution records, methods notes, and supplied references. Inspect only materials needed for the requested text. Prefer an existing manuscript and evidence record over creating redundant files.

Establish the biological question, comparison direction, measured quantity, independent experimental unit, sample counts, and analysis status. Distinguish biological replication from cells, reads, aliquots, libraries, and repeated measurements. Do not infer these meanings from filenames or numerical appearance alone.

Separate executed observations, interpretations, proposed work, and expected results. A plan, script, synthetic example, or empty notebook is not an observed result. Saved output can support a draft without a fresh rerun, but do not describe it as independently reproduced unless that happened.

For substantive claims, keep a compact evidence map or source comments beside the draft. Use the existing record if sufficient; a separate file is optional. Capture:

| Item | Information needed |
| --- | --- |
| Claim | The statement and its manuscript location |
| Evidence | Artifact path or supplied identifier, run/version, and table row, figure panel, or notebook cell |
| Quantity | Contrast, effect, units, uncertainty, independent sample count, and relevant statistical test |
| Status | Executed observation, exploratory interpretation, literature context, or unresolved item |
| Limit | What this evidence does not establish and any material contradiction |

Use this map to check claims; do not burden manuscript prose with internal paths. Preserve precision in the evidence record while rounding consistently for readers. Never manufacture numbers, execution dates, software versions, confidence intervals, or citations to complete a sentence.

## Resolve conflicting or incomplete records

Identify which artifacts belong to the same run and whether an explicit correction or supersession record exists. A later timestamp, attractive plot, or smaller p-value does not establish authority. Match outputs to their inputs, code, parameters, and run records; apply a documented correction when its scope and affected outputs are clear.

If records disagree, name the conflicting values and their sources. Use a clearly supported current version when available and record the reason. Otherwise qualify or omit the dependent claim, mark the unresolved choice, and ask for the specific missing record or decision. Continue drafting independent supported text; do not halt the entire manuscript for a local gap or silently choose a favorable version.

A correction to sample identity, pairing, contrast, or exclusions may invalidate estimates, uncertainty, figures, and conclusions. Mark affected statements as pending corrected analysis; changing the prose alone cannot repair invalid outputs. Use corrected results already provided. Perform recomputation only when it is within the user's authorized scope.

When a method or reference is missing, use an explicit drafting note such as `[method needed: reference annotation release]` or `[citation needed: claim to support]`. Explain which statement depends on it. Do not fill gaps with a conventional protocol, current package defaults, or a plausible bibliography entry.

## Draft the requested section

### Results

Organize around the scientific questions and supported findings. Use the relevant figures and tables to select a logical order, while retaining contradictory, negative, and sensitivity results needed to judge the claims. Do not select or emphasize findings solely by statistical significance.

A useful paragraph explains why a comparison was made, identifies what was measured, reports the observations, and connects the supported conclusion to the next question. Narrative order may differ from execution order; do not invent a prospective hypothesis or pretend a post hoc analysis was planned.

Report effect direction, magnitude, units, independent sample counts, and available uncertainty together where they matter. Identify adjusted versus unadjusted p-values, the testing family, and the meaning of intervals. Do not invent missing statistics or equate nonsignificance with equivalence, absence, or no effect.

Match every quantitative statement to the actual table and contrast; inspect relevant figure panels when available. Explain discrepancies between text, plots, and tables. If a figure cannot be viewed, record that limitation rather than claiming visual verification. Do not treat a display subset as the analysis population.

Keep explanations close to what the measurements support. Exploratory enrichment, marker expression, correlation, or a prediction score alone cannot demonstrate mechanism, causal regulation, clinical usefulness, or independent validation. Put broader hypotheses in the Discussion and label them as hypotheses.

### Methods

Describe what was actually done and why that approach addresses the question. Match the prose to executed code, logs, environment records, and laboratory documentation; distinguish supplied author reports from details verified against execution records. Code presence alone does not prove that a step ran.

Include the details that affect interpretation or reproduction, as applicable: specimen and data provenance; eligibility and exclusions; biological units and pairing; assay/library preparation; preprocessing and normalization; reference genome and annotation; feature definitions; model, contrast, covariates, and dependence structure; statistical thresholds and multiplicity; software versions and consequential parameters; random seeds and train/evaluation separation.

Trace parameters to the actual run, including configuration overrides and documented version-specific defaults. State unavailable versions or settings as missing. Do not replace recorded choices with a more desirable method, justify an undocumented choice as historical intent, or claim a planned QC, control, sensitivity analysis, or validation was performed.

Organize methods so readers can locate the procedures underlying each result, without forcing identical headings or a fixed writing order. Cite checked original method sources where appropriate, and describe study-specific changes. A citation does not replace the details needed to understand this implementation.

### Discussion

Start with the bounded answer to the study question and the contribution supported by the Results. Explain how the observations change or constrain current understanding, then distinguish plausible explanations from tested mechanisms.

Compare with relevant literature actually inspected. Check that the cited work supports the specific statement and compare species, populations, assay meaning, design, and endpoints before claiming agreement or disagreement. If access or verification is incomplete, label that gap; do not imply a comprehensive literature review or novelty search was performed.

Connect limitations to the inference they restrict: for example, few independent donors limit precision, complete confounding prevents separating effects, and same-data discovery does not supply independent confirmation. Do not reduce material limitations to a generic closing disclaimer or conceal incompatible evidence.

Describe future work as proposals tied to unresolved questions. Keep expected outcomes conditional. Avoid priority claims such as “first,” broad generalization, or stronger causal and translational language unless the supplied evidence and checked literature warrant them.

### Other requested text and reviewer revisions

For an abstract, title, introduction, legend, or short revision, apply the same evidence boundaries at the appropriate level of detail. Do not draft those sections merely because Methods, Results, or Discussion were requested.

For reviewer-driven changes, connect the concern to the relevant evidence and actual revision. State whether a new analysis was completed, is proposed, or cannot answer the concern. Do not claim that a check was performed, that all concerns were resolved, or that evidence was added when it was not.

## Check and deliver

Reconcile the requested prose with its evidence: sample counts, denominators, direction, scale, values, interval meaning, figure/table labels, exclusions, software details, and citations. Preserve the distinction between exploratory and confirmatory work across all revised sections. Flag unresolved inconsistencies rather than smoothing them into a stronger story.

Keep scientific corrections separate from stylistic edits when that distinction matters for review. Preserve originals unless replacement is requested or established by the project workflow. Use the requested file format and destination, or provide the draft directly when no file is needed.

Deliver the requested text, concise evidence pointers, material unresolved items, and what was checked. State any limits on verification. A polished draft or successful document-format check does not establish reproducibility, statistical validity, biological validation, or readiness for submission.

## Source notes

For the origin and limits of the section-writing guidance, consult [writing-sources.md](references/writing-sources.md) when needed. Its sources inform communication structure; they do not supply biological findings or override the user's requested scope.
