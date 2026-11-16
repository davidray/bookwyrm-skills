---
name: lithophane-lanterns
description: Design, model, test, and package 3D-printable LED lithophane (lithopane) lanterns with image-bearing translucent panels, serviceable lighting, and evidence-backed fit and release claims. Use for new lanterns, adaptations of visual or mesh references, panel and light-source redesigns, scale changes, print troubleshooting, and release review. Exclude open-flame lanterns and ordinary opaque lamps without lithophane panels.
---

# Lithophane lanterns

Create an illuminated object whose exterior, panels, light path, assembly, and print process work as one product. A convincing render is only visual evidence; a lithophane lantern succeeds when the printed panels read under the actual light, fit and remain retained, and the light can be installed, switched, and removed.

This skill covers the whole lantern lifecycle, from brief and concept through part-by-part decoration, print engineering, and locked release.

## Establish the real design inputs

Record before committing to architecture:

- authoritative concept or reference views and the visible properties to preserve;
- intended printer, nozzle, material, layer height, and maximum build volume when known;
- the exact low-voltage LED, tea light, cable, switch, controller, or battery envelope;
- panel count, artwork, viewing direction, target size, and whether panels must be removable;
- finish mode: single-color and hand-painted, multicolor, separate materials, or another explicit plan;
- service expectations, handling context, and the requested release level.

Use a battery-powered or otherwise low-voltage LED source. Exclude open flame. Do not infer hardware size, switch access, heat behavior, tolerances, hidden construction, or optical performance from concept art or a product label. If the physical light is available, measured dimensions outrank nominal packaging dimensions.

Read [workflow and gates](references/workflow-and-gates.md) for a new build or a material redesign. Read [engineering](references/engineering.md) before fixing dimensions, interfaces, segmentation, or orientation. Flat structural parts (divider blades, controller and floor plates, diffusers, flat lid decks) are laser-cut acrylic by default, with a printed fallback; see its laser-cut acrylic section.

For Dave's lantern projects, read [Dave's lantern print profile](references/dave-print-profile.md) before selecting the build envelope, exterior feature sizes, segmentation, material, nozzle, compatibility target, lithophane recipe, or fit clearances. It holds physically proven settings; reuse them instead of proposing new coupons for the same interfaces. Keep project-specific proportions, visual approvals, hardware, and exceptions in the project checkpoint.

When the user hands every decision to you, follow the autonomous-run rules in [workflow and gates](references/workflow-and-gates.md): keep every gate and use an independent reviewer in place of the user's approvals.

For tool setup (headless Blender in a container, slicing from the command line), read [tooling](references/tooling.md).

For Dave's lantern projects, read [Dave's art pipeline](references/dave-art-pipeline.md) before generating concept, part, or panel art or any AI mesh, and before spending generation credits.

In a series of lanterns, keep the shared interfaces consistent: panel slot and retention, divider or LED post, strip, hardware plate, and tolerances. Overall size is a target the approved art may break; say so when it does rather than distorting the art to match a sibling.

## Select the lighting architecture

For Dave's lantern projects, record one of these standard lighting architectures before fixing the internal structure: **split lighting**, **lit shell**, **puck light**, or **tea light**. Do not silently combine their assumptions.

- When **split lighting** is selected, read and apply [standard lighting architectures](references/standard-lighting-architectures.md). The named choice imports the established controller and power system, swappable hardware plate, four-chamber split divider (printed core post plus four flat laser-cut or printed blades, never one piece), and four-strip lighting topology as one baseline system.
- When **lit shell** is selected (an opaque hollow sculpture with lithophane regions printed into its wall, lit from a central LED post), read and apply its section of the same reference. It shares the split-lighting controller, power, and hardware plate but has no divider.
- For **puck light** or **tea light**, model the actual selected light and its service envelope. Do not inherit the split-lighting PCB, battery, divider, or strip topology unless the user explicitly requests a hybrid.

Treat a standard architecture as a reusable starting system, not proof that it fits a new lantern. Preserve its locked interfaces and revalidate the lantern-specific optical spacing, divider fit, service path, heat behavior, and enclosure integration.

## Protect function before decoration

Block out these systems together:

1. actual light-source envelope and insertion/removal path;
2. switch, finger, cable, battery, and ventilation access as applicable;
3. light-to-panel spacing and any diffuser or hotspot-control volume;
4. lithophane panel field, thickness range, frame overlap, clearance, and extraction path;
5. structural frame, base, roof, retention, and intended print segmentation;
6. protected silhouette, focal forms, and decorative hierarchy.

Fit purchased parts (lights, batteries, switches) with generous clearance, so a slightly different part from another pack still fits. Never design a fit that only works if the part is exactly right (David, 2026-11-15). Model clearance and motion reserves as named, visible non-production objects. Do not decorate over them or silently shrink them. A scale change is a redesign whenever it changes the protected hardware envelope, minimum printable features, panel thickness range, light spacing, or service access. Never uniformly scale a finished reference mesh and call the result engineered. To make a small tea-light version of a finished lantern (one-piece body, glued-in panels), read [miniaturize a lantern](references/miniaturize.md).

Record how panels go in and how the roof or lid comes off at blockout, and show it in the review. Default to positive roof location (pegs or a keyed lip); gravity-only seating needs the user's explicit acceptance. For Dave's lanterns, add the central lid tie-down: an M4 eye bolt in a heat-set insert in the lid, a wire down the post bore, and an M4 bolt, washer and nut through the hardware plate. Reserve its axis column at blockout (see [engineering](references/engineering.md), lid tie-down).

Never use dowels (David, 2026-11-16). Wherever two printed faces are glued, align them with printed alignment tabs: a male tab 4.0 mm in diameter and 4.0 mm tall on one face, a female socket 4.2 mm in diameter and 4.2 mm deep in the other. Joints that are not glued, hinges and pivots need no tab. Plan them when you choose the segmentation; see [engineering](references/engineering.md), glued joints.

## Decorate part by part, and let the art win

Whole-lantern decoration has fallen well short of the concept every time it was tried. After the overall concept and the functional blockout are approved, split the decoration into a few parts, make and approve concept art for each part alone, model each part separately until it is faithful to (or better than) its art, and only then assemble and compare with the overall concept. Read [workflow and gates](references/workflow-and-gates.md) gate 3 for the procedure.

The approved art is the priority, not the blockout geometry. When a faithful part breaks the blockout, change the structure (wider plinth, wider body, taller lantern, lid pocket) or ask the user; do not squash, fold, clamp, or stretch the art to fit. Scale decoration uniformly. Never stretch carved or organic detail along one axis.

Label your own ideas. A printability or production change you propose is a proposal until the user accepts it; never write it into the approved visible properties, and do not alter the approved look for printability risk you have not evidenced.

Keep lithophanes as separate replaceable parts by default. Integrate them only when the process and assembly plan make that deliberate. Give every panel a positive seat and retention strategy, plus a plausible assembly and replacement path. Mere intersection with a frame is not retention.

## Build panels as optical parts

Use actual image-derived relief for production panels. Textures, emission, and images mapped onto flat plates are presentation-only. Dark image regions normally become thicker and transmit less light; bright regions become thinner and transmit more. Confirm polarity with a rendered height preview or test strip before generating all panels.

Treat base thickness, relief range, image resolution, tonal curve, border, panel orientation, and light spacing as process-dependent parameters, not universal constants. Preserve important faces and silhouettes through crop and tonal preparation; avoid relying on tiny low-contrast details that disappear in transmitted light. Sharpness is limited by the extrusion line and by light scattering, not by layer height: detail narrower than about two line widths won't read (see the detail limits in panels and optics).

Read [lithophane panels and optics](references/panels-and-optics.md) whenever creating, replacing, resizing, or diagnosing panels.

## Keep evidence boundaries explicit

In Blender or another source model, separate at minimum:

- export-authoritative structure;
- export-authoritative lithophane geometry;
- functional/service reserves and motion paths;
- presentation-only artwork, materials, glow, and staging.

Use editable source geometry and repeatable generators where they improve reliability. Code is for structural and parametric geometry only. Never hand-build detailed or decorative parts in code, including stairs, decks, railings and brackets; generate them with Tripo, through the Tripo API (David, 2026-11-14). An approved AI-generated part mesh is authoritative for visible form: keep it as the exterior and cut or add the function into it (hollowing, slots, seats, bays, lid pockets, hidden internals). It is not functional lantern architecture until those openings, load paths, panel seats, service paths, segmentation, and printable topology are deliberately added and verified, but the visible surface stays as the art made it.

Produce neutral production-only views as well as attractive lit views. A useful review packet normally includes a matched three-quarter view, front/elevation view, neutral geometry view, cutaway, exploded/service view, underside access view, and isolated panel previews. Put the approved concept or part art beside the model on every sheet. Show reserves only in functional views, with a clear legend.

Read [modeling and evidence](references/modeling-and-evidence.md) when building the source scene, adapting a generated mesh, or preparing review artifacts.

## Retire uncertainty with small physical tests

First check the proven settings in the print profile: lithophane relief, panel print settings, pane seats, sliding fits, tongue and groove, and wire exits are already physically proven for Dave's lanterns, so do not propose new coupons for those interfaces. For a genuinely new interface, use the cheapest representative coupon before a long print. Common coupons include:

- the actual light-source opening or carrier interface;
- panel channel, ledge, latch, or roof-capture cross-section;
- lithophane tonal/thickness strip under the intended LED and material;
- diffuser spacing and hotspot test;
- joint, roof key, detent, cable route, or support-removal sample.

Record the printer, material, orientation, slicer profile, nominal dimensions, measured result, and user verdict. A passing coupon locks only that interface under those conditions. If the physical result contradicts the model, redesign from the physical result and refresh every affected visual, dimensional, and audit artifact.

## Gate claims by evidence

Do not export or label a complete production set while a blocking interface remains only visual or assumed. Audit the actual exported meshes and sliced parts, not only the Blender scene. Inspect units, bounds, components, manifoldness, degeneracy, positive volume, gaps, orientation, supports, layer behavior, and round-trip import.

Keep optical, mechanical, visual, and release claims separate. A lit render does not prove transmission. A watertight mesh does not prove assembly. A successful slice does not prove fit. One fit ring does not qualify the entire lantern.

Read [validation and release](references/validation-and-release.md) before production export, print instructions, packaging, or any claim that files are ready to print or release.

## Deliver a durable project state

Maintain a checkpoint whose top block is the current state, rewritten every session: gate, evidence level, active files, open decisions, and next step. Below it, keep the dated history. The checkpoint identifies the active source, exact accepted decisions, protected interfaces, measured hardware, panel parameters, physical results, superseded files, open risks, current evidence level, and next unsatisfied gate. Preserve user-approved visual references and working branches; change locally rather than destructively replacing them.

For release, provide the editable source, production meshes, panel-to-face mapping, quantities, material and orientation guidance, assembly/service order, hardware requirements, tested and untested interfaces, safety boundary, validation results, and the highest supportable claim level. Avoid the unqualified label “print-ready.”

When the user approves a version for printing, lock it by pull request under `lanterns/<lantern>/v<N>/` in this repository, with one 3MF per part, every generating script, the approved art, the review sheets, and a README. See [validation and release](references/validation-and-release.md). Then follow the publish-to-the-hoard skill (bookwyrm-rpg `services/library/skills/publish-to-the-hoard/SKILL.md`): it adds `piece.json`, runs `tools/check_piece_json.py`, and leaves the import to The Hoard after the merge. At the end of a session that changed a lantern's meshes without locking, say so in one line.
