# Lightweight analysis records and completion checks

Read this when choosing a record format or assembling final results. Reuse an existing notebook or analysis document if it contains what is needed. The templates below are optional; neither separate files nor every field are mandatory.

## Record one question

```text
Question / why it matters:
Verified inputs and meaning: location, source, sample/feature units, prior processing
Verified design / provisional assumptions / unknowns:
Decision: comparison, reference group, covariates, filters, aggregation, exclusion evidence
Timing: prespecified / post hoc exploration / error or experimental-information correction
Execution: code location, command, or notebook execution order
Observations: actual n, effects/units, uncertainty, warnings, before/after changes
Interpretation and limitations:
Next question and reason / information needed from the researcher:
```

## Minimum connections for a rerun

- Input sources and current versions or locations, with original and transformed data distinguished. Use checksums when exact file identity matters.
- Direct links between code, key parameters, and result tables or figures. Document required access permissions or external inputs as rerun conditions.
- Language, package, and reference-data versions that affect the results; seeds for stochastic operations and remaining nondeterminism. Do not force a complete system-package inventory on a small analysis.
- Script commands or notebook execution from the beginning. Record whether a clean rerun actually occurred and any failures. Running only selected successful cells is not full reproduction.
- What was checked by opening figures and what remains unresolved. Mark figures unreviewed if they could not be opened.

## Corrections and superseded results

Identify the correction's source, old assumption and new relationship, and affected code, tables, figures, and explanations. Preserve originals and distinguish corrected metadata and current outputs. Rerun the necessary calculations and mark prior results as superseded. Even if the estimated effect is unchanged, check n, uncertainty, tests, figures, and interpretation again.

## What the final report should retain

1. The question and current answer, including parts the data cannot answer.
2. Data, samples, and key actual observations. Where possible, report effects, units, uncertainty, and independent n together.
3. Methods and reasons for consequential choices, major before/after preprocessing changes, and whether analyses were added after seeing results.
4. The conclusion's scope and unresolved issues. Distinguish literature facts, current executed results, candidate explanations, and proposed follow-up work.
5. Locations of code, tables, figures, and records; rerun instructions; and actual execution, rerun, and visual-review status.
6. What to check next and the uncertainty that check would reduce.

Before closing, check whether the researcher can explain the question, data, reasons for choices, observations, limitations, and next check. Provide evidence and artifacts instead of success labels. Software or format checks, synthetic examples, scenario review, analysis of real data, and independent biological validation are different levels of evidence.
