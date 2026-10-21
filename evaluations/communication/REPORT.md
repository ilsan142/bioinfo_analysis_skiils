# Communication skills validation

Date: 2026-10-21. This report concerns the communication update and three new skills. All task data are synthetic. Communication guidance was checked against MIT BE and Broad pages cited in the installed references. This is not a biological validation or a controlled comparison against an unskilled model.

## Test design

Three authoring agents implemented the new skills in separate directories. Fresh evaluation agents then received only one copied skill, its realistic task, and minimal synthetic input artifacts. They did not receive the rubric, fixture-builder code, other cases, prior results, or the authoring conversation. The coordinator separately read each deliverable and compared it with the task and input evidence. No pass is inferred solely from package validation.

The [task inputs](cases.json) and [coordinator scoring criteria](rubric.md) are separate. Cases 01–03 exercise the new skills; case 04 checks the research assistant's review-only boundary after an integration correction. `prepare_case.py --suite communication` stages one case without copying the rubric or other cases. [build_inputs.py](build_inputs.py) regenerates the tiny synthetic fixture using NumPy, SciPy and Matplotlib; its deliberately misleading image is an evaluation input, not a plotting recommendation. Staging an existing case requires only the Python standard library.

## Completed blind communication tasks

| Case | Actual work and observed behavior | Result and limits |
| --- | --- | --- |
| 01: meeting | Wrote a Korean five-minute storyboard with notes, a four-minute talk and one-minute discussion; linked all four donor rows and retained mixed response directions; identified complete condition/library confounding and distinguished four paired donors from cells; proposed crossed conditions for follow-up and labeled proposals | Required behaviors observed. [meeting.md](runs/01/meeting.md). No new analysis, deck, rehearsal, or figure viewing was claimed; none was needed for the text/table input. Timing is an estimate, not a measured talk. |
| 02: figure | Reviewed the actual PNG, caption and donor table; identified biological n mismatch, illustrative error bars, overclaim, hidden pairing, undefined scale and misleading truncated bars; distinguished confirmed reporting errors from unavailable statistical checks; retained readable labels and did not invent a defect from the red/green palette alone | Required behaviors observed. [review.md](runs/02/review.md). Agent reported opening the PNG; coordinator independently opened it and verified visible issues. No redesign, cell-level reanalysis, print-size test or accessibility certification occurred. |
| 03: manuscript | Drafted only the requested Korean Results paragraph and Methods; used corrected paired n=4, difference 0.25, 95% interval [-1.273480, 1.773480] and p=0.637618; withheld the requested strong activation story and superseded p=0.003; marked missing genes, preprocessing and versions | Required behaviors observed. [draft.md](runs/03/draft.md). No new analysis or invented citation was introduced. Input records support the draft; the agent did not independently reproduce the upstream experiment or score. |

The coordinator checked source files, task text, image assets, and copied skill files against the original staged inputs after completion; all were unchanged. Completed case directories and their skill versions are preserved under `runs/01`–`runs/03`. [run_integrity.json](run_integrity.json) records these comparisons and file hashes. This is preservation evidence, not a claim that the agents' prose was independently reproduced verbatim. Raw agent tool transcripts are not bundled; tool-order claims are therefore limited to the observed artifacts and agent execution reports.

## Existing-skill regressions

| Test | Actual work and findings | Outcome |
| --- | --- | --- |
| Research assistant, analysis case 01 | Inspected all 8 independent donors and 3 markers; retained all samples; connected checks, distributions, exploratory batch-adjusted contrasts and bounded sensitivity checks. Consolidated the stepwise script exploration into a 24-cell notebook with 10 executed code cells and 0 errors. Purpose statements accompany displayed values, units and independent n are explained, and a three-panel donor plot was inspected. | Required scientific and final-output behaviors observed. [Notebook](runs/analysis-01/marker_exploration.ipynb). The agent reports inspecting each script stage before writing dependent analysis; the final notebook alone does not prove that historical order or that the notebook was used throughout exploration. |
| Planner, planner case 02, first run | Checked the full inputs and identified 6 independent donors, 3 per condition, with complete condition/batch confounding. Produced a bounded conditional plan without fitting a model or calculating the proposed group contrasts. | Scientific scope and plan passed review, **output explanation partially failed**: preserved probe code ends with a bare JSON diagnostic dictionary, without the required purpose print. [Original plan](runs/planner-02-v1/analysis_plan.md). This run is not relabeled as a full pass. |
| Planner, planner case 02, revised run | A fresh agent used the revised skill with the same raw input. The saved executable probe prints the reason and units before each coherent group and a compact donor-by-condition-by-batch table. The plan preserves the confounding limit and contrasting/inconclusive-result branches without performing the proposed analysis. | Required behaviors observed after refinement. [Revised plan](runs/planner-02-v2/analysis_plan.md). The coordinator reran the saved probe successfully; [execution record](planner_replay_checks.json). The probe uses the original absolute task path; change its `root` to the local case directory when replaying elsewhere. |
| Research assistant, communication case 04 | Read corrected paired relationships and the flawed code; identified two independent donor pairs, arbitrary rounding, an independent-groups test and invalid n. Specified affected outputs without rerunning the analysis or editing inputs. | Required review-only behavior observed. [Review](runs/04/review.md). No `execution_marker.txt` or `result.txt` was created. Absent numerical results and figures were not claimed as inspected. |

The coordinator independently reran the normal notebook in a separate copied directory using its saved runner. All 10 code cells executed in a fresh kernel with 0 errors. Three result TSVs and the PNG were byte-identical to the preserved agent outputs; original input contents were unchanged. The coordinator also opened the replayed PNG and checked axes, legend, donor symbols and visible sample coverage. See [replay_checks.json](replay_checks.json). This confirms execution and output consistency, not the correctness of biological claims or general validity of the statistical assumptions.

## Findings and refinements

- A separate read-only integration review identified an unconditional execution/recomputation requirement in the research assistant that conflicted with review-only scope. The current skill qualifies those requirements to authorized analysis; case 04 then tested the revised boundary.
- The first planner run explained design decisions well but printed an unexplained dictionary in the saved probe. The planner now requires purpose statements in the executable probe itself and includes an on-demand compact display example. The fresh blind rerun above used the same input and the revised skill and retained purpose-labeled output in its actual saved code.
- The lab-meeting skill now explicitly preserves the user's preference not to introduce hexbin in requested redraws, without calling an existing hexbin scientifically invalid. That later redraw instruction has structural review only; the meeting task did not request any redraw.

Preserved skill copies show the exact instructions for each run. They are historical evaluation evidence, not alternate installation targets. Later refinements are not retroactively attributed to earlier runs.

## Structural verification

All five current installable skills passed the skill-creator `quick_validate.py` frontmatter/naming/scaffold check. The repository validator passed English-only installed instructions, local links, Markdown fences and whitespace, named skills, and analysis/planner/communication input schemas (10, 3 and 4 tasks respectively). These structural checks do not execute or score those tasks.

## Additional scenarios and untested scope

The initial communication release supplied three task specifications per new skill with separate rubrics:

- [Lab meeting scenarios](lab-meeting/scenarios.md) and [rubric](lab-meeting/rubric.md).
- [Figure review scenarios](figure-review/scenarios.md) and [rubric](figure-review/rubric.md).
- [Manuscript scenarios](manuscript/scenarios.md) and [rubric](manuscript/rubric.md).

Those nine specifications were reviewed for coverage but were not individually executed. The three completed tests above use the distinct inputs in `cases.json`; they are not passes for all task-specific scenarios. Real notebook-to-deck conversion, live presentation timing, PDF/vector rendering, screenshot-only review, requested figure edits, existing-hexbin retention, literature verification failures, and unresolved artifact conflicts without an explicit supersession record remain untested in fresh agents. No end-to-end Codex/Claude Code discovery test or cross-model reliability study was performed. Existing historical evaluation results do not establish that every old case still passes after this update.

## Later slide-revision refinement

The lab-meeting skill now routes targeted slide edits to [slide revision guidance](../../skills/bioinformatics-lab-meeting-assistant/references/slide-revision.md). It adds natural takeaway headlines, comparison-driven layouts, meaning-preserving label edits, selective removal of footer prose, and a four-field per-slide response. A three-second reading goal is explicitly a design heuristic; important uncertainty, independent sample counts, confounding, and required attribution remain visible. Targeted edits do not require a full talk, new analysis, or deck creation.

A fourth [lab-meeting scenario](lab-meeting/scenarios.md) and separate [scoring criteria](lab-meeting/rubric.md) cover uncertain effects, complete confounding, ambiguous labels, and odds/probability confusion. This is an additional text-only test specification, not an executed or passed behavioral test. The earlier nine specifications and preserved agent runs remain unchanged. Author review checked the new instructions against these failure cases; no new independent agent run, PPTX generation, rendered-slide inspection, audience test, or three-second comprehension measurement was performed for this refinement.

For this refinement, the lab-meeting skill passed `quick_validate.py`; `validate_package.py` passed for five skills, 70 documents, 199 local links, and the unchanged 10/3/4 executable-case input schemas. The fourth lab-meeting scenario is a Markdown specification and is not part of those executable-case counts. Whitespace checks passed. These results establish package consistency only.
