---
name: "generated-scene-diorama"
description: "Build a multi-piece printable scene diorama (village, island, market) from one approved concept image, with generated pieces (Tripo by default) under a budget, then save it to The Hoard."
---

# Generated scene diorama

Paths such as `shared/...` and `families/...` are from the root of the bookwyrm-skills repo (`~/code/bookwyrm-skills` on David's Mac). Open them from there: a `../` link resolves wrongly when this skill is opened through a link in `~/.claude/skills/`.

This skill turns a brief and a credit budget into a prototype print set of separate pieces, each printed in one colour and painted by hand, on a tiled base. The only human gate is choosing the concept. It was distilled from two runs: the Victorian Christmas village (1000 credits, about 2.5 hours) and the Isle of Berk (899 credits). The run logs and the full spec (LOG.md, SPEC-draft.md) were in another project's files and aren't reachable from here; this skill holds what they taught.

Use this skill when most pieces will be generated (image to 3D) and the budget drives the decomposition. Use `layered-diorama` (bookwyrm-dioramas) for a hand-modelled scene built bottom-up. Both save to The Hoard through the `workshop` skill.

## Inputs to settle first

- **Brief:** the theme, the style, and every element the scene must contain.
- **Budget:** a Tripo credit cap for the 3D calls plus a Meshy credit cap for the images.
- **Printer:** the exact model and its build volume. Also the nozzle, which sets the finest detail: a 0.6 mm nozzle gives about 1.2 mm features, and resin figure faces need 0.4 to 0.6 mm. The fleet and its build volumes are in `shared/print-profile/print-profile.md`; ask which one if you don't know.
- **Scale policy:** for example forced perspective, with buildings at 120 to 235 mm and adults at about 38 mm.
- **Slug:** one per product, kebab case, and never reused. Check it against The Hoard first: `christmas-village` already belonged to a lantern, so the village became `victorian-christmas-village`.

## Tools

- **Paid calls:** 3D from Tripo (Meshy only when David asks by name) through the per-project Tripo helper, which enforces a credit cap, and images from Meshy's image models. [Image to 3D](../../shared/image-to-3d/image-to-3d.md#engines-and-prices) (`shared/image-to-3d/image-to-3d.md`) says exactly how a build calls Tripo and what each call costs. Keep one working folder per scene on the Mac, for example `~/code/bookwyrm-rpg-lantern-art/<scene>-diorama/`; `berk-diorama/bk.py` there is the model for the image helper and its ledger (its 3D call is Meshy; use the Tripo helper instead). A helper refuses a call when `committed + estimate > cap`. The human-readable LEDGER.md is generated from the machine ledger and never kept by hand. An image costs 9 Meshy credits. The runs below used Meshy for 3D (20 credits a mesh, 29 a leaf), so rescale their numbers.
- **Free work:** headless `bpy` in the cloud container (`pip install bpy`) handles blockout, clay renders, procedural ground and props, assembly and print export. The Berk run had scripts for each (render_clay, make_ground, make_props, assemble, export_print); they were in that project's files, so expect to write them again.
- **Moving files:** device commits refuse files over about 25 MB. Send big meshes in 24 MB chunks, rejoin them with `cat`, and check sha256. Project files cap at 10 GB, so clear superseded assembly and print folders once David agrees.
- **Optional fan-out:** stages 5 to 9 (decide, generate, render and review, retry) can run as a Claude workflow, only when David opts into workflows. A dry run of the earlier one cost about 1.6M tokens for 6 elements.

## Stages

Levels: L0 is the scene, L1 an element, L2 a part, L3 a sub-part. **Hard cap at L3.** Both runs stopped at L2.

0. **Plan.** Write PLAN.md (levels, stopping rule, budget split) and start DECISIONS.md. DECISIONS.md logs every call you make in David's place, with its reason.
1. **Concepts.** Make 3 or 4 candidates in parallel, each from a shared style preamble plus a theme paragraph that **lists every element**. **G1 (human):** David picks one and confirms the budget. Treat the choice as open until confirmed, and pause anything started on a retracted pick.
2. **L1 decompose.** Crop each element from the approved concept. Prune first: model simple geometry and the ground in Blender, and drop low-weight extras. For every element, record its footprint, its facing (yaw relative to the concept camera) and its position in `elements.json`. Record the organising features (roads, squares, water) and the **relations** (faces the road, rings the square, depth order, part-to-part such as "the nave runs back from the tower door") in `layout.json`.
3. **Blockout (G4a).** Place boxes at the planned size, facing and position on a base sized **from the layout**, then render from the concept camera. A cold reviewer scores composition, density, scale and facing, and checks every relation pass/fail. Fix the facing and base size here, because growing a fixed base later is not free.
4. **Element art (G2).** Make one image-to-image per element from two references, the crop and the whole concept. The art must show the element as the concept crop shows it. An automatic check blocks on structural mismatch (`art_ok: false` means regenerate for 9 credits, or log a waiver), and it is never skipped. Skipping it cost about 67 credits on the village against a 9-credit fix, and on Berk it would have caught both bad longhouses before they were meshed.
5. **Pilot.** Run one cheap, typical element end to end to prove the chain.
6. **L2 decompose.** Use one agent per element, giving it the stopping rule and the element's allowance. It writes `plan.json` with explicit numbers per node and a sculpt prompt per leaf.
7. **Generate.** Make every sculpt input, then every mesh, through the ledger.
8. **Clay renders.** Render the art beside the clay mesh at print size, one job per leaf in parallel. Serial rendering was the slowest step, at 29 minutes.
9. **Leaf review (G3).** One cold reviewer per element sees only the art, the crop and the clay render. Each leaf gets a verdict of pass, retry-detail, retry-shape, retry-art or retry-interface, plus fragile features. The review is a triage for you, not a gate: it catches shape and interface failures but misses fine-detail ones (it missed the Berk cliff house and longship). Look at every clay render yourself before accepting it. Treat a pass with faithfulness or detail of 2 or less as a retry.
10. **Retries.** Pay for retries from the reserve, in review priority order:
    - **Detail:** one retry with a sharper sculpt input, then split.
    - **Shape:** single view first, four views on the second failure.
    - **Art:** regenerate the art before any 3D.
    - **Interface:** regenerate the child that doesn't own the surface.
11. **Assemble and review the scene (G4b).** Render a matched view from the concept camera. A cold reviewer scores each category, gives an overall percentage of faithfulness, and checks each relation pass/fail. Loop with free fixes first (cut, rotate, reseat, move, rescale, ground relief), then paid regenerations. Exit at 80% faithful, or after two rounds that each gain less than 5 points, or when the scene-fix reserve is spent. Never call a version done before a cold review has scored it. If David is around, invite image pins on the matched view, one fix per pin, and apply them all in one pass.
12. **Print set.** Build `print-vN/`:
    - Ground tiles with joints (magnets or clips).
    - Open floors where light goes in.
    - Rod sockets for flying pieces.
    - Every part closed and fitting the bed.
    - `parts.json` with the size, face count and print count of each part.
    - PRINT-AND-TEST.md with the claim level and known gaps.
13. **Save for The Hoard.** When David approves a version, follow the `workshop` skill: save it as a draft change set for `<slug>`, with the generating scripts committed under `projects/<slug>/` in davidray/bookwyrm-dioramas. Its `piece.json`:
    - `kind: diorama`.
    - `rights.design: ai-assisted`.
    - `ip: none`, or the third-party world (for example `how-to-train-your-dragon`) with `personal-use-only`.
    - One component per print file.
    - The matched-view render as the first image.

    Version and status are David's at promotion; tell them the status the evidence supports (`digitally-validated` until something is printed). Never promote it yourself.

## Stopping rule (per node)

A node is a leaf when all of these hold:

1. Its longest printed dimension is at most 120 times its finest signature detail.
2. It is one object: whole, centred, and one print and paint segment.
3. The split fits the node's allowance and still leaves one retry.
4. If it splits, every shared surface (gable walls, sockets, eave line) belongs to exactly one child, and both prompts say so. Three of the village's five first-pass failures were roofs and bodies that disagreed.
5. Don't split a building whose silhouette is the point, unless a lift-off roof is needed for light and the whole fails the ratio by more than about 20%.

## Budget split

| Line | Share |
|---|---:|
| Concepts | 4–5% |
| Element art | ~13% |
| Leaves, first pass including the pilot | 55–60% |
| Reserve for leaf retries | at least 15% (first-pass failure is about 25%; retries nearly always pass) |
| Reserve for scene fixes | at least 7%, held until G4b exits |

Size each element's allowance from its ratio, not from a flat tier. When the allowances can't pay for what the rule asks, drop an element or merge repeats rather than starve the hardest ones. Never call the budget final before G4b exits, and tell David the scope and rough cost before any paid batch.

## Reporting

- Post the concept options and the budget at G1. Then post each assembly's matched view with its score and open gaps, and the print set with its claim level.
- Pin-style feedback on matched-view images works well, and David prefers it for layout notes.
- Keep a short project memory: thread, folders, ledger totals and the current version.