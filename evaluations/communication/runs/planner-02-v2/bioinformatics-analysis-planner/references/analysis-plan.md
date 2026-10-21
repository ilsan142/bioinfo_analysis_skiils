# A reviewable analysis plan and handoff

Read when assembling a plan or handing it to an analysis agent. Use one existing record or `analysis_plan.md`; this is an adaptable outline, not a demand for every heading or a separate file per section.

## Compact plan outline

### Question and scope

State the biological question, population, independent unit, comparison direction, outcome and units, and the intended kind of conclusion. Separate the primary question from optional exploration. Say whether outcome results have already been seen and whether the current request includes execution beyond feasibility checks.

Explain why resolving the question matters for the present research decision. Use supplied context or checked literature; do not add an unsupported novelty claim. If the goal is exploratory, an honest description of what is not yet understood is sufficient.

### What is known

| Evidence or issue | Source and inspection scope | Consequence for design |
| --- | --- | --- |
| Verified input meaning and prior processing | Actual data dictionary or generation record; distinguish inspected content from reported metadata | Which input requirements are satisfied |
| Verified sample relationships and coverage | Identifier/replicate checks actually run; counts with units | Which comparisons and paired or dependent structure are possible |
| Provisional assumption | Evidence supporting it and how to check it | Which recommendation changes if false |
| Unresolved information | Where it was sought | Which step is blocked and what can continue |

Replace these illustrative rows with the present evidence. Do not repeat every technical diagnostic in the main plan; show what affects decisions and retain details with the probe code if needed.

### Recommended route and decisions

Use one row per meaningful question, or short paragraphs when clearer.

| Question | Proposed check/method and why | Evidence to inspect | Decision and next step |
| --- | --- | --- | --- |
| Can measurements be assigned to the intended samples? | Compare all relevant keys and their uniqueness before joining | Counts of matched, unmatched, and duplicate keys | Proceed with the verified join; resolve ambiguous keys before estimating group differences |
| Can the target contrast be identified? | Inspect independent units and condition-by-batch coverage; design rank if relevant | Counts with experimental units and any dependent model terms | Estimate only supported contrasts; otherwise describe the combined difference and request crossed observations |

These are examples, not compulsory steps when equivalent checks are already verified. Continue the table with only the questions needed for the present goal. State the actual comparison, scale and covariates, or the unresolved prerequisite that prevents choosing them. For each proposed figure, say what the researcher will be able to judge from it.

### First executable step

Name the next question, input paths, minimal action, expected output type, and the rule for interpreting that output. If this check has already run, give its observed result and advance to the next unresolved question. Do not label an already completed check as pending or repeat it without a reason.

If execution is blocked, name the missing field/file/decision precisely and give a feasible independent step. For a planning-only request, a complete handoff is the endpoint; do not begin the full analysis merely because the next step is specified.

### Completion, limits and revisions

Define what the later analysis must deliver: an answer at the supported level, effect and uncertainty where defensible, transparent exclusions, reviewed figures, and rerunnable code with input/method provenance. State which conclusions the design cannot establish and the most useful additional information.

Keep a short dated note for material changes: what changed, new evidence, affected steps and outputs, and whether results had already been inspected. Preserve prior agreements and source facts without generating a separate versioned plan file for every minor edit.

## Examples of conditional choices

- **Paired observations:** If records and IDs establish the same donors under both conditions, preserve those pairs in the proposed comparison and count donors as the independent unit. If pairing remains unknown, inspect identifiers and distributions but defer a paired or independent model choice. Do not invent pairs or default to a test merely because it runs.
- **Complete condition/batch overlap:** Allow descriptive summaries of the observed combined difference. Withhold claims about a separable treatment effect and specify the need for conditions crossed within independent batches. A different correction algorithm does not create that design information.
- **Unknown expression scale:** Preserve fractional values and inspect provenance. Make normalization and modeling conditional on the generating process and prior transformations; do not round values or assume TPM from decimals.
- **Biological prediction:** If the goal is new-patient performance, plan patient-separated evaluation with learned transformations fitted on training data. If only a split manifest is available, audit overlap now and leave performance estimation unexecuted.

## Reader check before delivery

Can a researcher unfamiliar with the files explain why the recommended comparison is supported, what could invalidate it, and what will be checked next? Can the executing agent begin that step without inventing biological facts or silently choosing among unresolved objectives? If not, make the relevant assumption or decision explicit rather than adding more tools to the plan.

## Probe output that explains the decision

Keep purpose and meaning in the reusable probe itself, not only in the final prose. For example, after checking donor relationships and preparing a condition-by-batch count table, the output code might read:

```python
print("Check whether both conditions occur within batches, so treatment and batch can be distinguished.")
print("Counts below are independent donors, not cells or measurement rows.")
print(donors_by_condition_and_batch)
```

Use the user's language in a real task. This is an illustrative display fragment, not an executed check or a prescribed library. Construct the table from verified units, inspect the actual values, and then explain their consequence. Group one purpose with its coherent summary; do not print a full diagnostic dictionary or repeat a caption for each scalar. Preserve failures and missing information that affect the design, even when routine successful checks are summarized compactly.

## Explain what the plan will let the researcher decide

For a consequential proposed check, connect **current uncertainty -> discriminating evidence -> possible decisions**. Include an ambiguous result when it is plausible. Do not invent numerical thresholds just to fill a decision table.

For example, a plan to compare donor-level expression should say whether the question concerns a consistent within-donor difference or a pooled cell-level pattern. If effects are consistent across donors, report their magnitude and uncertainty at the donor level. If they differ materially, inspect prespecified context or clearly labeled exploratory explanations. If too few informative donors remain, narrow the conclusion and state what additional independent observations are needed. None of these branches guarantees a discovery or proves a mechanism.

State how each optional analysis would resolve a particular ambiguity before adding it. A failed check can justify revising the question, obtaining missing records, or stopping an unsupported claim; it need not trigger a search through more methods. An inconclusive but well-supported answer meets the scientific purpose better than a promised significant result.

For a review meeting, make the requested decision explicit only when the researcher must choose: for example, which biological target to prioritize or which additional experiment would resolve a design limitation. Routine implementation already authorized does not require a new approval step.

Communication sources checked on 2026-10-21:

- [MIT BE Thesis Proposal](https://mitcommlab.mit.edu/be/commkit/be-thesis-proposal/): connect purpose, rationale, feasible approach, completion criteria, and alternatives.
- [Broad Slideshow](https://mitcommlab.mit.edu/broad/commkit/slideshow/): adapt the explanation to its audience and the feedback sought.

These sources guide explanation, not statistical validation. The planning rules are original operational applications; no proposal text or source figures are reproduced. Do not transfer thesis-specific novelty requirements, document lengths, or persuasive claims to routine exploratory planning.
