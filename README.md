# Bioinformatics Analysis Skills

[English](README.md) | [한국어](README.ko.md)

Reusable Agent Skills for **doing bioinformatics with a researcher who can understand and review the analysis**, usable in Codex and Claude Code.

| Skill | When to use it | Main deliverable |
| --- | --- | --- |
| [`bioinformatics-analysis-planner`](skills/bioinformatics-analysis-planner/SKILL.md) | Design questions, comparisons, methods and priorities from available data, or substantially revise a design | A plan with verified evidence, conditional choices and a first executable step |
| [`bioinformatics-research-assistant`](skills/bioinformatics-research-assistant/SKILL.md) | Explore, execute, review and interpret an analysis | Rerunnable work connecting questions, actual outputs, interpretations and next decisions |

Each skill works independently. Use the planner when a separate design is useful, then let the research assistant implement and revise it. Both skills are not mandatory for every analysis.

## Why this exists

Many of the bioinformatics skills I encountered focused on a particular omics workflow or analysis tool. I felt a need for a skill that supports the research process itself: exploring the data, understanding what the measurements mean, and deciding what analysis should come next.

Coding assistants such as Codex and Claude Code can produce working code quickly. In research, however, working code is only part of the requirement. The researcher also needs to understand what was done, why it was appropriate, what was actually observed, and what the evidence cannot establish. Code can execute successfully while hiding an incorrect experimental unit, an unsupported assumption, or a biological interpretation the data do not justify.

This skill is designed to make the agent a research assistant whose work the researcher can follow and evaluate. It emphasizes readable code and explanations, with analysis organized around one meaningful scientific question at a time. The assistant explores the data, inspects real outputs, and then chooses the next analysis or visualization using biological and statistical reasoning. The initial plan remains provisional until the data support its choices.

The aim is to keep the researcher involved in scientific judgment while letting the assistant carry out routine, agreed work without repeated approval requests.

Exploratory notebooks fit this aim: code, output, and the researcher's interpretation can sit together, letting another reader follow why the analysis took its next step. The skill therefore prefers an executed `.ipynb` for exploration. The notebook grows as results are inspected, so it records how observations informed decisions, including choices added after seeing the data.

## How the skill works

For each meaningful question, the assistant:

1. Explains the question and why it matters.
2. Separates verified inputs, provisional assumptions, and unknowns.
3. Implements and runs the minimum analysis needed.
4. Inspects actual numbers, warnings, and any generated figures.
5. Explains observations, interpretation, and limitations.
6. Uses those results to choose the next step or revise the plan.

The skill covers principles shared by RNA-seq, single-cell, spatial, genomic variants, microbiome analysis, and biological prediction. It does not prescribe one universal pipeline. It checks measurement meaning, independent replicates, dependence, confounding, exclusions, uncertainty, data leakage, and interpretation only where relevant. It should not activate for unrelated web or app development.

The distributed instructions are in English. The assistant follows the user's language, with Korean as the fallback when no preference is apparent. It does not start an unsolicited research analysis when the request is only for planning, review, or skill creation.

## Design an analysis from the data

`bioinformatics-analysis-planner` starts with lightweight checks of measurement meaning, experimental units and feasible comparisons. It connects the research question and effect of interest to recommended methods, their prerequisites, and the evidence that would change a choice or stop an unsupported inference. Its output is a plan section in an existing record or a concise `analysis_plan.md`.

For a planning-only request, it stops before differential expression, full clustering or predictor training. If design and execution are already requested together, it continues without asking for routine approval again. The plan stays provisional; changes made after inspecting results are recorded with their reasons.

This separation makes the researcher's intent and analytical decisions explicit, regardless of model capability. Adding a skill does not demonstrate better scientific accuracy or model performance. A straightforward analysis can still be planned and executed using the research assistant alone.

## Analysis in a notebook

Each scientific question forms a connected sequence: **question and rationale → code and actual output → observations, interpretation, and limitations → next decision**. The assistant writes the interpretation after inspecting the output and before implementing analysis that depends on it. Important decisions stay in the notebook so the researcher does not need the chat history to understand the work.

Before calling the notebook reproducible, the assistant reruns it in order from a fresh kernel, checks the new outputs, and saves them with the current code. Corrections to sample relationships require recalculation and updates to affected outputs and explanations. Missing inputs, failed execution, and unverified steps remain explicit.

This is a default for exploration, with room for the researcher's workflow. Existing literate documents, explicitly requested scripts, established pipelines, code reviews, or unavailable notebook runtimes can call for another format. Long or reusable calculations can live in scripts while their important parameters, results, and rationale remain visible in the notebook. A sufficient notebook is also the analysis record; duplicate narrative logs and separate exports of every intermediate result are unnecessary.

## Files

| File | Purpose |
| --- | --- |
| [Planner SKILL.md](skills/bioinformatics-analysis-planner/SKILL.md) | Question, data, design feasibility, conditional choices, execution scope and handoff |
| [Plan writing guide](skills/bioinformatics-analysis-planner/references/analysis-plan.md) | Compact plan outline and conditional examples |
| [Research assistant SKILL.md](skills/bioinformatics-research-assistant/SKILL.md) | Core workflow, scientific decisions, researcher questions, reporting, and completion criteria |
| [scientific-review.md](skills/bioinformatics-research-assistant/references/scientific-review.md) | Conditional scientific and statistical checks, data-type considerations, and checked sources |
| [collaboration-examples.md](skills/bioinformatics-research-assistant/references/collaboration-examples.md) | Examples of explanations, necessary questions, corrections, and limits |
| [analysis-record.md](skills/bioinformatics-research-assistant/references/analysis-record.md) | Notebook workflow, saved outputs and clean reruns, lightweight records, and final reports |
| [Evaluation inputs](evaluations/cases.json) and [rubric](evaluations/rubric.md) | Ten small scenarios; inputs and scoring criteria are kept separate |
| [Evaluation report](evaluations/REPORT.md) | Executed checks, evidence, revisions, and untested areas |
| [Notebook validation](evaluations/NOTEBOOK_WORKFLOW.md) | Fresh-agent notebook checks, executed examples, and clean-kernel replay evidence |

Install the selected skill directories under `skills/`. Planner validation is documented [separately](evaluations/planner/REPORT.md). References are read when needed. Evaluation inputs, scoring criteria, and historical records are outside the distributable skill. The skill has no mandatory analysis scripts, package installation, or product-specific hooks.

## Installation

Clone this repository:

```bash
git clone https://github.com/ilsan142/bioinfo_analysis_skiils.git
cd bioinfo_analysis_skiils
```

Copy the **entire selected skill directory** to one of the following locations. Replace `<skill-name>` with an actual skill name from the table above. Choose either project or user scope for each product to avoid maintaining divergent copies.

| Product | Project scope | User scope | Explicit invocation |
| --- | --- | --- | --- |
| Codex CLI / IDE | `<project>/.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` | `$<skill-name>` or select it with `/skills` |
| Claude Code | `<project>/.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` | `/<skill-name>` |

For user-wide installation, run the relevant block from the cloned repository. Set `skill_name` to the skill you want; repeat with the other name if you want both. The copy is skipped if that destination already exists; compare existing files before updating them.

Codex:

```bash
skill_name=bioinformatics-analysis-planner
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/$skill_name" && \
  test ! -L "$HOME/.agents/skills/$skill_name" && \
  cp -R "skills/$skill_name" "$HOME/.agents/skills/"
```

Claude Code:

```bash
skill_name=bioinformatics-analysis-planner
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/$skill_name" && \
  test ! -L "$HOME/.claude/skills/$skill_name" && \
  cp -R "skills/$skill_name" "$HOME/.claude/skills/"
```

For project scope, copy to the corresponding directory inside your research project instead. Do not copy `evaluations/` into the skill installation. If the skill does not appear, check discovery settings or start a new session.

These locations and invocation forms were checked against the [official Codex documentation](https://learn.chatgpt.com/docs/build-skills) and [official Claude Code documentation](https://code.claude.com/docs/en/skills) on 2026-10-19. The shared files use the [Agent Skills format](https://agentskills.io/specification). Actual discovery and invocation in both products have not been tested end to end.

## Usage

When you need a separate design, invoke the planner. Execution can be requested later or authorized together with planning.

In Codex:

```text
$bioinformatics-analysis-planner
Inspect the data and experimental records in this directory and write an analysis plan for the treatment comparison. Run only lightweight checks needed for the design, and record unresolved decisions and the first executable step.
```

In Claude Code:

```text
/bioinformatics-analysis-planner Inspect this dataset and its experimental records and prepare an analysis plan.
```

To execute the plan:

```text
$bioinformatics-research-assistant
Read analysis_plan.md and start with the first unfinished step. Inspect each result before choosing the next analysis, and record necessary revisions to the plan.
```

For direct analysis without a separate plan document:

In Codex:

```text
$bioinformatics-research-assistant
Inspect the expression matrix and experimental records in this directory, and help me analyze the treatment effect.
```

In Claude Code:

```text
/bioinformatics-research-assistant Inspect the expression matrix and experimental records in this directory, and help me analyze the treatment effect.
```

Supply the biological question and available data or records. The assistant should inspect existing information before asking for anything missing. It should continue independent checks when an unresolved question blocks only part of the analysis.

## Validation and limits

The planner has package checks, executed input probes on three synthetic cases, and author-written plan walkthroughs. It has not received independent agent behavioral validation. See the [planner validation record](evaluations/planner/REPORT.md). The historical evaluations below concern the research assistant.

The earlier notebook update was tested with two fresh agents given only the skill and synthetic tasks, without expected answers or a request to use notebooks. Both produced executed notebooks and recorded observations before implementing dependent analysis. The normal case also generated and visually inspected a plot; the confounded case correctly withheld an identifiable treatment-effect claim. Independent clean-kernel reruns reproduced their stored outputs and exported tables. See the [validation record](evaluations/NOTEBOOK_WORKFLOW.md), [normal-case notebook](evaluations/runs/nb-01/analysis.ipynb), and [confounding notebook](evaluations/runs/nb-03/treated_control_batch_analysis.ipynb).

The original Korean edition was exercised in six scenarios: well-described data, fractional expression values, complete condition/batch confounding, prediction leakage, corrected sample relationships, and an unrelated web request. The normal case was rerun after a refinement to consolidate small outputs. Seven clean-process reruns checked the resulting analysis code. Four other scenarios were reviewed but not executed.

The English edition separately passed package checks and fresh-agent regression checks for well-described data and complete condition/batch confounding. Both generated analyses were rerun in fresh processes with identical result tables. The other eight cases have not been rerun after translation; see the [English-edition validation record](evaluations/ENGLISH_EDITION.md). Historical inputs, skill snapshots, and execution records retain their original language and wording so that the evidence is not rewritten retrospectively. They are not alternative installable skills.

Published evaluation evidence in this repository uses synthetic cases. Full client integration and broad reliability across models remain unvalidated. Notebook-format exceptions and corrections to an existing notebook have not received fresh behavioral tests. One synthetic figure was reviewed; that is not broad visualization validation. Synthetic execution is not biological validation.

To check the current package from the repository root, use Python 3 with PyYAML installed:

```bash
python3 evaluations/validate_package.py
python3 evaluations/prepare_case.py 01 /tmp/bio-skill-case-01-new
python3 evaluations/prepare_case.py 01 /tmp/bio-planner-case-01-new --suite planner
```

Each `prepare_case.py` command prepares a fresh, isolated case directory using only the Python standard library. It does not run an agent evaluation. Give a fresh agent only that directory's skill and task inputs, and score its actual behavior separately. Deliver case 07's correction only after its initial result; for case 10, expose only skill metadata without forcing invocation.
