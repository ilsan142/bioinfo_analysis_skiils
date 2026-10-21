# Lab meeting task input scenarios

These are synthetic scenario specifications for future evaluation, not executed tests or research findings. Give an evaluated agent only the relevant task and staged input packet, plus the skill. Keep `rubric.md` separate. No notebook, image, or result file named below is bundled here; before a file-based run, construct the described fixtures with matching content and record their synthetic origin. A text-only exercise cannot establish actual figure-viewing behavior.

## Scenario 1: Paired single-cell update with an uncertain candidate

### User task

“이 실행된 분석 자료로 랩미팅 발표 흐름과 발표자 노트를 만들어줘. 면역학 연구자와 분석 담당자가 함께 듣고, 발표 12분과 토론 5분이야. 후보 유전자를 다음 실험으로 넘길지 의견을 받고 싶어. 한국어로 작성하고 PPT 파일은 필요 없어.”

### Input packet

- `paired_update.ipynb`, saved executed record: cell `design` describes six human donors, each contributing one control and one treated sample; cell `qc` reports 12 libraries and 18,340 retained cells. Cell `history` records that target A was chosen after inspecting differential expression and that no independent cohort has been tested.
- `results/target_summary.tsv`, row `target_A`: donor-paired treated-minus-control contrast, mean +0.20 log2 units, 95% donor-bootstrap interval [−0.05, +0.44]. The saved method note says donors, not cells, were resampled. No primary endpoint was prespecified.
- `figures/paired_target.png`: a rendered figure of six donor differences, one negative and five positive, with the same summary estimate and interval. One donor label overlaps the zero line; the legend uses an abbreviation not defined elsewhere. Provide the image itself during a visual evaluation.
- `figures/cell_umap.png`: a cell-level embedding with condition colors. It does not display donor-level replication.
- `analysis-plan.md`, section `Next evidence`: independent donors would address across-donor replication; an orthogonal assay on stored specimens would address assay agreement but would not be a new donor cohort. Costs, future sample availability, and a prioritization threshold are unresolved.
- `old_outline.txt`: a previous draft calls the target “robustly activated in n = 18,340 samples” and uses the heading “Validation.” It predates the saved interval estimate. Preserve this source as history.

## Scenario 2: A promising first plot followed by a confounding audit

### User task

“이번 주 결과가 약해 보여서 발표를 어떻게 잡을지 고민이야. 기존 분석과 기록을 보고 8분 업데이트와 7분 의사결정 토론용으로 구성해줘. PI는 처리 효과를 기대했어. 중요한 실패도 포함하고, 다음에 무엇을 해야 할지 선명하게 정리해줘. 재분석은 하지 말아줘.”

### Input packet

- `sample_manifest.tsv` contains six distinct donors: C1, C2, C3 are controls processed in batch A; T1, T2, T3 are treated samples processed in batch B. Donors are unpaired. No other samples exist.
- `initial_analysis.ipynb`, cells `naive-de` and `pca`: the original condition-only analysis reports 127 genes with adjusted p < 0.05 and shows PCA separation. These are saved outputs from the first exploratory analysis.
- `figures/pca.png`: six visible sample points, with condition represented by color and batch by shape. Color and shape groups coincide. Provide the image in a visual evaluation.
- `design_audit.md`: the later audit documents complete condition/batch confounding and inability to estimate a separate treatment effect from this design. It does not report a corrected effect estimate.
- `decision_history.md`: the team paused pathway interpretation after the design audit. An earlier suggestion to remove T3 was rejected because there was no independent QC failure; T3 remains in the source records.
- `followup_options.md`: retrieve processing records to check whether labels are wrong; if labels are correct, plan both conditions within each future batch with biological replication. No new samples have been acquired, no correction has been run, and no numerical power calculation exists.

## Scenario 3: Design discussion before any assay results exist

### User task

“Prepare an English lab meeting storyboard with speaker notes for a mixed molecular biology and computational audience. I have 15 minutes including questions. We need feedback on whether a pulse-chase design can answer our RNA stability question. Use the plan and existing metadata audit; the experiment has not started. Please proceed with a useful draft without waiting for a slide-format decision.”

### Input packet

- `analysis-plan.md`, question Q2: compare transcript degradation between conditions in a pulse-chase experiment. Proposed time points are 0, 2, and 6 hours, with three independent cultures per condition and time point; these are planning values. Culture allocation and availability are not yet verified. Calibration and model assumptions remain unresolved.
- `metadata_audit.tsv`: records from a prior public dataset document condition, time, and library identifier for 12 libraries. Donor/culture relationships and spike-in usage are undocumented. This is a completed metadata inventory, not a kinetic analysis or a new experiment.
- `design_options.md`: option A measures labeled fractions alone; option B adds a calibrated abundance measurement. The document says the meaning and identifiability of a degradation estimate depend on the measurement model and assumptions and must be checked before fitting. No feasibility result resolves this choice.
- `figures/proposed_decay_curves.png`: an author-drawn illustration with smooth declining curves, no measured points, and a caption stating “Hypothetical trajectories, arbitrary units.” Its generic title is “Treatment improves stability.” Provide the actual schematic during a visual evaluation.
- `notes.md`: the PI wants to choose which measurement needs to be secured before purchasing reagents. The team has not decided what precision is required. No cited paper has been supplied, and there are no executed assay or model outputs.

## Scenario 4: Natural headlines and layouts without losing scientific meaning

### User task

“아래 슬라이드 내용을 연구 발표용으로 다듬어줘. 제목은 3초 안에 핵심을 이해할 수 있게 자연스럽게 쓰고, 반복되는 좌우 2분할과 긴 각주를 정리해줘. 슬라이드마다 기존 제목 -> 수정 헤드라인, 레이아웃 제안, 본문과 불릿, 차트 개선 지시사항을 써줘. 수정안만 필요하고 PPT 파일이나 새 분석은 필요 없어.”

### Input packet

The following is a synthetic text transcript, including author descriptions of the current layouts. No rendered slides, plots, or raw data are supplied. Do not stage imaginary image files for a text-only run.

- Slide 1 title: “Contribution of treatment to target activation.” Left half contains a paragraph explaining every processing step; the right half is described as an estimate with an interval. Source record: six paired donors, treated-minus-control difference +0.20 log2 units, 95% donor-bootstrap interval [-0.05, +0.44]. The candidate was selected after inspecting the data. The small footer currently holds the independent n, interval definition, and exploratory status. Body prose repeats the numerical result twice.
- Slide 2 title: “Is the contribution of treatment separable?” Left and right cards say “Control: batch A” and “Treated: batch B”; three distinct unpaired donors are in each condition. The processing record confirms complete condition/batch confounding. The main text claims treatment causes the separation, while the small footer says no separate treatment effect can be estimated. A full software-version list occupies the bottom margin.
- Slide 3 title: “Contribution of the odds-type model.” Two equal cards contain lengthy model prose and a summary statistic. The supplied model record defines an odds ratio of 1.4, treated relative to control, with a 95% confidence interval [0.7, 2.8]; it does not provide predicted probabilities. A separate chart label reads “Odd -> even”; its meaning is undocumented. No sample-size information or image is available for this slide. Do not assume that the label describes a train/test split.
