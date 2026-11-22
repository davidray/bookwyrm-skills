# Independent review

How a separate reviewing agent (the critic) checks a build before David sees it, and how the builder uses its verdict. The same for every family.

## When

The critic reviews before every gate, in every family (David, 2026-11-19): the concept, the budget, the physical check, and every gate a skill adds, such as approval of a whole sculpt. A gate is not put to David until the critic has reported on what he will be shown. The review covers what that gate decides:

- **Concept:** the image against the brief and David's words, and the list of what it invents. Any image that feeds modeling (concept, part art, sheet, 3D input) that shows a finish (plating, paint, patina, antiquing, weathering, a metal or cast look) or detail softened for one is a FAIL, as is a finish mock-up that is unlabelled or used as modeling input ([concept and faithfulness](../concept-and-faithfulness/concept-and-faithfulness.md#concept-art-feeds-modeling-a-finish-mock-up-does-not), `shared/concept-and-faithfulness/concept-and-faithfulness.md`).
- **Budget** (and any raise): the plan's calls, engines and prices against the brief and the skills, and the reserve against the rule in the `workshop` skill.
- **Physical check:** the print folder, exports, checks and claims, as below.

Family rules add reviews, never remove them: [reviews](../../families/printable-container/references/reviews.md) (`families/printable-container/references/reviews.md`) for containers, [workflow and gates](../../families/lithophane-lanterns/references/workflow-and-gates.md#autonomous-runs) (`families/lithophane-lanterns/references/workflow-and-gates.md`) for lanterns, the cold reviews in `families/generated-scene-diorama/SKILL.md`, and any time David asks. A cold review a family already requires at a gate counts as the critic's review there if it was briefed as below.

Self-review grades generously. In the Moria test the builder passed its own work until a skeptic found a blurred inscription and stale files; in the lantern tests self-review missed a mismatched panel set and a body that had drifted from the concept.

## The brief the reviewer gets

Give it the files, not the builder's conclusions:

- the governing references: approved concept and part art, and which property each one governs (from the build's brief, `read_build`);
- David's decisions, verbatim, and the brief's definition of done;
- the current files: renders of the exported meshes (neutral material, matched to the concept's view), the exports themselves, check output (`*.json`, logs), and the print folder with its README and PRINT-AND-TEST;
- a neutral part map: each part, its print orientation, and what is separate, glued or moving;
- the gate the build is about to reach, and the checklist for it (the family's review lists and [evidence and claims](../evidence-and-claims/evidence-and-claims.md), `shared/evidence-and-claims/evidence-and-claims.md`).

Leave out the builder's measurements, reasoning, scores and recommendation. A reviewer once inherited a wrong ratio and proposed a stretch from it. It measures for itself.

## What it checks

1. **Faithfulness:** the matched view against the governing image (never a finish mock-up), property by property: silhouette, proportion, focal point, motifs, story details. Departures missing from the compromise register.
2. **Claims:** every claim in the README, checkpoint and gate report against the evidence that would support it. Numbers retyped instead of taken from check files. A status or word ("fit-tested", "print-ready") stronger than the evidence ladder allows.
3. **Freshness:** renders, checks and print files made from the current source, with no superseded file in the print folder.
4. **Printability:** the family's before-a-long-print list: thin free-standing features, carved faces on the bed, supports trapped against carving, parts that start above the bed, bed fit.
5. **The gate itself:** whether the build is really at the gate it claims, and whether the decision put to David is the one the evidence calls for.

## What it reports

One verdict per item: **PASS**, **FAIL** or **CAN'T CHECK**, each with the evidence (file path, image, measured number) and, for a FAIL, what would close it. Then the list of what it could not check and why. No overall score: a score once passed a blockout at 85/100 that was plainly far from the concept.

## Using the verdict

- The builder fixes each FAIL and has it re-reviewed, or puts it to David at the gate in the reviewer's words. The builder cannot waive a FAIL, and nor can the reviewer.
- A FAIL still open at a draft or release goes at the top of its README as unresolved, not under known shortfalls.
- The gate report says that a review ran, links its report, and lists any open FAILs.
- A review covers the files it was shown. Any change to geometry or art after it needs a new review for what changed.
