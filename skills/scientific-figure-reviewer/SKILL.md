---
name: scientific-figure-reviewer
description: Review scientific figures and captions against their intended message, supplied evidence, experimental design, and publication or presentation setting. Use for requested scientific figure critique, including evidence tables and prioritized fixes. Do not apply to every routine plot, general website design, or unsolicited statistical reanalysis.
---

# Scientific figure review

Produce a concrete, evidence-bounded review that helps a researcher decide what to revise. Work independently of any particular application, plotting library, or companion skill. Follow the user's language and requested output format; default to Korean when no language preference is apparent.

## Establish the review boundary

Use the request and supplied materials to identify the audience, intended medium and size, figure version, caption, and central claim. If the message is implicit, describe your interpretation as provisional. Do not require a complete analysis package before reviewing what is available.

Review-only work does not authorize changing figures, captions, data, filtering, models, or analysis code. Provide proposed wording or layout changes as proposals. If revision is requested, preserve originals and distinguish presentation changes from changes to scientific analysis. Do not force statistical reruns or new analyses to complete a communication review.

Read [review-examples.md](references/review-examples.md) when calibrating severity, handling incomplete evidence, or proposing a redesign; it also records the design sources and their limits.

## Inspect the actual figure

Open every supplied figure or relevant page with an available image or document viewer. Inspect the full composition and, when needed, enlarged panels; assess readability at the intended display size when known. For vector or document inputs, inspect a rendered view as well as any source text needed for verification.

Code inspection, file existence, successful export, OCR, and data-table checks do not establish visual quality. Record which images/pages were actually viewed and which checks used tables, code, or captions. If viewing is unavailable, explicitly mark visual inspection incomplete and continue the supported text/table review; do not invent visual observations.

Use a compact evidence/source table: artifact and version or path; panels/claims it covers; how it was inspected; what it can and cannot verify. Link supplied sources where possible. Missing raw data limits numerical verification, not all communication feedback.

## Review message and scientific meaning

- Compare the title, caption, panel order, annotations, and visual emphasis with the evidence shown. Separate descriptive association from causal or mechanistic claims. Do not make a conclusion more assertive merely to create a memorable title.
- Check axis meaning, units, direction, ranges, breaks, baseline choices, transformations, normalization, and denominators against available records. A nonzero baseline or log scale is not automatically wrong; explain a specific interpretive consequence when flagging one.
- Identify the observation represented by a point, line, image, or bar. Distinguish independent biological units from cells, reads, fields, technical repeats, and repeated measurements. State what supports the reported sample count; do not infer independence from plotted marks alone.
- Assess whether pairing, time, nesting, group sizes, and relevant variability are understandable. Check the stated meaning of intervals and error bars, comparisons, statistical symbols, and multiplicity descriptions where present. Do not assume the analysis ignored pairing just because paired lines are absent.
- Compare labels, counts, plotted summaries, and caption claims with supplied tables or code when relevant. Say whether a discrepancy is confirmed or only unresolved. A plausible figure does not verify estimates, uncertainty, significance, or underlying data validity.
- Check whether exclusions, display subsets, aggregation, and downsampling are disclosed. Distinguish the data displayed from the data analyzed. Preserve controls, contrary findings, and limitations needed to evaluate the claim; visual simplification must not conceal them.
- For representative images, inspect scale bars, labels, crop boundaries, insets, and comparable display settings where available. An unexplained crop is a documentation question, not proof of manipulation. Without originals, do not claim image-integrity verification.

## Review communication and accessibility

- Check panel labels and reading order; legend-to-mark mapping; clipped annotations; overlapping labels; text size; contrast; and consistency of symbols, axes, and colors across panels.
- Check whether distinctions survive without color alone, using labels, shapes, line styles, or other redundant cues where useful. Do not certify accessibility from a palette name without inspecting its use.
- Match detail to the medium: a paper needs enough figure/caption context to stand alone; a slide needs legible evidence at presentation size; a poster needs a clear reading path. Preserve the scientific information essential to interpreting the comparison.
- Judge plot choice by what the reader needs to compare and what the observations represent. A hexbin plot is not a scientific defect. When redesign is requested, prefer familiar biological figures such as sample points, paired lines, distributions, time courses, or annotated heatmaps when suitable; do not introduce hexbin unless the user requests it.
- Treat stylistic alternatives as optional unless they cause a concrete comprehension problem. Do not replace a useful figure simply to make it look novel or satisfy a fixed gallery of chart types.

## Deliver an actionable review

Lead with the most consequential supported conclusion about the figure, then provide the source table and prioritized observations. For each observation include:

1. **Location:** figure, panel, axis, caption sentence, or exact region.
2. **Observation and evidence:** what is visible or documented; cite the relevant artifact, table field, or code location. Mark an unresolved concern as unverified.
3. **Impact:** the misunderstanding or scientific interpretation that could result.
4. **Proposed fix:** a specific label, caption, layout, or display change, or the smallest missing information needed. Identify any proposal that would require separate analysis work.
5. **Severity:** critical for a demonstrated issue that materially invalidates the displayed claim; major for a substantive interpretation or evidence gap; minor for a localized readability problem; suggestion for an optional improvement. Severity describes consequence, not certainty.

Use human-readable explanations rather than bare scores or a checklist of generic warnings. Report no defect when the supplied material does not support one; an adequate panel may be explicitly retained. Missing inputs are limitations or focused questions, not invented errors.

Close with a short revision order and the remaining verification limits. State whether visual inspection occurred, whether source values were checked, and whether any changes were actually made. A completed review is not a rerun of the analysis or biological validation.
