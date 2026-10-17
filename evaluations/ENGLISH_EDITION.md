# English edition validation

Date: 2026-10-17. The four distributed skill documents were translated into English while preserving their scientific decision rules, conditional reference loading, and user-language behavior. English and Korean READMEs describe the motivation, installation, and limits. Historical inputs and execution records retain their original wording.

The skill files tested in this edition are identified by [skill-en-v1.sha256.json](runs/skill-en-v1.sha256.json). The subsequent notebook-workflow update has a separate [validation record](NOTEBOOK_WORKFLOW.md). Earlier Korean-edition results are documented in [REPORT.md](REPORT.md); those results must not be treated as a rerun of the English edition.

## Scope

Two fresh agents received only the translated skill and the original task inputs for cases 01 and 03, in separate temporary directories. They did not receive the rubric, expected answers, or the parent conversation. Task inputs remain in Korean; this checks use of English instructions with Korean user requests, not broad multilingual reliability.

## Observed behavior

| Case | Observations and outcome | Evidence |
| --- | --- | --- |
| 01: well-described synthetic data | Matched all 8 sample IDs, identified 4 independent donors per condition and balanced batches, then implemented comparisons after checking the inputs. Adjusted treated-minus-control effects were +1.025, +0.100, and -0.100 log2 intensity. Marker A's leave-one-donor-out range was +0.98 to +1.06. Continued without repeated approval and labeled the results exploratory and synthetic. Passed the applicable case criteria. | [Analysis record](runs/en-01/analysis_record.txt), [results](runs/en-01/results.tsv), [public execution trace](runs/en-01/public_trace.jsonl) |
| 03: complete condition/batch confounding | Confirmed the 3/0, 0/3 condition-by-batch table and design rank 2 of 3. Reported observed group differences +2.0 and +0.5 while marking the batch-adjusted treatment effect non-identifiable. Did not report treatment p-values or confidence intervals, or claim that correction solved confounding. Passed the applicable case criteria. | [Analysis record](runs/en-03/analysis_record.md), [results](runs/en-03/descriptive_results.tsv), [public execution trace](runs/en-03/public_trace.jsonl) |

The public traces show output inspection before dependent implementation. No rubric or other-project reads were observed. Each run kept code, a result table, and its execution/report records together without introducing a generic pipeline. Neither generated a figure; actual figure inspection remains untested. Public traces contain tool calls, outputs, and user-facing explanations, not private reasoning or system prompts.

## Execution and format checks

Both generated analyses were copied into new temporary directories and rerun in fresh Python processes. Both exited with code 0, and their result tables were byte-identical to the archived outputs. Bounded numeric checks confirmed the expected effects and the non-identifiable status. Original inputs matched the case definitions. See [english_replay_checks.json](runs/english_replay_checks.json).

The skill-creator validator and the repository's package validator passed. Checks covered shared metadata, absence of untranslated Korean in the four distributed documents, bilingual README links, local reference links, Markdown fences, and the ten evaluation inputs. See [English-edition format checks](runs/english_format_checks.txt).

Whitespace checks apply to maintained files with `git diff --cached --check -- . ':!evaluations/runs/**'`. Archived evidence is excluded because it preserves original CSV/TSV line endings and the spacing of generated tabular output. `.gitattributes` preserves archived bytes instead of normalizing them. No historical result was reformatted to make a formatting check pass.

## Limits

Only cases 01 and 03 were rerun with the English edition. The other eight cases were not rerun after translation. The earlier Korean edition's six executed scenarios and four review-only scenarios remain historical evidence, not results for this edition. These are small, single-run behavioral checks with shared tooling and no no-skill control. They do not establish biological validity, robust multilingual performance, performance across models, or actual Codex/Claude Code installation and discovery.
