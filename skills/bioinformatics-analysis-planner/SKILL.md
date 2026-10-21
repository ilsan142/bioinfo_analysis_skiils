---
name: bioinformatics-analysis-planner
description: Design or revise a bioinformatics analysis plan from available data and experimental records. Use when the researcher asks how to analyze a dataset, which questions and comparisons it can support, which methods to prioritize, or how to turn a research goal into a conditional analysis roadmap. Inspect inputs as needed and produce a reviewable plan with decision points and a first executable step. Do not use for unrelated app planning or require a separate planning phase for routine analysis execution.
---

# Plan a bioinformatics analysis from the evidence

## Purpose and scope

Produce a scientific analysis design that the researcher can review and an analysis agent can act on. Success means connecting **the biological question, actual data, independent experimental units, feasible comparisons, reasons for method choices, decision points, and the next executable step**. A list of tools or a polished plan without input evidence is insufficient.

Use this skill for an explicit planning deliverable or a substantive redesign. It applies across omics and biological prediction without prescribing one pipeline. Follow the user's language, defaulting to Korean when no preference is apparent. Explain for a researcher familiar with the biology, without assuming implementation expertise.

For a planning-only request, read records and run small, non-destructive feasibility checks when permitted: inspect schemas, identifiers, counts, missingness, value ranges, replicate relationships, and design cross-tabulations. Stop once these checks support a useful conditional plan. Do not fit outcome models, run differential expression, cluster the full dataset, train predictors, or complete a pipeline merely to write a plan. If code execution is disallowed or unavailable, state exactly what was inspected and keep dependent choices conditional.

Planning is not a compulsory approval stage. If the user already requested both design and execution, finish a concise design and continue the authorized analysis. If they requested only a plan, delivering it completes that scope. Do not invent a requirement to approve every routine step.

## 1. Establish the question and available evidence

Read project rules, prior plans, notebooks, data dictionaries, experimental records, and previous decisions before asking questions. Reuse a suitable existing plan. Record if outcome results have already been inspected; a plan written afterward is not a prospective or preregistered analysis.

State the primary question in plain language: **which population or biological units, what comparison and direction, which outcome or quantity, and what kind of conclusion is sought?** Distinguish description, association, prediction, and causal interpretation. Keep secondary or exploratory questions separate and limited to those relevant to the goal. If only data are provided, propose a small number of supported questions and a reasoned priority; do not silently invent the researcher's intent.

Connect the question to the uncertainty or research decision it would resolve. Use existing context to explain why that matters; do not invent novelty, a literature gap, or a fixed hypothesis for exploratory work. Tailor the explanation to the person reviewing the plan, and identify a requested scientific decision only when one is actually needed.

Inspect only what changes the design. Establish:

- File locations and provenance; what rows, columns, identifiers, values, and units represent; generation and previous processing; relevant species, tissue, treatment, time, reference versions, and annotation.
- The independent experimental unit and observation unit; biological versus technical repeats; paired, repeated, nested, spatial, or related-sequence structure.
- Sample matching, duplicates, missingness, zeros, usable measurements, and per-comparison coverage. Report the actual scope of inspection: metadata, file headers, a subset, or complete inputs. A subset does not establish global identifier integrity.
- Batch, institution, time, and other design variables; whether groups and covariates overlap enough to support the requested comparison.
- Existing methods, software, compute and access constraints that materially affect feasibility. Do not install a large environment or download substantial data for a planning-only task.

Classify evidence as **verified fact with a source, provisional assumption with a reason, or unresolved question with its consequence**. Do not infer raw counts from integers, independent donors from file names, or pairing from row order. Preserve original inputs. Before showing probe output, explain why it matters; use labeled summaries instead of file inventories or identifier dumps. For printed values, print the purpose first. Read actual outputs before choosing dependent checks.

Keep this explanation in the executed probe code when that code is preserved for rerunning; prose added only to the final plan does not explain a bare output on rerun. Show decision-relevant counts or cross-tabulations instead of dumping an entire diagnostic dictionary. The [probe example](references/analysis-plan.md#probe-output-that-explains-the-decision) illustrates the intended level of detail.

## 2. Decide what the data can support

Identify the most consequential obstacle before recommending methods. Apply only relevant rules:

- **Measurement compatibility:** Distinguish observed/estimated counts, relative abundance, normalized measurements, and transformed values. If their meaning is unresolved, defer the dependent model; do not plan rounding, arbitrary imputation, or repeated normalization to satisfy software.
- **Replication and dependence:** Specify the independent n for each proposed comparison, including loss of pairs or sparse strata. Many cells, reads, spots, or visits do not replace independent biological replication. Select an aggregation or dependence-aware strategy only after checking relationships.
- **Identifiability:** Check whether condition can be separated from batch, donor, time, or other relevant variables. With complete confounding, describe what remains observable, what inference must be withheld, and what crossed observations would resolve the problem. Do not make batch correction a promised solution.
- **Preprocessing and exclusions:** Give each filter or transformation a purpose and evidence requirement. Treat unverified thresholds as provisional. Specify what will be inspected before fixing them and what would trigger sensitivity analysis. Do not choose exclusions or thresholds to improve significance.
- **Inference:** Define contrast direction, necessary covariates, uncertainty reporting, and the proposed multiple-testing family when applicable. Distinguish an effect worth studying from statistical significance. Do not promise power, discovery counts, confidence-interval width, or future results without defensible inputs.
- **Prediction:** Define the intended generalization unit, split units, and held-out evaluation before choosing models. Plan learned preprocessing and feature selection within training folds. Keep repeated people, sites, times, or related sequences separated as required by that target.
- **Interpretation:** Match annotation, mapping and measurement limits to the claim. Plan how composition, sparse coverage, or alternative explanations will be assessed when they could change the conclusion. A plot, marker, enrichment, or successful model fit is not a mechanism test.

Choose one recommended starting route and only consequential alternatives. Give the reason and prerequisite for each choice. Check official method documentation or original papers when a specific methodological claim requires evidence; record what was actually consulted and any unavailable source. Do not turn planning into an exhaustive literature review or catalog of tools.

## 3. Build a conditional sequence of scientific questions

Organize the roadmap by questions, not code cells or a mandatory sequence such as normalization, PCA, clustering, enrichment. Each step should state:

1. The question and why it is needed for the research goal.
2. Required inputs and assumptions, with evidence already available.
3. The minimal proposed check or method and its rationale.
4. The evidence to inspect: a labeled table, estimate with units and uncertainty, diagnostic, or purposeful figure.
5. How that evidence changes the decision: continue, revise a particular choice, request missing experimental information, or stop the unsupported inference.

Describe **expected output types**, not invented outcomes. Prefer familiar figures that expose the comparison and experimental units; do not propose hexbin unless explicitly requested. A small table is often sufficient for a design check.

For consequential branches, explain what plausible contrasting outcomes would change, including an inconclusive result or a failed assumption. State which explanations the proposed check can distinguish and which it cannot. Choose alternatives because they address a defined obstacle; do not promise a favorable result or treat significance as the only success criterion. The [plan guide](references/analysis-plan.md#explain-what-the-plan-will-let-the-researcher-decide) gives a compact decision-focused example.

Make the first unresolved step executable now: name its input paths, check, and decision criterion, with a small code snippet or existing command if helpful. Leave later choices conditional on results. Do not prewrite a full analysis pipeline. Bound sensitivity checks to specific uncertainties and retain the primary comparison rather than enumerating every possible parameter combination.

## 4. Resolve necessary questions and hand off the plan

Ask only when the answer changes the biological target, replicate interpretation, exclusion decision, or another consequential branch. First summarize the facts already checked, the missing information, the implications of plausible answers, and a recommendation where justified. Continue unrelated feasibility work while waiting. Preserve existing agreements; autonomous planning does not authorize inventing biological facts.

Save one concise plan in the existing analysis record, or use `analysis_plan.md` if no suitable record exists. Do not create a notebook, multiple logs, or a configuration framework solely to house a short plan. If probes were executed, preserve enough code, inputs, output evidence and environment information to reproduce those checks, preferably in the same record or an existing notebook.

Read [analysis-plan.md](references/analysis-plan.md) when writing the deliverable or handing it off. Adapt its outline; omit irrelevant sections. The final plan must make these clear:

- The question, comparison and claim boundary; known facts, assumptions, and decision-relevant unknowns.
- The recommended route, the rationale and branches that can change it, and the first executable step.
- Which checks actually ran, what they found, and which analyses are proposed or blocked.
- What a completed analysis must show, its key limitations, and what additional information would reduce them.

Indicate readiness for the **next step**, not a blanket declaration that the study is valid. If the data cannot identify the intended effect, a plan for descriptive work plus a clear missing-data requirement is a valid result.

When execution is authorized, pass the plan and its evidence to the analysis workflow. If available, `bioinformatics-research-assistant` can implement it question by question; it is not required to install or use this planner. The executing agent should inspect results before implementing dependent steps, retain agreed choices, and update the plan when evidence changes a branch. Record the reason and timing of material revisions. Do not rerun planning at every cell or treat the plan as an immutable pipeline.
