---
name: printable-container
description: Design decorative 3D-printable containers from concept art or a brief through dimensional architecture, editable modeling, carved relief, lithophanes, fit tests, printable STL files, and release documentation. Use for boxes, chests, cases, lanterns, enclosures, sculpted figural containers (such as a figure holding a print-in-place ring box), and similar hollow assemblies, including their lighting and controller boards; do not use for ordinary standalone miniatures with no container, purely visual renders, or safety-critical pressure, medical, food-contact, mains-voltage, open-flame, or high-energy battery products without domain-specific engineering requirements.
---

# Printable container

Paths such as `shared/...` and `families/...` are from the root of the bookwyrm-skills repo (`~/code/bookwyrm-skills` on David's Mac). Open them from there: a `../` link resolves wrongly when this skill is opened through a link in `~/.claude/skills/`.

Turn a visual idea into a usable, manufacturable container without quietly designing away what made the concept appealing. Treat visual design, protected function, mechanical architecture, manufacturing, physical evidence, and release claims as related but distinct systems.

References:

- [concept and faithfulness](../../shared/concept-and-faithfulness/concept-and-faithfulness.md) (`shared/concept-and-faithfulness/concept-and-faithfulness.md`) (shared): new or substantially changed designs.
- [decorative relief](references/decorative-relief.md): carved exteriors, feet, handles, mating features.
- [lithophanes](references/lithophanes.md): lit panes, scene images, inscriptions and fonts.
- [engineering and validation](references/engineering-and-validation.md): joints, stack-ups, energy safety, orientation, exports.
- [image to 3D](../../shared/image-to-3d/image-to-3d.md) (`shared/image-to-3d/image-to-3d.md`) (shared): engines and prices, prompts, multi-view sheets, scaling and judging for generated figures, ornaments and carving.
- [moving parts and figures](references/moving-parts-and-figures.md): hinges, print-in-place mechanisms, sculpted figures, filament saving.
- [lighting and electronics](../../shared/lighting-and-electronics/lighting-and-electronics.md) (`shared/lighting-and-electronics/lighting-and-electronics.md`) (shared): LED scenes on WLED, controller boards, lighting tests.
- [box-family standards](references/box-family-standards.md): house dimensions, hardware and defaults.
- [design rules](../../shared/design-playbook/design-playbook.md) (`shared/design-playbook/design-playbook.md`) (shared): twenty rules from the travel cases; read before a new box.
- [reviews](references/reviews.md): review checklists and when the critic reviews.
- [project records](references/project-records.md): checkpoint, test and release records, and the release-and-lock layout.

## Begin with authority and evidence

Before modeling, identify the authoritative references, explicit user requirements, actual contents and hardware, available printers/processes, intended energy or light source, project-specific definition of done, and which decisions remain provisional. Preserve original references and measurements. Do not infer hidden construction, exact dimensions, materials, electronics, or mechanisms from concept art. Hold open-flame or other safety-critical designs unless suitable domain requirements, materials, clearances, tests, and acceptance criteria are supplied; never imply ordinary printed plastic is flame-safe.

Before using concept art, compare its proportions with the real envelope. Render a neutral guide of the real case (front-left and back-right, lid seated) and generate or regenerate concept art on that guide. Mirkwood concept r2 showed a box about half the real height, so every faithful model of it read too tall or stretched.

## Resolve how color will be made

Before treating concept color as a requirement, settle how it will be produced: a single-color print that is hand painted, multi-color or multi-material printing, separate colored parts, real illumination or translucency, or presentation only. Use the answer the brief or user already gave; otherwise ask once and record it. The Middle-earth boxes are single-color prints, hand painted.

For hand-painted work, every paint transition needs a physical boundary in the printed geometry: raised, recessed, grooved, or a separate part, with brush access. Judge carving on a neutral single-color render of the exported geometry. A painted render shows the finish plan; it cannot stand in for missing relief. Shaders, textures, emission and bloom prove nothing about the print, and rendered light proves nothing about a real lithophane.

## Get the concept art approved

Before the blockout, show David a concept image: their own reference, or generated art when the brief is words only. Do not make concept art in Blender. Reconcile the contents with David's own nouns and quantities first (a dice tray stays a dice tray). Label generated art as a provisional interpretation and list what it invents: style, layout, closure, magnets, electronics, scale.

Get an explicit approval, revision request, or deferral of the image itself, not of a description. A plain "approved" covers the most recent image and its visible properties only. It never approves dimensions, hidden construction, or pictured mechanisms such as magnets, hinges or latches; those stay proposals until designed and tested. Re-ask if the concept, interior or function changes materially.

For a sculpted container (a tree, a figure, a creature), get the whole model approved as one sculpt before splitting it into print parts. The Party Tree box sculpted its trunk, crown and hill separately and fitted them in code; they never read as one tree, and it was shut down on 2026-11-16.

When several approved images disagree (door position, corner treatment, feet), record which image governs each property before modelling.

Create or update a checkpoint containing the active source, accepted decisions, protected geometry and interfaces, open risks, validation performed, physical feedback, superseded artifacts, and next step.

## Work from protected function outward

Fit purchased parts (tea lights, magnets, batteries, boards) with generous clearance, and never design a tolerance so tight that a part must be exactly right to fit (David, 2026-11-16).

1. Define the finished usable interior and the envelopes of contents, lining, hands, tools, connectors, cables, hinges, and moving parts.
2. Establish a dependency map: contents and clearances → structural shell → lid/closure/hinge → internal modules → decoration/electronics → interface tests → production parts.
3. Make a complete, inexpensive blockout. Reserve major focal forms, openings, motion, assembly paths, service access, structure, wiring, and supports before detail.
4. Develop the design as editable systems: shell, mechanisms, inserts, decoration, sculpture, lighting/electronics, and release geometry. Preserve accepted sources and change locally.
5. Choose methods by form: dimension-controlled solids for functional geometry; generated or sculpted meshes converted to height maps for organic relief (bark, roots, figures); authored height maps for architecture, line art and lettering, where exact widths and placement matter (Shire hillside, Moria Doors); exact CSG for anything that mates. Blender, interactive or headless `bpy`, holds the authoritative source model; do not use OpenSCAD or another parametric CAD tool for the container. Scripted primitives and bevel curves cannot produce carved relief; six Mirkwood blockout revisions proved it. Pick a method that can reach the target look before iterating on it. Never hand-build detailed or decorative 3D parts in code (figures, stairs, decks, railings, brackets); generate them with the 3D generator ([image to 3D](../../shared/image-to-3d/image-to-3d.md) (`shared/image-to-3d/image-to-3d.md`) names the engines, how to call them and their prices). Code is for structural and parametric geometry only (David, 2026-11-14).
6. Engineer solid material volumes at final scale. Let the slicer create infill; create voids only when they serve a deliberate function.
7. Build decoration into the real shell and lid rather than adding parts. Carve walls, not upward-facing tops; lid tops stay flat for now. Every added piece (a glued bezel, a skin) needs a reason David accepts. Never use dowels (David, 2026-11-16). Where two printed faces are glued, align them with printed alignment tabs: male 4.0 mm in diameter and 4.0 mm tall, female 4.2 mm in diameter and 4.2 mm deep (hinges, pivots and joints that are not glued need none); see [engineering and validation](references/engineering-and-validation.md), glued joints. Decide print orientation before carving a face: a face printed against the bed comes out flat.

## Retire uncertainty cheaply

For every consequential unknown, ask what smallest test can answer it. Prefer representative coupons or shallow interface assemblies before full-size parts. Test such things as sliding clearance, magnet pockets, hinge motion, connector engagement, panel retention, feature thickness, optical spacing, hardware envelopes, paint allowance, and support removal using the intended material, printer, orientation, and slicer profile. When David says a coupon is not needed for a simple feature, skip it.

Record actual dimensions and outcomes. A successful test locks only the tested interface and conditions; it does not qualify the entire assembly. Physical results outrank unsupported digital confidence.

## Review with David's eye

David's reaction to a matched render is the faithfulness verdict. Put the concept and the current model, rendered from the same view, side by side in one image, and make a new one for every visible revision before it replaces the last. An audit score never overrides that look: Mirkwood blockout r6 passed an AI audit at 85/100 while its renders were plainly far from the concept.

Keep review proportional. `scripts/` holds optional checkers from the earlier gated process (scorecards, production-relief records, delivery-gate state); use them only when a project asks for that rigor. Run the short self-checks in [reviews](references/reviews.md) before long prints and before handing over a print folder. The critic reviews before every gate (see [independent review](../../shared/independent-review/independent-review.md), `shared/independent-review/independent-review.md`). Hashes, manifests and scorecards do not improve geometry; record only what changes decisions.

## Keep claims honest

State plainly what has been checked: rendered, checked digitally (mesh and slicer), coupon-tested, or printed and assembled. A good render, closed mesh, or warning-free slice does not prove fit. Any multi-part functional interface needs a physical test before it is called fit-tested. Use "prototype" for printable files whose physical behavior is untested, "fit-tested" only for the named interfaces that passed a physical test, and do not use the standalone label "print-ready".

## Finish with actual deliverables

Audit the exported files rather than relying only on the source scene: units, scale, orientation, dimensions, manifoldness, components, and unintended intersections or gaps. Inspect the sliced plate for supports and thin features when it matters.

- One numbered print folder holds every part needed to build the object, including unchanged inherited parts (light tray, lithophane, inserts). Each file name carries part number, revision, quantity and print orientation, for example `05-stump-foot-r3-print-x4-roots-down.stl`. Superseded files move to `superseded/`.
- Keep one authoritative print folder. Mark any other copy (a cloud staging folder, an old mount) as not authoritative, or remove it.
- Bump a part's revision for every geometry change once its file has been shown or handed over.
- Supports a part needs go into its 3MF (painted or as a modifier), or into a numbered PRINT-AND-TEST step with a picture. "Paint supports under the ledge" in prose alone gets missed.
- Render the exported files in the assembled pose before release, and check that magnet pockets, seams and pull bays face their mating parts.
- Test a print-in-place mechanism on its own before the full part, and check its clearance through the whole motion.
- Include a PRINT-AND-TEST.md with print order, orientation, supports, hardware, assembly steps, and what is still untested. For a multi-part build, add the pictures that make assembly unambiguous: an exploded view, a sectional stack, numbered steps, front and up markers, and magnet polarity.

## When David delegates decisions

If David hands over their own calls ("make all the decisions", an unattended test):

- Keep a decision log. Mark every call made in David's place PROXY, with the reason, so David can overrule each one.
- Some verdicts stay David's: whether the result looks right against the concept, any compromise to the focal design, and any release or lock. Deliver at prototype status and ask for those.
- Record every skipped test as a guess, with what would prove it wrong, and still put the coupon in the print folder.
- Before handing over, have an independent skeptic (a separate agent given the files, not your conclusions) look for over-claims. In the Moria test the builder graded itself generously until challenged; the skeptic caught a blurred inscription and stale files.

## Release and lock

When David says to cut a version or lock it, save it as a draft through the workshop skill (`workshop/SKILL.md` in this repo), laid out as described in [project records](references/project-records.md): part table with physical status per part and the mesh audit. David promotes it as `vX.Y`. A promoted revision never changes; any geometry change is a new draft.
