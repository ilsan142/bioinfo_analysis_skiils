# Notebook workflow validation

Date: 2026-10-17. This update makes an executed notebook the preferred record for exploration, while preserving explicit format requests and established workflows. This file contains evaluation criteria and results, not instructions for ordinary analyses.

The tested four-file skill is identified by [skill-en-notebook-v1.sha256.json](runs/skill-en-notebook-v1.sha256.json). Its instructions and both READMEs remain in English and English/Korean respectively; task inputs and the agents' notebook explanations are in Korean, following the user requests.

## Inputs and criteria fixed before execution

Two fresh agents receive only the updated skill and isolated task inputs, without the parent conversation, scoring criteria, or expected answers. Case 01 uses the original synthetic inputs with one added user request: show individual marker_A values in a plot distinguishing condition and batch. Case 03 uses the original complete-confounding task unchanged. Neither task requests a notebook; the default must come from the skill. The tasks and inputs will be retained with their outputs.

Assess actual behavior and artifacts, not particular headings or phrases:

- Choose an executed notebook for these exploratory tasks without unnecessary approval. Keep the notebook understandable without the chat transcript and avoid redundant report files.
- Inspect input-check outputs before implementing dependent comparisons. Record actual observations, interpretation, limits, and the reason for the next choice in notebook Markdown. An assembled notebook alone cannot prove this timing; inspect the public execution trace as well.
- Preserve correct sample joins, measurement scale, independent replication, and scientific interpretation. Case 01 must identify eight donors, four per condition, with balanced batches; treated-minus-control differences should be +1.025, +0.1, and -0.1 log2 intensity. Case 03 must identify rank 2 of a three-column intercept/condition/batch design and must not claim an identifiable adjusted treatment effect.
- Generate and actually open the requested case-01 figure. Check displayed units, group/batch meaning, all eight observations, and any clipping or missing labels. Embedding an image alone is insufficient.
- Save genuine kernel outputs, verify notebook schema separately, and independently rerun from a fresh kernel in a new directory using only declared inputs and code. Inspect resulting values and compare them with the reported observations. Schema success alone is not execution or biological validation.
- Preserve original input bytes and distinguish actual execution from unexecuted work. Report any failure, instruction revision, or missing check instead of calling the case passed.

## Execution results

Both cases passed the applicable behavioral criteria in this single run. Neither agent received expected answers, the rubric, or an instruction to produce a notebook. Both read the notebook reference, executed actual kernel cells incrementally, inspected outputs before adding dependent analysis, and kept the explanation in the notebook without a duplicate narrative report. No repeated approval request or read of scoring criteria was observed. Workspaces were separate temporary directories with shared installed tooling, not a security sandbox.

| Case | Observed result | Evidence |
| --- | --- | --- |
| 01: well-described synthetic data plus a requested plot | Joined all eight samples by ID despite different column order; identified four independent donors per condition and two per condition/batch cell. Four analysis code cells covered integrity/design, distributions/plot, comparison, and sensitivity. Adjusted differences were +1.025, +0.1, and -0.1 log2 intensity; marker_A's leave-one-donor-out range was +0.98 to +1.06. The notebook labels model selection and sensitivity work as exploratory and distinguishes synthetic results from biological validation. | [Task](runs/nb-01/TASK.md), [executed notebook](runs/nb-01/analysis.ipynb), [results](runs/nb-01/marker_results.tsv), [public trace](runs/nb-01/public_trace.jsonl) |
| 03: complete condition/batch confounding | Three analysis code cells covered integrity, identifiability, and descriptive comparison. The notebook displays the 3/0, 0/3 cross-tabulation and rank 2 of 3, followed by the decision not to fit an adjusted treatment effect. Observed differences +2.0 and +0.5 are explicitly joint condition/batch comparisons. Algebraic examples are labeled as illustrations rather than estimated effects. | [Task](runs/nb-03/TASK.md), [executed notebook](runs/nb-03/treated_control_batch_analysis.ipynb), [results](runs/nb-03/descriptive_group_differences.tsv), [public trace](runs/nb-03/public_trace.jsonl) |

The normal agent opened its [marker_A PNG](runs/nb-01/marker_A.png) during exploration and after its final rerun. The parent reviewer also opened the PNG and checked all eight labeled donor points, condition counts, log2 units, batch colors/shapes, mean-line meaning, and legibility. No missing observations or material cropping were found. The figure is also embedded in the notebook. Case 03 used small tables instead of an unnecessary plot.

Final analysis artifacts were one notebook, one result table, and one small rerun script per case, plus PNG/SVG exports of the requested normal-case plot. Temporary cell-building helpers were removed by the agents. Public traces preserve tool calls, outputs, and user-facing messages; private reasoning, system prompts, and internal coordination messages are excluded. Their temporary paths refer to the original execution locations.

## Independent execution and format checks

The parent reviewer ran [replay_notebooks.py](replay_notebooks.py) against the archived notebooks. For each case it validates the schema, copies only task inputs into a new directory, clears all saved code outputs and execution counts, and executes from a fresh kernel. It compares actual stream/display data, including the embedded PNG, with stored evidence. Runtime output counters/metadata are excluded and working-directory paths are normalized. Both notebooks reproduced those outputs, and their exported TSV result tables were byte-identical. Raw inputs remained equal to the original case fixtures. Bounded numerical checks covered expected effects, independent donor counts, marker_A sensitivity bounds, and the confounded result's non-identifiable status. See [replay checks](runs/notebook_replay_checks.json).

Rerun from the repository root, in an environment with the packages recorded by the notebooks:

```bash
python3 evaluations/replay_notebooks.py
```

The notebooks record Python 3.12.7 and relevant packages; the replay used nbformat 5.10.4 and nbclient 0.10.2 with the existing Python kernel. No packages or large datasets were installed. The replay does not launch new agents or revalidate the timing of their scientific choices; that was checked separately in the traces.

The skill-creator validator and repository package validator passed, covering shared metadata, English distribution, local links, Markdown structure, and evaluation input structure. Maintained files passed `git diff --cached --check -- . ':!evaluations/runs/**'`; archived evidence retains its original spacing and bytes. See [format checks](runs/notebook_format_checks.txt). Notebook schema, execution, numerical inspection, and visual review are separate evidence classes. No behavioral failure requiring another instruction revision was observed in these two cases.

## Scope limits

These two small synthetic cases cannot establish reliability on real research data or across models. Existing-workflow exceptions, missing notebook runtimes, and mid-analysis experimental-design corrections are subject to instruction review in this update, not fresh behavioral tests. The other eight scenarios were not rerun with this notebook edition. Earlier evaluation editions remain historical evidence. Product discovery, installation, and full notebook rendering in the Codex/Claude Code interfaces are not tested here. There is no no-skill control or repeated-trial success-rate estimate.
