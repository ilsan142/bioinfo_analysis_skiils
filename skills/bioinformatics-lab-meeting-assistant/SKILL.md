---
name: bioinformatics-lab-meeting-assistant
description: Prepare or revise bioinformatics lab meeting slide content, storyboards, and speaker notes from existing evidence. Use for research updates, design discussions, or editing research slides for audience understanding.
---

# Prepare a lab meeting from existing evidence

Help the audience understand what the work currently supports and make the next research decision. Follow the user's language; default to Korean when no preference is apparent. Keep scientific identifiers and units precise.

Use this skill independently with the materials available. An analysis plan, completed notebook, another skill, and a presentation application are not prerequisites. Honor the requested format; a narrative and storyboard with speaker notes can be the finished deliverable.

For revisions to existing slides, read [slide revision guidance](references/slide-revision.md). Return the requested slide-by-slide changes without requiring a new talk outline, time budget, or separate report. Inspect supplied slides before diagnosing their layout; text-only inputs support wording and proposed layout changes, not a claim of visual inspection.

## Establish the meeting brief

Recover the audience, their relevant background, speaking time versus discussion time, and intended decision from the request and existing records. State reasonable assumptions if these are unspecified and continue drafting. Ask only about a missing constraint that materially changes the message; routine outline and format choices do not need approval.

Distinguish a results update, troubleshooting discussion, and review of a proposed design. A design discussion may appropriately spend most of its time on alternatives and their consequences. Do not impose a slide count or a universal sequence.

## Read the evidence before shaping the story

- Inspect the relevant notebook cells and saved outputs, result tables, figures, analysis plan, and decision history. Record enough of each artifact's version and location to retrieve the evidence, such as file plus cell ID, section, table row, or figure panel.
- Distinguish outputs visible in the supplied record from results independently checked during this task. Existing execution counts alone do not establish that current code produced every output. Mark stale, conflicting, or missing evidence; do not require a full rerun to prepare the talk.
- Identify the biological question, comparison direction, measurement scale, independent experimental unit, replication, and major processing choices needed to interpret the selected results. Do not count cells, reads, or technical replicates as independent biological samples.
- Separate observed findings, literature context, interpretations, proposed work, and illustrative schematics. Use visibly distinct labels where a listener could mistake a proposal or expected pattern for an observation.
- For each consequential claim, retain its source, evidence status, and limitation. Include available effect size, units, uncertainty definition, and independent sample count. Say when uncertainty was not estimated rather than inventing it.
- Read supplied literature supporting substantive background claims; give a retrievable citation and accurate scope. If a source cannot be checked, label that limitation or omit the dependent assertion. Do not start a new literature review or analysis merely to fill the talk.

An absent result, failed analysis, or unresolved confound can be the central finding. Keep the original notebook, exploration history, and outputs intact. Do not rewrite exploratory decisions as prospective hypotheses or hide an inconvenient result that changes the conclusion.

## Build a claim-driven storyboard

Write the current answer to the research question in language warranted by the evidence, including when it remains unanswered. Select a short path from the biological motivation through the evidence to the decision the group can help make. Reorder the explanation for comprehension without falsifying the order in which discoveries and decisions occurred.

Give each presentation segment a clear job. A slide title should state the supported takeaway or unresolved question, not just an assay name. Keep decisive caveats next to the claim; move optional procedural detail to notes or backup material. Material counterevidence belongs in the main narrative when omitting it would alter the audience's conclusion.

Place one concise, evidence-bounded message at the top of each slide. Use natural spoken language in the audience's language, avoiding literal translations and vague topic headings. Aim for a message recognizable at a glance; a three-second reading goal is a design heuristic, not a measured comprehension result. An unresolved question remains appropriate when the evidence cannot support a conclusion.

For each proposed slide or spoken segment, provide the fields that make it usable:

| Element | What the presenter needs |
| --- | --- |
| Message and purpose | The question or bounded claim and why this audience needs it |
| Display | Existing figure/table and panel, brief text, or explicitly labeled proposed schematic |
| Evidence | Source locator, evidence status, independent units, relevant uncertainty, and limiting assumptions |
| Speaker notes | How to read the evidence, what it shows, what it cannot show, and a transition to the next question |
| Timing and discussion | A plausible time allocation and any specific feedback needed at this point |

Do not force separate inventories when these fields fit naturally in the storyboard. Use concise spoken notes rather than reading a dense notebook or placing the full script on slides. Allocate time to unfamiliar concepts and consequential decisions, leaving the requested discussion time available. Mark timing as an estimate unless actually rehearsed.

Read [the worked example and source notes](references/storyboard-example.md) when a claim is ambiguous, a decision needs sharper framing, or a compact example would help.

## Make the visual evidence readable

Open and visually inspect the actual figures selected for the talk, including embedded notebook images when present. Check that displayed panels support the titles and that axes, units, transformations, legends, sample coverage, and interval meanings can be understood. A filename or caption is not a visual inspection. If viewing is unavailable, say which visual checks remain incomplete and continue with inspectable evidence.

Introduce unfamiliar encodings in the notes before interpreting them: what a point or line represents, which comparison to inspect, and what uncertainty means. Distinguish a cell-level display from donor-level inference.

Choose the layout to expose the relevant comparison or sequence. Avoid imposing the same two-column or card arrangement on every slide; retain paired panels when they aid a real comparison. Use brief labels and minimal body text, leaving verbal explanation to the presenter. Simplify technical labels only after checking their meaning, retaining units, transformations, comparison direction, and statistical definitions. Replace dense footnotes with a compact legend for necessary conditions and source-linked notes for optional detail; keep conclusion-changing limitations and required attribution visible.

Suggest or make presentation copies only within the requested scope. Preserve originals and source links. Enlarging labels or separating panels must not conceal a discordant sample, change a comparison, silently crop meaningful ranges, or remove uncertainty essential to the claim. Label hypothetical diagrams and predicted patterns as schematic or proposed. New estimation or data selection is additional analysis, not cosmetic slide preparation.

When a redraw is requested, prefer familiar biological displays that expose the comparison and experimental units. Do not introduce hexbin unless explicitly requested; an existing hexbin is not a scientific defect merely because it differs from this presentation preference.

## Make the requested feedback actionable

Frame discussion around a decision the audience can resolve: the competing explanations or options, evidence for each, what remains unknown, and what observation would change the choice. Include a recommendation when supported, with its reason and limits. Avoid ending solely with a generic request for comments.

For a proposed next experiment or analysis, state the uncertainty it addresses, required control or independent unit, expected output type, and decision criterion at the level justified by the supplied plan. Label unestablished operating values as proposed. Do not invent pilot results, guarantees of power, causal mechanisms, or feasibility evidence.

## Review and deliver

Read the sequence of titles and transitions as a scientific argument. Check that conclusions agree with the inspected artifacts, nonsignificance is not presented as proof of no effect, and confounding is not explained away by a successful software run. Keep exploration, independent confirmation, and technical validation distinct.

For a full meeting, return the usable narrative/storyboard and speaker notes in the requested form, with source links, a time budget, and explicit feedback decisions. For a targeted revision, use the slide-by-slide format in the revision guidance unless the user supplies another format. Briefly identify unavailable evidence or unfinished visual checks and distinguish proposed work from completed preparation. Claim a rendered deck, rehearsal, rerun, or biological validation only if that work actually occurred.
