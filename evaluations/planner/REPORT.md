# Bioinformatics analysis planner: initial validation

Date: 2026-10-19. This report concerns `bioinformatics-analysis-planner`. It does not extend earlier research-assistant behavioral results to the new skill.

## What ran

- Prepared the three synthetic tasks using `prepare_case.py --suite planner`, then executed [probe_inputs.py](probe_inputs.py) on their actual staged files. [feasibility_checks.json](feasibility_checks.json) retains results, input hashes, runtime version, skill hashes and preparation checks.
- Case 01: 3 features, 8 matched observations, 4 distinct donors, 4 complete pairs; both conditions present in each batch.
- Case 02: 2 features, 6 matched observations, 6 distinct donors; control only in batch A and treated only in batch B.
- Case 03: 3 features, 4 matched observations; donor and batch fields unavailable. No measurement type was inferred from fractional values.
- Confirmed the existing preparation command still stages the research-assistant suite, existing destinations are not overwritten, invalid case IDs fail before writing, and scoring material is excluded from staged tasks.
- Checked both skills with the skill-creator format validator and the repository validator, including metadata, English-only distributed instructions, local links, Markdown fences and task-input structure. These are packaging checks, not scientific validation.

The probes inspect schemas, identifiers and metadata relationships. They do not estimate effects, fit a model, calculate p-values or determine that the underlying measurements are scientifically valid.

## Review based on those results

The author wrote [plan walkthroughs](plan_walkthroughs.md) after reading the probe results, preserving the distinctions between completed checks, proposed next steps and blocked inference. The paired case retains donor pairing; the confounded case restricts the claim and identifies missing crossed observations; the missing-meaning case defers model and normalization choices.

This is **author review with executed feasibility checks**, not a blind agent evaluation. Expected design choices were known to the author. No case is assigned an independent behavioral pass.

## Not yet tested

- A fresh agent choosing and following the planner without evaluator guidance.
- Planning-to-execution handoff between separate agents or installed product clients.
- Automatic skill selection, including avoiding unrelated app planning or unnecessary planning before routine execution.
- Prediction leakage, changes after seeing outcomes, and explicit requests for planning plus execution.
- Scientific validity on real research data or reliability across models.

Use [cases.json](cases.json) as task inputs and keep [rubric.md](rubric.md) separate for a future independent evaluation. Do not reuse these author-written plans as expected outputs shown to the evaluated agent.

## Reproduce a feasibility probe

From the repository root, select a new directory:

```bash
python3 evaluations/prepare_case.py 01 /tmp/planner-case-01-new --suite planner
python3 evaluations/planner/probe_inputs.py /tmp/planner-case-01-new
python3 evaluations/validate_package.py
```

The first two commands use the Python standard library. The repository validator additionally requires PyYAML. Preparing and probing a fixture does not execute an agent.
