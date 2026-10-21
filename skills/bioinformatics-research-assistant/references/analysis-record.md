# Lightweight analysis records and completion checks

Read the notebook sections when creating or updating an exploratory notebook; read other sections when choosing another record format or assembling final results. Reuse an existing notebook or analysis document if it contains what is needed. The templates below are optional; neither separate files nor every field are mandatory.

## A notebook the researcher can follow

Prefer one `.ipynb` for a coherent exploratory analysis unless the user's format, project workflow, task, or available runtime calls for another form. The notebook should be understandable without the chat transcript. Put the question, input locations and meaning, known design and unresolved assumptions, and minimal execution instructions near the start. Do not create empty sections for a whole planned pipeline before the data justify it.

Build each question as a small connected group of cells:

1. **Before execution, Markdown:** What will this check answer, why does it matter, and which verified facts or assumptions does it use? State consequential comparison or preprocessing choices here.
2. **Code and actual outputs:** Run the minimum necessary computation. Introduce each output group with its purpose, then show the counts, table, warnings, or figure needed for that question. Keep important inputs and parameters easy to find. A question can need several cells; do not impose a fixed cell count.
3. **After inspection, Markdown:** Record the observed values, interpretation, limitations, and the next question with its reason. Add this before implementing work whose choices depend on the result. Note when a choice was added after seeing the data. The chat update can be shorter, but must agree with the saved notebook.

For example, an identifier check can be followed by the actual matched, missing, and duplicate counts and a decision about whether sample-level comparisons can proceed. Do not fill these numbers or assume a successful match before executing the check. A short table can be sufficient; a notebook does not require a figure for every question.

Use direct, readable analysis code. Move long or reusable calculations to scripts when useful, while keeping their invocation, consequential parameters, output summaries, and scientific rationale visible in the notebook. Avoid a notebook that merely launches an opaque pipeline. Display the actual generated figure and inspect it with available viewing tools; successful execution or image embedding alone does not establish visual review. Do not duplicate every inline table or plot into a separate artifact unless it needs export or reuse.

## Explain outputs as in a lab meeting

Assume the reader has not seen the data, variable names, or earlier chat. Each output group should make clear **why this check matters, what the displayed quantities mean, what was observed, and how it changes the next step**. A label such as "Shape" or "Values min/max" names an object but does not explain a reason.

- For printed values, start the output block with a short `print("...")` explaining the purpose in the user's language. For tables and figures, an immediately preceding Markdown explanation or caption is sufficient. Introduce a new purpose when a cell switches questions; do not add a separate explanation before every number or repeat the same explanation in Markdown and print.
- Prefer one compact table for related checks across conditions or samples. Label dimensions as genes, cells, samples, or other actual units instead of leaving an unexplained tuple. Define terms such as nonzero entries only when that quantity informs a decision.
- Show the input files actually used and their roles when establishing provenance. Do not repeatedly dump every archive member. For identifier alignment, report matched, unmatched, and duplicate counts from the full check; matching a few example barcodes does not establish alignment. Show a small, labeled set of problematic identifiers only when needed to explain a mismatch, with the total affected count.
- Use a figure when a distribution, relationship, or pattern is easier to assess visually. Use a small table or sentence for exact counts and pass/fail checks. Do not turn every diagnostic into a plot or create extra files just to make the notebook look polished.
- Keep routine validation in executable checks with useful failure messages and summarize consequential results for the reader. Remove redundant debugging prints after exploration, but retain unresolved problems, important warnings, and evidence that changes the analysis. Do not suppress all warnings or hide failed checks for tidiness.
- After execution, interpret the actual output and state the next decision. A successful identifier check permits the next inspection; it does not establish data quality or biological validity. Keep observations distinct from expectations and do not write the conclusion before seeing the result.

Before sharing, read the rendered notebook without relying on the chat: can someone explain why each output is present, what its units are, and what follows from it? If not, improve the explanation, summarize the output, or remove a redundant display while preserving the underlying check. See the [output explanation example](collaboration-examples.md#when-turning-diagnostic-output-into-an-explanation) for a compact illustration.

## Communication review

Use this review when a notebook has become hard to follow or when preparing a summary for a different audience. Reuse the existing record; a separate communication report is not required.

- **Orient before showing:** State the biological or integrity question and introduce unfamiliar units, axes, transformations, and observation units. Explain the comparison to inspect without predicting what the data will show.
- **Explain after inspecting:** State the supported observation, cite the relevant output, distinguish interpretation from alternatives, and connect the next check to the unresolved uncertainty. A transition such as "next, clustering" does not explain a decision.
- **Match the medium:** Keep enough methods and intermediate evidence in the executable notebook for review. A meeting summary can foreground a few important results and link to the full record. Do not apply slide-style brevity to every exploratory cell or hide evidence that weakens a conclusion.
- **Audit the message:** Does the title say more than the figure or design supports? Could the reader mistake cells for donors, association for causation, or a proposed check for a completed one? Preserve independent n, material uncertainty, exclusions, and interpretation limits where they affect the message.
- **Read as a newcomer:** Can a researcher explain the question, actual observation, claim boundary, and reason for the next step without the chat? If not, repair the missing explanation or simplify a redundant display. More comments do not repair confusing variable names or an opaque analysis pipeline.

Illustrative wording, not observed results:

> Before execution: To attach treatment and donor information to the right cells, compare the complete cell-identifier sets and check duplicate keys. The summary will distinguish matched cells from unmatched or ambiguous records.
>
> After execution: Replace this example with the actual match counts and any problems. If the join is unambiguous, explain that cell metadata can now be connected and identify the next design question. This does not establish independent replication or measurement quality.

Keep finding-based headings conditional on actual observations. Later editorial reordering must not erase which choices were made after seeing results. Contrary findings that change the conclusion belong in the main explanation, even when repetitive implementation details move to linked supporting output.

Communication sources checked on 2026-10-21:

- [MIT BE Results](https://mitcommlab.mit.edu/be/commkit/journal-article-results/): rationale, evidence, and transitions between findings.
- [Broad Slideshow](https://mitcommlab.mit.edu/broad/commkit/slideshow/): audience, purpose, and orientation before displaying unfamiliar data.
- [MIT BE Figure Design](https://mitcommlab.mit.edu/be/commkit/figure-design/): correspondence between a message, visual evidence, and its setting.
- [MIT BE Coding and Comment Style](https://mitcommlab.mit.edu/be/commkit/coding-and-comment-style/): readable names and structure before additional commentary.

These are communication references, not validation of a statistical method. The rules above apply their ideas to evidence-preserving analysis; no source figures or passages are reproduced. Broad's slideshow page credits adaptation from MIT BE, so the two sites are not independent scientific evidence.

## Execution, saved outputs, and a clean rerun

- Execute during exploration and inspect each relevant result before writing dependent analysis. As the analysis settles, organize cells into a runnable order while preserving the distinction between prespecified choices and later exploration. A final linear notebook need not reproduce every failed attempt, but must retain consequential changes and their reasons.
- Use the correct language kernel and document working directory, input paths, required packages and versions, and relevant random seeds. Run through the notebook execution environment; do not fabricate execution counts or paste shell results into code-cell outputs to make unexecuted cells look executed. If the work ran as scripts, describe it as script execution.
- After consequential edits, invalidate and recompute affected downstream outputs and update their interpretation. Avoid showing old outputs under changed code. Preserve original inputs; mark any retained prior report or notebook as superseded rather than presenting two versions as current.
- Once the requested analysis is assembled, restart with a fresh kernel and execute its analysis cells in order using the documented inputs and environment. Inspect the rerun results and save the resulting notebook. This checks reliance on hidden variables, execution order, and correspondence between current code and saved evidence; it does not establish scientific validity. Do not repeat full reruns after every exploratory cell.
- Stop and address execution errors or clearly label a partial run. Keep useful completed work, identify the failing step and affected downstream results, and do not label a run successful merely because error-tolerant execution reached the last cell. For expensive stages using existing artifacts, record their origin and parameters and state exactly which computations were rerun; loading an old result is not recomputing it.
- Treat notebook-schema validation, kernel execution, inspection of numerical results, and visual review as distinct checks. If the runtime, dependencies, inputs, or resources prevent a clean rerun, record what actually ran and what remains unverified. Do not install a large analysis environment just to satisfy the preferred format.

The [Jupyter notebook format documentation](https://nbformat.readthedocs.io/en/latest/format_description.html) describes Markdown, code, and stored outputs. The [NBClient execution documentation](https://nbclient.readthedocs.io/en/latest/client.html) gives one optional way to execute and save notebooks and describes error handling. These are implementation references, not required libraries; use the project's available notebook tools. Both were checked on 2026-10-17.

## Record one question

```text
Question / why it matters:
Verified inputs and meaning: location, source, sample/feature units, prior processing
Verified design / provisional assumptions / unknowns:
Decision: comparison, reference group, covariates, filters, aggregation, exclusion evidence
Timing: prespecified / post hoc exploration / error or experimental-information correction
Execution: code location, command, or notebook execution order
Observations: actual n, effects/units, uncertainty, warnings, before/after changes
Interpretation and limitations:
Next question and reason / information needed from the researcher:
```

## Minimum connections for a rerun

- Input sources and current versions or locations, with original and transformed data distinguished. Use checksums when exact file identity matters.
- Direct links between code, key parameters, and result tables or figures. Document required access permissions or external inputs as rerun conditions.
- Language, package, and reference-data versions that affect the results; seeds for stochastic operations and remaining nondeterminism. Do not force a complete system-package inventory on a small analysis.
- Script commands or notebook execution from the beginning. Record whether a clean rerun actually occurred and any failures. Running only selected successful cells is not full reproduction.
- What was checked by opening figures and what remains unresolved. Mark figures unreviewed if they could not be opened.

## Corrections and superseded results

Identify the correction's source, old assumption and new relationship, and affected code, tables, figures, and explanations. Preserve originals and distinguish corrected metadata and current outputs. Rerun the necessary calculations and mark prior results as superseded. Even if the estimated effect is unchanged, check n, uncertainty, tests, figures, and interpretation again.

For a notebook, this includes saved cell outputs and Markdown statements that quote or interpret them. A correction to replicate relationships can change the independent n, model, intervals, and plot grouping even if the same measured values remain. Finish with an in-order clean-kernel rerun of the corrected analysis when feasible and report its status.

## What the final report should retain

1. The question and current answer, including parts the data cannot answer.
2. Data, samples, and key actual observations. Where possible, report effects, units, uncertainty, and independent n together.
3. Methods and reasons for consequential choices, major before/after preprocessing changes, and whether analyses were added after seeing results.
4. The conclusion's scope and unresolved issues. Distinguish literature facts, current executed results, candidate explanations, and proposed follow-up work.
5. Locations of code, tables, figures, and records; rerun instructions; and actual execution, rerun, and visual-review status.
6. What to check next and the uncertainty that check would reduce.

Before closing, check whether the researcher can explain the question, data, reasons for choices, observations, limitations, and next check. Provide evidence and artifacts instead of success labels. Software or format checks, synthetic examples, scenario review, analysis of real data, and independent biological validation are different levels of evidence.
