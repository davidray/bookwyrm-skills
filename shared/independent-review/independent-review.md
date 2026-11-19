# Independent review

How a separate reviewing agent (the critic) checks a build before David sees it, and how the builder uses its verdict. The same for every family. When to call one is the family's rule: [reviews](../../families/printable-container/references/reviews.md) (`families/printable-container/references/reviews.md`) for containers, [workflow and gates](../../families/lithophane-lanterns/references/workflow-and-gates.md#autonomous-runs) (`families/lithophane-lanterns/references/workflow-and-gates.md`) for lanterns, the cold reviews in `families/generated-scene-diorama/SKILL.md`, and any time David asks.

Self-review grades generously. In the Moria test the builder passed its own work until a skeptic found a blurred inscription and stale files; in the lantern tests self-review missed a mismatched panel set and a body that had drifted from the concept.

## The brief the reviewer gets

Give it the files, not the builder's conclusions:

- the governing references: approved concept and part art, and which property each one governs (from `BRIEF.md`);
- David's decisions, verbatim, and the brief's definition of done;
- the current files: renders of the exported meshes (neutral material, matched to the concept's view), the exports themselves, check output (`*.json`, logs), and the print folder with its README and PRINT-AND-TEST;
- a neutral part map: each part, its print orientation, and what is separate, glued or moving;
- the gate the build is about to reach, and the checklist for it (the family's review lists and [evidence and claims](../evidence-and-claims/evidence-and-claims.md), `shared/evidence-and-claims/evidence-and-claims.md`).

Leave out the builder's measurements, reasoning, scores and recommendation. A reviewer once inherited a wrong ratio and proposed a stretch from it. It measures for itself.

## What it checks

1. **Faithfulness:** the matched view against the governing image, property by property: silhouette, proportion, focal point, motifs, story details. Departures missing from the compromise register.
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
