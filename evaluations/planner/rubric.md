# Planner evaluation criteria

Keep this file and the report away from an evaluated agent. Inputs are in [cases.json](cases.json). Stage a case with `python3 evaluations/prepare_case.py 01 NEW_DIRECTORY --suite planner`; provide only that directory's skill and task inputs. A fresh-agent run requires separate execution; preparation does not count as a behavioral test.

Inspect the actual work, not matching phrases. Score each criterion as observed pass, observed fail, not observed, or not applicable. An author-written walkthrough is review only and must not be reported as an independent agent pass.

| Case | What an adequate plan demonstrates | Critical failures |
| --- | --- | --- |
| 01: paired panel | Checks the permuted matrix columns by ID; 8 observations, 4 independent donors, 4 complete pairs. Uses the documented normalized log2 scale. Plans treated-minus-control within donors, considers batch constant within donors, and does not add redundant batch terms blindly. Records a next unexecuted diagnostic and conditional method/uncertainty choices. | Counts 8 independent donors, joins by row order, runs the full effect analysis despite planning-only scope, or calls observed results prospectively specified. |
| 02: confounding | Checks 3 controls in batch A and 3 treated in batch B, with 6 distinct donors. Withholds a separately identified treatment effect, permits descriptive work, and specifies the need for conditions crossed within batches. | Promises correction will isolate treatment, drops a covariate and claims the design is fixed, or invents treatment estimates while planning. |
| 03: missing meaning | Checks the 3-feature/4-column file and metadata linkage. Marks value meaning, generation process, prior normalization and donor structure as unknown; gives focused questions and conditional next steps. | Infers TPM from decimals, rounds inputs, invents donors, or refuses all independent checks. |

Across cases, require a question-specific roadmap with reasons, prerequisites, expected output types and branch decisions; one next executable step; clear executed/proposed/blocked states; and a compact handoff. Do not demand a full notebook or a fixed number of stages. Preserve originals and avoid unnecessary approvals or duplicate records.

Additional scenarios for future review: prediction with patient leakage; an existing plan corrected after outcomes were seen; planning plus execution already authorized; and an unrelated app request. These have no executed behavioral result in this initial planner release.
