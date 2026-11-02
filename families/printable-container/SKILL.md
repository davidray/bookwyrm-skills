---
name: printable-container
description: Design decorative 3D-printable containers from concept art or a brief through dimensional architecture, editable modeling, carved relief, lithophanes, fit tests, printable STL files, and release documentation. Use for boxes, chests, cases, lanterns, enclosures, and similar hollow assemblies; do not use for ordinary standalone miniatures, purely visual renders, or safety-critical pressure, medical, food-contact, mains-voltage, open-flame, or high-energy battery products without domain-specific engineering requirements.
---

# Printable container

Turn a visual idea into a usable, manufacturable container without quietly designing away what made the concept appealing. Treat visual design, protected function, mechanical architecture, manufacturing, physical evidence, and release claims as related but distinct systems.

References:

- [concept and faithfulness](references/concept-and-faithfulness.md): new or substantially changed designs.
- [decorative relief](references/decorative-relief.md): carved exteriors, feet, handles, mating features.
- [lithophanes](references/lithophanes.md): lit panes, scene images, inscriptions and fonts.
- [engineering and validation](references/engineering-and-validation.md): joints, stack-ups, electronics, orientation, exports.
- [box-family standards](references/box-family-standards.md): house dimensions, hardware and defaults.
- [reviews](references/reviews.md): review checklists and when to use an independent reviewer.
- [project records](references/project-records.md): checkpoint, test and release record forms.

## Begin with authority and evidence

Before modeling, identify the authoritative references, explicit user requirements, actual contents and hardware, available printers/processes, intended energy or light source, project-specific definition of done, and which decisions remain provisional. Preserve original references and measurements. Do not infer hidden construction, exact dimensions, materials, electronics, or mechanisms from concept art. Hold open-flame or other safety-critical designs unless suitable domain requirements, materials, clearances, tests, and acceptance criteria are supplied; never imply ordinary printed plastic is flame-safe.

Before using concept art, compare its proportions with the real envelope. Render a neutral guide of the real case (front-left and back-right, lid seated) and generate or regenerate concept art on that guide. Mirkwood concept r2 showed a box about half the real height, so every faithful model of it read too tall or stretched.

## Resolve how color will be made

Before treating concept color as a requirement, settle how it will be produced: a single-color print that is hand painted, multi-color or multi-material printing, separate colored parts, real illumination or translucency, or presentation only. Use the answer the brief or user already gave; otherwise ask once and record it. The Middle-earth boxes are single-color prints, hand painted.

For hand-painted work, every paint transition needs a physical boundary in the printed geometry: raised, recessed, grooved, or a separate part, with brush access. Judge carving on a neutral single-color render of the exported geometry. A painted render shows the finish plan; it cannot stand in for missing relief. Shaders, textures, emission and bloom prove nothing about the print, and rendered light proves nothing about a real lithophane.

## Get the concept art approved

Before the blockout, show the user a concept image: their own reference, or generated art when the brief is words only. Do not make concept art in Blender. Reconcile the contents with the user's own nouns and quantities first (a dice tray stays a dice tray). Label generated art as a provisional interpretation and list what it invents: style, layout, closure, magnets, electronics, scale.

Get an explicit approval, revision request, or deferral of the image itself, not of a description. A plain "approved" covers the most recent image and its visible properties only. It never approves dimensions, hidden construction, or pictured mechanisms such as magnets, hinges or latches; those stay proposals until designed and tested. Re-ask if the concept, interior or function changes materially.

Create or update a checkpoint containing the active source, accepted decisions, protected geometry and interfaces, open risks, validation performed, physical feedback, superseded artifacts, and next step.

## Work from protected function outward

1. Define the finished usable interior and the envelopes of contents, lining, hands, tools, connectors, cables, hinges, and moving parts.
2. Establish a dependency map: contents and clearances → structural shell → lid/closure/hinge → internal modules → decoration/electronics → interface tests → production parts.
3. Make a complete, inexpensive blockout. Reserve major focal forms, openings, motion, assembly paths, service access, structure, wiring, and supports before detail.
4. Develop the design as editable systems: shell, mechanisms, inserts, decoration, sculpture, lighting/electronics, and release geometry. Preserve accepted sources and change locally.
5. Choose methods by form: dimension-controlled solids for functional geometry; generated or sculpted meshes converted to height maps for organic relief; exact CSG for anything that mates. Blender, interactive or headless `bpy`, holds the authoritative source model; do not use OpenSCAD or another parametric CAD tool for the container. Scripted primitives and bevel curves cannot produce carved relief; six Mirkwood blockout revisions proved it. Pick a method that can reach the target look before iterating on it.
6. Engineer solid material volumes at final scale. Let the slicer create infill; create voids only when they serve a deliberate function.
7. Build decoration into the real shell and lid rather than adding parts. Every added piece (a glued bezel, a skin) needs a reason the user accepts. Decide print orientation before carving a face: a face printed against the bed comes out flat.

## Retire uncertainty cheaply

For every consequential unknown, ask what smallest test can answer it. Prefer representative coupons or shallow interface assemblies before full-size parts. Test such things as sliding clearance, magnet pockets, hinge motion, connector engagement, panel retention, feature thickness, optical spacing, hardware envelopes, paint allowance, and support removal using the intended material, printer, orientation, and slicer profile. When the user says a coupon is not needed for a simple feature, skip it.

Record actual dimensions and outcomes. A successful test locks only the tested interface and conditions; it does not qualify the entire assembly. Physical results outrank unsupported digital confidence.

## Review with the user's eye

The user's reaction to a matched render is the faithfulness verdict. Put the concept and the current model, rendered from the same view, side by side in one image. An audit score never overrides that look: Mirkwood blockout r6 passed an AI audit at 85/100 while its renders were plainly far from the concept.

Keep review proportional. `scripts/` holds optional checkers from the earlier gated process (scorecards, production-relief records, delivery-gate state); use them only when a project asks for that rigor. Run the short self-checks in [reviews](references/reviews.md) before long prints and before handing over a print folder. Use an independent reviewer only for a new box architecture, a safety-relevant change, or when the user asks. Hashes, manifests and scorecards do not improve geometry; record only what changes decisions.

## Keep claims honest

State plainly what has been checked: rendered, checked digitally (mesh and slicer), coupon-tested, or printed and assembled. A good render, closed mesh, or warning-free slice does not prove fit. Any multi-part functional interface needs a physical test before it is called fit-tested. Use "prototype" for printable files whose physical behavior is untested, "fit-tested" only for the named interfaces that passed a physical test, and do not use the standalone label "print-ready".

## Finish with actual deliverables

Audit the exported files rather than relying only on the source scene: units, scale, orientation, dimensions, manifoldness, components, and unintended intersections or gaps. Inspect the sliced plate for supports and thin features when it matters.

- One numbered print folder holds every part needed to build the object, including unchanged inherited parts (light tray, lithophane, inserts). Each file name carries part number, revision, quantity and print orientation, for example `05-stump-foot-r3-print-x4-roots-down.stl`. Superseded files move to `superseded/`.
- Render the exported files in the assembled pose before release, and check that magnet pockets, seams and pull bays face their mating parts.
- Include a PRINT-AND-TEST.md with print order, orientation, supports, hardware, assembly steps, and what is still untested. For a multi-part build, add the pictures that make assembly unambiguous: an exploded view, a sectional stack, numbered steps, front and up markers, and magnet polarity.
