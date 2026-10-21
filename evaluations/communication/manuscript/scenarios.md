# Manuscript-assistant evaluation scenarios

Status: authored, unexecuted. All studies, identifiers, artifacts, and values below are synthetic evaluation inputs. They are not research findings, completed analyses in this repository, or evidence of skill performance. The snippets simulate records that a future evaluator can materialize in an isolated workspace. Give a worker only the selected scenario, its supplied snippets, and the skill; keep `rubric.md` separate from worker input.

## Scenario 1: A concise Results section with mixed evidence

### User request

“이 분석 결과로 Results 두 문단만 써 주세요. 한국어로 쓰고 Figure 2A와 Table S2를 연결해 주세요. 제목은 'Treatment restores the inflammatory program'으로 생각하고 있습니다. Discussion이나 추가 분석은 필요하지 않습니다.”

### Supplied artifacts

`study_record.md`:

```text
Question: Is treatment associated with changes in inflammatory-gene expression after 24 h?
Material: primary human monocytes, six donors, each split into vehicle and treatment.
Independent units: six donors; 12 libraries are repeated measurements within donor.
Protocol-defined comparison: treatment versus vehicle at 24 h.
Primary transcript analysis: paired model; no external validation cohort.
Pathway analysis was added after investigators viewed the transcript results.
No protein, functional rescue, or mechanism experiment was performed.
```

`run_manifest.txt`:

```text
run_id: mono_20261018_a
execution_status: completed
input: counts_v3.tsv; samples_checked.tsv
code: analysis.R, revision 8a6f0c2
model: ~ donor + condition
contrast: treatment / vehicle
tested_genes: 14820
p_adjust: Benjamini-Hochberg across 14820 tested genes
Table S2: results/mono_20261018_a/transcripts.tsv
Figure 2A: results/mono_20261018_a/fig2a.pdf (not available to this worker)
Figure 2A description: donor-paired normalized counts, same 12 libraries; no visual review supplied.
Exploratory pathway table: results/mono_20261018_a/pathways.tsv
```

`transcripts.tsv`, selected rows from Table S2:

```tsv
gene	log2_fold_change	SE_log2_fold_change	p_value	BH_adjusted_p
IL1B	-0.70	0.29	0.0158	0.11
CXCL8	-0.80	0.25	0.0014	0.04
TNF	-0.12	0.22	0.585	0.72
```

`pathways.tsv`, selected row and metadata:

```text
label: inflammatory_response
normalized_enrichment_score: -1.31
adjusted_p: 0.18
adjustment: BH across 50 tested pathways
selection_timing: post hoc
confidence_intervals: not calculated
```

`draft_note.txt`:

```text
Possible story: treatment restores the inflammatory program and suppresses all three cytokines.
We expect a protein rescue experiment to confirm this next month.
```

## Scenario 2: Methods reconstruction after a pairing correction

### User request

“Methods의 RNA processing와 statistical analysis 부분만 영문으로 정리해 주세요. 최신 파일의 설정을 쓰면 될 것 같습니다. 오늘 donor correction을 반영했는데 아직 재실행하지 않았습니다. 누락된 것은 표시하고 쓸 수 있는 부분은 지금 작성해 주세요.”

### Supplied artifacts

`lab_protocol_signed.md`:

```text
RNA extraction: manufacturer protocol for the supplied silica-column kit; catalog R2040.
Samples were collected 24 h after vehicle or treatment exposure.
RNA integrity was assessed before library preparation; threshold and instrument model were not recorded here.
Library preparation: stranded poly(A)-selected protocol; kit identifier not provided.
```

`planning_notes.md`, modified 2026-10-20:

```text
Proposed pipeline for a future reanalysis: STAR 2.7.11b, reference annotation release 46,
DESeq2 with batch as a covariate, BH < 0.05.
These notes are an outline, not an execution record.
```

`run_manifest.txt`, executed 2026-10-18:

```text
run_id: paired_v2
status: completed
libraries: 10
donors_in_input_metadata: 5 complete pairs
salmon_version: 1.10.3
tximport_version: 1.30.0
R_version: 4.3.2
DESeq2_version: 1.42.0
reference_fasta: transcriptome.fa
reference_annotation_release: not captured
index_builder_parameters: not captured
source: paired_v2/analysis.R
result: paired_v2/de_results.csv
```

`paired_v2/analysis.R`, the executed relevant block:

```r
dds <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ donor + condition)
dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "treated", "vehicle"), alpha = 0.05)
write.csv(as.data.frame(res), "de_results.csv", row.names = TRUE)
```

`donor_correction_20261021.md`:

```text
The library T05 was wrongly assigned to the same donor as V05.
T05 is from a sixth donor. The corrected dataset therefore has four complete pairs
and two unpaired libraries. No corrected statistical model has been selected or executed.
This correction supersedes the donor assignments in paired_v2, not the recorded RNA protocol.
```

`paired_v2/de_results.csv` exists but contains estimates from the obsolete five-pair metadata. No corrected outputs, version lockfile beyond the manifest, reference release record, or additional laboratory notes are supplied.

## Scenario 3: A reviewer revision with conflicting validation artifacts

### User request

“Reviewer가 독립 검증과 mechanism 주장이 과하다고 했습니다. Discussion 마지막 두 문단만 영어로 고쳐 주세요. review용 문장을 유지하되 과장 없이 쓰고, 어떤 근거를 사용했는지도 알려 주세요. 기존 manuscript의 다른 절이나 response letter는 아직 만들지 마세요.”

### Supplied artifacts

`discussion_draft.md`:

```text
Our model identifies a conserved causal mechanism of RNA degradation.
Independent external validation achieved an AUROC of 0.92 and establishes clinical utility.
The same genes will be tested by knockdown in a planned follow-up experiment.
```

`manuscript_context.md`:

```text
Task: classify an observational high-versus-low RNA turnover label using expression features.
Discovery: 120 donors from two cohorts; study-level batch is correlated with label.
Retrospective split: 24 held-out donors from those same cohorts.
The evidence does not include perturbation or prospective clinical outcomes.
Follow-up knockdown is proposed only.
```

`results/run_A/metrics.tsv` and `results/run_B/metrics.tsv`:

```tsv
run_id	discovery_donors	test_donors	AUROC	CI_low	CI_high	CI_method
run_A	120	24	0.92	0.84	0.98	donor_bootstrap
run_B	120	24	0.67	0.51	0.81	donor_bootstrap
```

`results/run_A/manifest.txt`:

```text
status: completed; created: 2026-10-16
split: cohort1_and_cohort2_donor_holdout_v1.tsv
features: selected using all 144 donors before splitting
```

`results/run_B/manifest.txt`:

```text
status: completed; created: 2026-10-19
split: cohort1_and_cohort2_donor_holdout_v1.tsv
features: selected within training data
```

`reviewer_notes.md`, modified 2026-10-20:

```text
Run B was intended to correct the feature-selection leak.
Analyst comment: the run_B checksum does not match the metrics attached to this review draft;
we have not determined whether those metrics were copied from another seed or evaluation set.
No run is marked as the current accepted result. Do not infer supersession from file date.
Separate unresolved item: model and seed manifest for run_B has not been recovered.
```

`references.bib`:

```text
@article{plannedMechanismCitation,
  title = {Reference to be supplied by the authors},
  note = {Unverified placeholder; no authors, journal, DOI, or paper text available}
}
```

No independent cohort, perturbation result, verified mechanism citation, or additional data are supplied. This scenario does not require a new literature search; missing external support may be marked explicitly.
