# Bioinformatics Analysis Skills

[English](README.md) | [한국어](README.ko.md)

Reusable Agent Skills for **doing bioinformatics with a researcher who can understand and review the analysis**, usable in Codex and Claude Code.

The first skill is [`bioinformatics-research-assistant`](skills/bioinformatics-research-assistant/SKILL.md). It defines how an assistant investigates data, makes scientific decisions, explains observations, and leaves reproducible work.

## Why this exists

Many of the bioinformatics skills I encountered focused on a particular omics workflow or analysis tool. I felt a need for a skill that supports the research process itself: exploring the data, understanding what the measurements mean, and deciding what analysis should come next.

Coding assistants such as Codex and Claude Code can produce working code quickly. In research, however, working code is only part of the requirement. The researcher also needs to understand what was done, why it was appropriate, what was actually observed, and what the evidence cannot establish. Code can execute successfully while hiding an incorrect experimental unit, an unsupported assumption, or a biological interpretation the data do not justify.

This skill is designed to make the agent a research assistant whose work the researcher can follow and evaluate. It emphasizes readable code and explanations, with analysis organized around one meaningful scientific question at a time. The assistant explores the data, inspects real outputs, and then chooses the next analysis or visualization using biological and statistical reasoning. The initial plan remains provisional until the data support its choices.

The aim is to keep the researcher involved in scientific judgment while letting the assistant carry out routine, agreed work without repeated approval requests.

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

## Files

| File | Purpose |
| --- | --- |
| [SKILL.md](skills/bioinformatics-research-assistant/SKILL.md) | Core workflow, scientific decisions, researcher questions, reporting, and completion criteria |
| [scientific-review.md](skills/bioinformatics-research-assistant/references/scientific-review.md) | Conditional scientific and statistical checks, data-type considerations, and checked sources |
| [collaboration-examples.md](skills/bioinformatics-research-assistant/references/collaboration-examples.md) | Examples of explanations, necessary questions, corrections, and limits |
| [analysis-record.md](skills/bioinformatics-research-assistant/references/analysis-record.md) | Lightweight records, rerun information, and final-report guidance |
| [Evaluation inputs](evaluations/cases.json) and [rubric](evaluations/rubric.md) | Ten small scenarios; inputs and scoring criteria are kept separate |
| [Evaluation report](evaluations/REPORT.md) | Executed checks, evidence, revisions, and untested areas |

Install only `skills/bioinformatics-research-assistant/`. References are read when needed. Evaluation inputs, scoring criteria, and historical records are outside the distributable skill. The skill has no mandatory analysis scripts, package installation, or product-specific hooks.

## Installation

Clone this repository:

```bash
git clone https://github.com/ilsan142/bioinfo_analysis_skiils.git
cd bioinfo_analysis_skiils
```

Copy the **entire skill directory** to one of the following locations. Choose either project or user scope for each product to avoid maintaining divergent copies.

| Product | Project scope | User scope | Explicit invocation |
| --- | --- | --- | --- |
| Codex CLI / IDE | `<project>/.agents/skills/bioinformatics-research-assistant/` | `~/.agents/skills/bioinformatics-research-assistant/` | `$bioinformatics-research-assistant` or select it with `/skills` |
| Claude Code | `<project>/.claude/skills/bioinformatics-research-assistant/` | `~/.claude/skills/bioinformatics-research-assistant/` | `/bioinformatics-research-assistant` |

For user-wide installation, run the relevant block from the cloned repository. The copy is skipped if that destination already exists; compare existing files before updating them.

Codex:

```bash
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/bioinformatics-research-assistant" && \
  test ! -L "$HOME/.agents/skills/bioinformatics-research-assistant" && \
  cp -R skills/bioinformatics-research-assistant "$HOME/.agents/skills/"
```

Claude Code:

```bash
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/bioinformatics-research-assistant" && \
  test ! -L "$HOME/.claude/skills/bioinformatics-research-assistant" && \
  cp -R skills/bioinformatics-research-assistant "$HOME/.claude/skills/"
```

For project scope, copy to the corresponding directory inside your research project instead. Do not copy `evaluations/` into the skill installation. If the skill does not appear, check discovery settings or start a new session.

These locations and invocation forms were checked against the [official Codex documentation](https://learn.chatgpt.com/docs/build-skills) and [official Claude Code documentation](https://code.claude.com/docs/en/skills) on 2026-10-17. The shared files use the [Agent Skills format](https://agentskills.io/specification). Actual discovery and invocation in both products have not been tested end to end.

## Usage

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

The original Korean edition was exercised in six scenarios: well-described data, fractional expression values, complete condition/batch confounding, prediction leakage, corrected sample relationships, and an unrelated web request. The normal case was rerun after a refinement to consolidate small outputs. Seven clean-process reruns checked the resulting analysis code. Four other scenarios were reviewed but not executed.

The English edition separately passed package checks and fresh-agent regression checks for well-described data and complete condition/batch confounding. Both generated analyses were rerun in fresh processes with identical result tables. The other eight cases have not been rerun after translation; see the [English-edition validation record](evaluations/ENGLISH_EDITION.md). Historical inputs, skill snapshots, and execution records retain their original language and wording so that the evidence is not rewritten retrospectively. They are not alternative installable skills.

Real research data, analysis-figure review, full client integration, and broad reliability across models remain unvalidated. Synthetic execution is not biological validation.

To check the current package from the repository root, use Python 3 with PyYAML installed:

```bash
python3 evaluations/validate_package.py
python3 evaluations/prepare_case.py 01 /tmp/bio-skill-case-01-new
```

The second command prepares a fresh, isolated case directory using only the Python standard library. It does not run an agent evaluation. Give a fresh agent only that directory's skill and task inputs, and score its actual behavior separately. Deliver case 07's correction only after its initial result; for case 10, expose only skill metadata without forcing invocation.
