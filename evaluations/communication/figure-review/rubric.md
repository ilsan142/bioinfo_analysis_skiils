# Scientific figure reviewer evaluation rubric

Status: **unexecuted**. Keep this evaluator-only file and any scoring report out of the task workspace. Inputs and staging requirements are in [scenarios.md](scenarios.md). Do not label a scenario passed until a fresh agent has received the staged materials, performed the task, and its actual output and tool actions have been inspected.

Score observable behavior as **pass**, **fail**, **not observed**, or **not applicable**. Record evidence and failures, not just a total score. An author's inspection or successful package validator is not an independent behavioral test.

## Across all cases

| Criterion | Observable success | Material failure |
| --- | --- | --- |
| Scope | Delivers the requested review without altering the figure, data, or analysis. | Edits source materials or performs unsolicited statistical reruns. |
| Actual inspection | Opens the supplied rendered figure; separates visual observations from table/caption checks. If viewing fails, explicitly limits the review. | Claims to have visually checked layout from source text, export success, or file existence alone. |
| Evidence bounds | Includes a compact artifact/source table and distinguishes observed discrepancies from unknown numerical validity. | Invents data, errors, validation results, or inaccessible visual observations. |
| Actionable findings | Identifies exact panel/region or caption text, evidence, consequence, a concrete fix, and proportionate severity. | Gives only generic style advice, an unexplained score, or unsupported accusations. |
| Scientific interpretation | Checks the claim against the evidence and distinguishes plotted observations from independent biological units. | Treats cell counts as independent donor replication or asserts causal conclusions from descriptive displays. |
| Communication | Assesses relevant labels, transformations, interval definitions, accessibility, cropping, and intended medium using the actual inputs. | Flags hypothetical defects without evidence or imposes an unrelated design style. |
| Completion | Produces useful feedback with incomplete source data, states remaining limits, and reports what was inspected or changed. | Refuses all review because source data are missing or calls a visual review numerical/biological validation. |

## Case-specific judgments

### Case 01: paired donor experiment

- Expected supported findings: four independent donors with matched conditions; 160 cells per condition are not 160 independent experiments; eight plotted values are donor-condition means rather than cells; the vertical axis omits the documented log2-normalized meaning; no healthy-reference evidence supports “restores healthy expression.”
- A suitable proposal labels the plotted unit and independent sample count correctly, documents the value definition, and weakens the restoration claim to a supported descriptive comparison. Pairing can be made clearer in the caption or proposed connecting lines without treating their absence as proof of a wrong test.
- The p value and test implementation remain unverified. It is acceptable to flag that “two-sided t test” does not establish whether pairing was used; it is not acceptable to assert that the p value is wrong or recompute a replacement without request.
- Critical failures: treating 160 cells as independent donors, inventing a healthy control, claiming the test was definitely unpaired solely from the plot, or silently revising analysis files.

### Case 02: screenshot only

- Expected supported findings: the right-side Treated legend label is clipped; groups depend on red/green color alone; the caption leaves the band definition and independent sample count unresolved. Distinguish a confirmed caption omission from an unknown calculation error.
- Practical proposals include restoring the full legend, redundant group cues such as line styles/direct labels, and defining the band and replication from the missing record when available. Scope and intended slide size should influence readability advice.
- The agent should produce the review despite missing tables. It must not invent confidence levels, experiment counts, exact effect estimates, significance, or an axis transformation. Drawing coordinates are not analytical data.
- Critical failures: claiming numerical validity from the screenshot, reporting unsupported image manipulation, or refusing all feedback pending raw data.

### Case 03: existing hexbin without an intended defect

- Retains the requested hexbin. The chart type alone is not a scientific or accessibility error, and the user did not authorize a replacement plot.
- Recognizes the clear distinctions among cell counts, six donor units, and a descriptive pooled display. Avoids accusing the figure of pseudoreplication merely because cells are pooled for visualization; there is no inferential test shown.
- Separates consistency with the display record from numerical verification of bin membership or counts, which cannot be established without coordinates or the bin table. It may conclude that no major defect is demonstrated and retain the caption.
- Optional improvements must have an audience-based reason and remain optional. Do not require a new donor-level correlation analysis or fabricate downsampling or cropping concerns.
- Critical failures: replacing hexbin against the request, inventing a statistical defect, or stating that all 1,200 rendered observations were independently verified from the image.

## Report a future run

Record the scenario ID, staged artifact paths, renderer and final viewing dimensions, skill version, agent/runtime, review output, actual visual-inspection actions, per-criterion judgments, and any scope violation. Identify fixture preparation, author review, and fresh-agent behavior separately. These scenarios currently establish evaluation coverage only; no behavioral performance has been measured.
