# Calibrating a scientific figure review

Use the examples that match the task. They are hypothetical illustrations, not findings about the user's figures.

## Findings with bounded evidence

| Location | Observation and evidence | Impact | Proposed fix | Severity |
| --- | --- | --- | --- | --- |
| Figure 2A, caption sample count | The caption calls 600 cells independent replicates, but the supplied sample table assigns them to three donors. The plotting table identifies dots as donor means. | Readers may confuse the amount of cell sampling with the independent biological replication and misidentify the plotted units. | State three donors, the cell count, and that dots show donor means. Ask which unit supplied the reported uncertainty; do not declare its calculation wrong without inspecting it. | Major; replication-label mismatch confirmed, uncertainty calculation unresolved. |
| Figure 2B, vertical axis | The axis says “expression”; the supplied plotting table documents log2(normalized expression + 1). | The scale and size of a difference cannot be interpreted reliably. | Add the documented scale and normalization label, with details in the caption if necessary. | Major when this changes the biological reading; otherwise minor. |
| Figure 3C, lower-right annotation | In the rendered export, the last line of the condition label extends beyond the panel boundary. | One group cannot be identified completely. | Widen the label area or wrap the text, then inspect the new export at its target size. | Minor, or major if the group becomes ambiguous. |
| Figure 4A, shaded interval | The caption does not define the band; no supporting methods or data were supplied. | Readers cannot tell whether it represents variability, estimation uncertainty, or another quantity. | Name the interval, its level where relevant, and its unit of calculation after checking the analysis record. | Major evidence gap; not evidence of an incorrect interval. |
| Figure 5, density display | Hexagonal bins are labeled as counts, and the caption distinguishes all observations from independent donors. | No demonstrated defect follows from the chart type itself. | Retain it unless the user's audience or task calls for another display. | No finding solely for using hexbin. |

Distinguish **confirmed**, **unverified**, and **not assessable with supplied materials** in prose. A missing definition can be a confirmed reporting omission even when the underlying calculation is unknown. Do not label an unverified numerical suspicion critical.

## Compact source table

| Material | Review method | Supports | Limits |
| --- | --- | --- | --- |
| `figure2.pdf`, page 1 | Opened rendered page and enlarged A–C | Layout, visible labels, legend mapping, clipping | Cannot recover exact source values reliably |
| `figure2-caption.txt` | Read text | Declared message, reported sample sizes and interval definitions | Descriptions may disagree with code or data |
| `sample_summary.tsv` | Checked donor/condition records and field meanings | Documented grouping, pairing, and counts | Does not establish unseen raw-data quality |
| Analysis code unavailable | Not inspected | None | Numerical validity and implementation remain unverified |

Use actual paths, versions, and inspection methods. Never report an artifact as viewed because the renderer merely produced it. A rendering failure belongs in the review limitations, with any independent checks still completed.

## Review with incomplete supporting materials

For a screenshot with a caption but no data, review the visible axis labels, interval definitions, group distinctions, title strength, and clipping. State which judgments remain limited by screenshot resolution and missing analysis records. Do not infer undisclosed normalization, biological replication, image processing, or significance from the pixels.

Prefer a concrete statement such as “Panel B's caption does not identify the error bars; specify the quantity used” over “The statistics are invalid.” If the caption already defines them and nothing contradicts it, do not manufacture a warning. A useful review may conclude that no major problems were demonstrated.

If a review suggests an analysis concern, describe its implication and the minimum evidence needed to resolve it. Do not run a new test, change exclusions, alter the statistical model, or withhold all figure feedback until reanalysis is authorized.

## Redesign when requested

Choose a design that exposes the comparison: paired subject values for matched experiments, sample points with summaries for small groups, distributions when shape matters, and lines for genuine ordered time courses. These are options, not mandatory substitutions. A heatmap needs interpretable values and color scale; a scatter plot needs meaningful observation units.

For crowded points, consider size, transparency, or meaningful facets first. Disclose any display subset and its selection rule without implying that the analysis used the subset. Do not add hexbin unless requested, but do not remove an existing hexbin solely because of this presentation preference.

Keep scientific and presentation revisions distinct. Rewording an unsupported causal title as an association can be proposed during review; estimating a causal effect is new analytical work. Adding paired connecting lines can clarify a design without proving that an existing test used pairing.

## Checked sources and adaptation limits

Sources checked on 2026-10-21. These pages inform communication choices, not statistical validation. Their overlapping content is not independent scientific corroboration. No source illustrations or extended passages are reproduced here.

| Source | Ideas used | Limits of application |
| --- | --- | --- |
| [MIT Broad Communication Lab — Figure Design](https://mitcommlab.mit.edu/broad/commkit/figure-design/) | Align a figure's message with visible evidence; consider audience and medium; make panel structure and visual emphasis support the comparison. | Clear storytelling does not justify omitting contradictory results, controls, or uncertainty. Its chart suggestions are contextual options, not fixed rules. |
| [MIT Biological Engineering Communication Lab — Figure Design](https://mitcommlab.mit.edu/be/commkit/figure-design/) | Choose displays according to comparisons or distributions; adapt detail to papers, posters, and talks; reduce clutter and improve legend placement. | Follow the user's venue and scientific needs rather than enforcing a universal caption format or removing information needed for interpretation. |

The sources identify CommKit content as CC BY-NC 4.0 unless otherwise noted. This reference links to and briefly paraphrases their design guidance; it does not bundle their figures. Rules about independent units, pairing, data verification, review scope, and hexbin preference are this skill's operational guidance, not claims that these pages prescribe them.
