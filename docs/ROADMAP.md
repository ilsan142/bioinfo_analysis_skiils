# Candidate extensions after the communication update

Research date: 2026-10-21. The five skills listed in the repository README are implemented. Everything below is a proposed extension, not an installed skill or validated workflow. Priorities reflect this repository's researcher-facing purpose, not a survey ranking of available products.

## 1. Scientific manuscript review and response

Candidate: `scientific-peer-review-assistant`.

Input: a manuscript, figures, supplements and the review brief; optionally received reviewer comments and a revision record. Output: a bounded summary of the central claims, prioritized concerns with exact locations and evidence, and feasible remedies. A response mode would map each received comment to the actual change, evidence, and unresolved issue rather than claiming every requested experiment was done.

This adds independent assessment across the whole scientific argument, beyond drafting a requested manuscript section or reviewing one figure. Start with review mode; add response mode only when recurring revision tasks warrant it. Smaller reviewer edits already fit the manuscript skill and do not need a new dependency.

The [Broad Peer Review guide](https://mitcommlab.mit.edu/broad/commkit/peer-review/) emphasizes specific major/minor concerns and proportionate requests, including narrowing a claim when additional experiments are unnecessary. A future skill should distinguish an evidence-critical correction from an interesting new project. Test it on a manuscript with one central design flaw, one harmless stylistic issue, and an unreasonable request for new data. Passing means prioritizing correctly without inventing defects or demanding an unrelated study.

## 2. Research proposal and specific aims

Candidate: `bioinformatics-research-proposal-assistant`.

Input: a research question, checked literature, available preliminary evidence, resources, and the actual call or committee requirements. Output: an argument connecting the knowledge gap to aims, feasible approaches, risks, alternative outcomes, and what completion would establish.

The current planner designs an analysis from existing data. A proposal skill would design and explain a broader research program, potentially including data acquisition or experiments, and fit a specified evaluation context. It must not invent preliminary data, novelty, collaborators, budgets, institutional resources, or successful future outcomes.

Relevant sources are [MIT BE Thesis Proposal](https://mitcommlab.mit.edu/be/commkit/be-thesis-proposal/), [Broad NSF Research Proposal](https://mitcommlab.mit.edu/broad/commkit/nsf-research-proposal/), and [Broad Fellowship Application](https://mitcommlab.mit.edu/broad/commkit/fellowship-application/). Use their communication principles; recheck the current funder's actual eligibility, review criteria and formatting rules for each application rather than treating CommKit examples as current program rules. Test an unsupported novelty claim and missing pilot data before using the skill on a real application.

## 3. Scientific poster preparation

Candidate: `scientific-poster-assistant`, or initially an on-demand reference in the lab-meeting skill.

Input: existing results with explicit evidence and validation status, audience/event, dimensions, and whether a presenter will be present. Output: a content hierarchy, reading path, figure placement, concise text, and a short spoken introduction; produce an actual poster only when requested and a suitable rendering workflow is available.

The [Broad Poster guide](https://mitcommlab.mit.edu/broad/commkit/poster/) treats the poster as support for a conversation, with a clear purpose and visual emphasis. This is a different medium from slides, but it shares much of the new lab-meeting skill. Promote it to a separate skill only after real poster tasks reveal reusable layout, export and legibility checks. Test both an attended poster and a standalone display, then inspect an actual-size rendering rather than treating file export as visual QA.

## Defer generic expansion

Do not add one skill for every CommKit page. A title, abstract, or caption often belongs in the existing manuscript workflow; ordinary figure creation belongs in analysis; routine methods notes belong in the notebook. Dedicated skills become useful when the trigger, inputs, decisions, and finished artifact differ enough to warrant their own behavior and tests.

An evidence-synthesis or literature-review skill may eventually help proposals and manuscripts, but its search coverage, study appraisal and citation verification need methodological sources beyond these communication pages. It is not ready to specify solely from CommKit guidance.

## How to select the next implementation

Prefer the first candidate when the next real need is evaluating a draft or responding to substantive review. Prefer the second when choosing and defending a future research program. Start the third as a reference unless poster production becomes recurrent. Before expanding, test whether the five existing skills route independently and preserve evidence when passed a corrected or conflicting artifact.

All linked pages above were read on the research date. Related Broad pages acknowledge adaptation from MIT BE; they are communication guidance, not independent scientific corroboration. The candidate designs and evaluation suggestions here are original proposals, with no reproduced source figures or passages.
