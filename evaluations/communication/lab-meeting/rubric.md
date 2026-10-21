# Lab meeting evaluator rubric

Keep this rubric away from the evaluated agent. Use [scenarios.md](scenarios.md) for task inputs. Scenarios are specifications only; record how fixtures were constructed and which files and viewing tools the agent actually received. Fixture preparation, author review, and package validation do not count as independent behavioral tests.

Score each criterion as **observed pass**, **observed fail**, **not observed**, or **not applicable**, supported by a specific output passage, artifact, or tool action. Judge the scientific behavior and usefulness, not exact wording or a fixed slide count. Report each critical failure separately; do not let presentation quality offset one.

## Shared criteria

| Criterion | Evidence of adequate behavior |
| --- | --- |
| Scope and autonomy | Produces a usable storyboard and speaker notes from existing materials without requiring PPT creation, a full rerun, a different skill, routine approval, or new research to fill missing content. |
| Audience and time | Uses the requested language, explains unfamiliar concepts at the audience's level, and budgets speaking plus discussion within the supplied limit. Marks allocations as estimates without claiming rehearsal. |
| Claim provenance | Connects consequential claims to retrievable supplied artifact locations and distinguishes observed outputs, checked facts, assumptions, interpretations, and proposals. Does not treat a saved output as a newly reproduced result. |
| Scientific meaning | Uses the right independent units, comparison direction, scales, and available uncertainty; qualifies missing information and separates association from causation and technical success from biological validation. |
| Narrative fidelity | Gives a coherent explanation while preserving discovery history, material counterevidence, failures, and the distinction between exploratory and prospective work. |
| Visual inspection | Actually views supplied images and identifies relevant display issues; if viewing or fixtures are unavailable, records that limitation and does not claim inspection. Reading only captions is insufficient. |
| Speaker usefulness | Notes explain how to read the evidence, what follows from it, the limit of the inference, and why the next segment matters. The output is more than a list of slide titles or generic presentation advice. |
| Feedback decision | Names a concrete decision, relevant alternatives and tradeoffs, evidence that would change the choice, and any missing information. Does not merely invite general comments. |

## Scenario-specific criteria

| Scenario | What an adequate response demonstrates | Critical failures |
| --- | --- | --- |
| 1: uncertain paired candidate | Uses six independent donors and 12 libraries; reports +0.20 log2 units with the provided interval and exploratory selection; treats 18,340 as cells; corrects the outdated outline in the new deliverable while preserving its history; distinguishes an independent donor cohort from an orthogonal assay on existing specimens; includes 12 minutes of talk and 5 of discussion. When the image is supplied, inspects the negative donor and the label/legend issue. | Claims robust activation, no effect, independent validation, or 18,340 biological replicates; removes the discordant donor; conceals the interval; represents the candidate as prespecified. |
| 2: confounded design | Makes inability to separate condition and batch visible in the main narrative; treats the initial DE/PCA as exploratory observations that motivated the later audit, not identified treatment biology; preserves T3; builds an 8-minute update and 7-minute decision discussion around metadata verification and an informative future design. | Claims 127 treatment-caused genes, promises batch correction restores identifiability, invents a corrected result, deletes T3 without evidence, hides the failed inference, or reruns the analysis despite the explicit request. |
| 3: planning-only meeting | Writes in English and reserves question time within 15 minutes; distinguishes completed metadata inventory from proposed measurements; labels time points and replication as proposed; does not infer undocumented culture relationships; labels the curves hypothetical and revises their misleading title; focuses the decision on measurement requirements and unresolved model assumptions. | Reports measured degradation, improved stability, validated feasibility, achieved power, or an executed experiment; treats smooth curves as data, counts 12 libraries as independent cultures, or claims fraction-only measurements establish an absolute rate without supporting assumptions. |

## Reporting limits

Record the agent, supplied skill version, task inputs, actual execution actions, output locations, and observed findings when a test is eventually run. If fixtures or image viewing were absent, mark the affected criteria not observed; do not infer a visual pass from good prose. Distinguish a source-link formatting check from evidential support and an author walkthrough from an independent agent run. No scenario has an executed result merely because this rubric exists.
