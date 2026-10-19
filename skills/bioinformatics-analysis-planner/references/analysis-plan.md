# A reviewable analysis plan and handoff

Read when assembling a plan or handing it to an analysis agent. Use one existing record or `analysis_plan.md`; this is an adaptable outline, not a demand for every heading or a separate file per section.

## Compact plan outline

### Question and scope

State the biological question, population, independent unit, comparison direction, outcome and units, and the intended kind of conclusion. Separate the primary question from optional exploration. Say whether outcome results have already been seen and whether the current request includes execution beyond feasibility checks.

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
