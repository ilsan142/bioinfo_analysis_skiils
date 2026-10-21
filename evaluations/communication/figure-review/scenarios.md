# Scientific figure reviewer scenarios

Status: **unexecuted behavioral evaluation inputs**. The fixtures below are synthetic task specifications, not research results or completed tests. Stage each case in a fresh directory, render the specified figure, and provide the rendered figure with the exact caption and listed source records. Do not give the evaluated agent the private [rubric](rubric.md) or the figure-construction notes. Preparing or rendering a fixture does not count as a behavioral evaluation.

The evaluator must record the actual artifact paths and rendering method before a run. A fixture described below but not rendered is not a visual review test. Keep all figure content except an explicitly specified defect readable at the stated target size.

## Case 01: paired donor experiment for a paper

### Task given to the agent

> Please review Figure 2 and its caption for our specialist biology paper at a final width of 170 mm. Give a prioritized, practical review with the evidence behind each finding. The sample summary and plotting table are supplied. Please do not change files or rerun the statistics.

### Figure-construction notes for the evaluator

Render one panel labeled **A**, titled **“Treatment restores healthy expression”**, with Control and Treated on the horizontal axis and **“Expression”** on the vertical axis. Plot the eight values in the table below as four separate points per group. Use blue circles for Control and orange squares for Treated; both groups are also named under the axis. Add a legend entry **“Each point = one cell”** and a bracket labeled **p = 0.001**. Use a 0–6 vertical range with readable ticks. Include no healthy-reference group and no connecting lines. Avoid introducing unrelated cropping, color, or font defects.

### Caption supplied to the agent

> Figure 2. Treatment restores healthy expression. (A) Expression in control and treated cultures. n = 160 independent experiments per condition. p = 0.001, two-sided t test.

### Supplied `plot_values.tsv`

```tsv
donor_id	condition	value	value_definition	point_unit
D1	Control	2.0	mean of log2(normalized counts + 1)	donor-condition mean
D1	Treated	3.2	mean of log2(normalized counts + 1)	donor-condition mean
D2	Control	2.4	mean of log2(normalized counts + 1)	donor-condition mean
D2	Treated	3.4	mean of log2(normalized counts + 1)	donor-condition mean
D3	Control	1.8	mean of log2(normalized counts + 1)	donor-condition mean
D3	Treated	3.0	mean of log2(normalized counts + 1)	donor-condition mean
D4	Control	2.2	mean of log2(normalized counts + 1)	donor-condition mean
D4	Treated	3.5	mean of log2(normalized counts + 1)	donor-condition mean
```

### Supplied `sample-summary.txt`

> Four independently recruited donors each contributed matched control and treated cultures. Forty measured cells contributed to each donor-condition mean, giving 160 cells per condition. All eight donor-condition means are displayed. No healthy reference measurement is supplied. Test implementation and raw cell measurements are unavailable.

## Case 02: slide screenshot without source data

### Task given to the agent

> Can you review this result slide for a mixed biology audience? I only have this screenshot and the caption, not the source data or plotting code. It will be shown full-screen in a seminar. Please tell me what can be improved now and what cannot be checked; do not redesign it yet.

### Figure-construction notes for the evaluator

Render a 1280 × 720 slide with title **“Treatment-associated changes in reporter signal”**. Show one line panel with horizontal label **Time (h)**, tick values 0, 4, 8, 12, and vertical label **Reporter signal (a.u.)**. Draw red Control and green Treated lines, with identical solid styles and no point shapes; use only a matching color legend for group identification. Draw a translucent band around each line. End Control at 1.3 and Treated at 2.1 after both begin at 1.0; intermediate values are arbitrary drawing coordinates, not supplied data. Put the legend at the right edge and clip the last three letters of **Treated** at that edge. Keep the axes and other text readable. Supply the image only, without its vector source or construction notes.

### Caption supplied to the agent

> Reporter signal over 12 hours in control and treated cultures. Lines show the group mean; shaded bands show uncertainty. The number of independent experiments is not available in the presentation draft.

No numerical table, replicate metadata, code, raw image, or methods are supplied. The rendered slide and caption are the complete task inputs.

## Case 03: documented hexbin display with a narrow caption request

### Task given to the agent

> Please check Figure S3 and its caption for clarity and consistency with the supplied record. Our specialist audience is familiar with density plots and we want to keep the existing hexbin. Recommend a revised caption only if necessary. Do not change the chart or run new analyses.

### Figure-construction notes for the evaluator

Render one clearly labeled hexbin panel titled **“Two reporter measurements across recorded cells”**. Label the horizontal axis **Reporter A (a.u.)**, the vertical axis **Reporter B (a.u.)**, and the colorbar **Cells per bin**. Show a sequential, readable color scale with counts spanning 1–20. Display an irregular positively associated cloud of bins; the task supplies no exact coordinates. Keep labels legible at a final width of 170 mm, with no clipping, significance annotation, or donor-specific color encoding. Do not encode an intentional visual defect.

### Caption supplied to the agent

> Figure S3. Joint distribution of reporter A and reporter B in recorded cells. Color indicates the number of cells per hexagonal bin. The figure displays all 1,200 recorded cells from six independent donors, with 200 cells per donor and no display downsampling. This descriptive display pools cells across donors; it does not estimate a donor-level association or treatment effect. Axes show fluorescence in arbitrary units. No inferential test is shown.

### Supplied `display-record.txt`

> The export record reports 1,200 plotted cell records from donors D1–D6, 200 per donor. No records were excluded from the display. Both fluorescence variables use their recorded linear scale, in arbitrary units. Hexagonal bins encode cell counts. Raw coordinates, the bin-count table, and plotting code are unavailable. This record documents intended export settings; it does not independently verify the rendered bin counts.
