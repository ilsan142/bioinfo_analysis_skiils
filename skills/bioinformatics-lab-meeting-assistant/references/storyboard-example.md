# A lab meeting built around an unresolved result

Read this example when uncertainty makes the central message or feedback request difficult to frame. The example and all numbers below are synthetic teaching material, not executed research or a fixed presentation template. Artifact locators illustrate the precision to use with real supplied files; these files are not bundled.

## Worked example

The presenter has ten minutes for an update and five for discussion. The audience knows the biology but includes researchers unfamiliar with single-cell statistics. A saved analysis reports six independent donors with paired control and treated samples, 18,340 retained cells, and a donor-level expression contrast of +0.20 log2 units with a reported 95% bootstrap interval of −0.05 to +0.44. The target was selected after inspecting these data; no independent confirmation exists.

The meeting's purpose is to decide what evidence is needed before prioritizing the candidate. A suitable central message is: “The exploratory estimate is positive, but the current donor-level uncertainty does not establish its direction.” The large cell count explains the measurement volume; it does not increase the number of independent donors.

| Segment | Evidence and speaking approach | Time estimate |
| --- | --- | --- |
| Why this candidate is being considered | Introduce the biological question from `analysis-plan.md`, question Q1. Say the candidate emerged during exploration; do not imply it was the prespecified primary endpoint. | 1 minute |
| What was measured and what is independent | Use the sample map in `paired_update.ipynb`, cell `sample-map`. Explain six donor pairs, the expression scale, and the difference between a cell and a donor. | 2 minutes |
| What the current estimate can support | Show the actually viewed donor-effect panel from `figures/paired_target.png`, linked to `results/target_summary.tsv`, row `target_A`. State the contrast, interval method, and uncertain direction together. | 3 minutes |
| What would change the decision | Compare the alternatives already documented in `analysis-plan.md`, section `Next evidence`: independent donor replication versus an orthogonal assay on the same specimens. Explain which uncertainty each addresses without claiming either has been performed. | 4 minutes |
| Decision for the group | Ask which uncertainty should be reduced first given available samples, and whether that choice supports replication, assay validation, or both. Record the scientific criterion needed for later prioritization. | 5 minutes of discussion |

Example speaker notes for the result segment:

“Each value summarizes a donor's treated-minus-control difference on the reported log2 scale. The estimate is +0.20, and the saved donor-level bootstrap interval includes both a small decrease and an increase. These data therefore leave direction uncertain. The target was chosen after exploring the dataset, so this is a candidate for follow-up. The next choice depends on whether we most need evidence of reproducibility across donors or evidence that the measurement itself is reliable.”

In a real task, inspect the plot before including it. If the file cannot be viewed, retain the table-supported statement and mark the figure review incomplete. A proposed follow-up sketch must be labeled as a proposal. A different target with a null result or a sample contradicting the main trend cannot be removed merely to strengthen this story.

If the original design instead has all controls in one batch and all treated samples in another, the interpretation changes: a difference cannot be attributed separately to treatment from these data. Make that limitation part of the main message and use the discussion to choose an informative design or recover missing records. Do not present batch correction as proof that the treatment effect was recovered.

## Checked communication sources

Sources checked on **2026-10-21**. These are communication references, not evidence for the synthetic biological example or validation of this skill. The overlapping pages are related guidance, not independent corroborating studies.

- [Broad Institute of MIT and Harvard Communication Lab: Slideshow](https://mitcommlab.mit.edu/broad/commkit/slideshow/). The page connects presentation purpose and audience to the selection of evidence, and recommends orienting listeners to a figure before interpreting it. It credits an earlier MIT Biological Engineering Communication Lab article. The skill applies these principles by linking the meeting decision to selected artifacts and explaining observation units before claims.
- [MIT Biological Engineering Communication Lab: Slideshow](https://mitcommlab.mit.edu/be/commkit/slideshow/). The page, marked updated July 2026, discusses explicit feedback goals, message-bearing titles, spoken preparation, pacing, and logical transitions. The skill uses these principles for flexible storyboards and notes; it does not turn a pacing heuristic into a required slide count.

The instructions and example here are newly written. No source figures, sample slides, or source passages are reproduced. Both source pages identify their CommKit content as licensed under Creative Commons Attribution Non-Commercial 4.0 unless otherwise noted.
