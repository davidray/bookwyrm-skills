# Future 3D Design Playbook

Lessons distilled from the Shire Travel Case and Interior v1 work, 2026-10-25, and the decorated Shire and Mirkwood cases, 2026-11-02.

## Central lesson

The project advanced fastest when uncertainty was made explicit and answered with the smallest useful physical test. Most avoidable rework came from an unstated assumption about what was being stored, how a part was used, which surface was the datum, where wires moved, or whether a test print matched final manufacturing conditions.

Future projects should therefore optimize for **early clarity and cheap evidence**, not for producing full-size geometry as soon as possible.

## What worked especially well

### 1. Physical evidence outranked digital confidence

Mesh checks, collision checks, renders, and slicer output caught real problems, but they never replaced a physical fit report. The project improved decisively when the lid/base seam, false-floor panels, connector projection, magnet pockets, folio, dice capacity, miniature retention, and complete interior were physically tested.

**Default rule:** label every result by evidence level: visual, dimensional, exported mesh, sliced, coupon-tested, component-fit-tested, or assembled-use-tested. Never call a model “proven” without naming what was physically proven.

### 2. Small coupons saved full-size reprints

Magnet-pocket arrays, connector-holder revisions, seam rings, switch openings, USB-C captures, lithophane thickness samples, and depth spacers isolated one question at a time. The successful middle magnet pockets and connector Set B are strong examples of inexpensive tests locking high-value interfaces.

**Default rule:** for every expensive or consequential uncertainty, ask: “What is the smallest print that can answer this?” Full-size prints should combine interfaces that are already understood whenever practical.

### 3. Modular architecture protected progress

The Foundation version was frozen while the lid, electronics, artwork, and storage continued evolving. Interior v1 used independent modules and preserved a contiguous future bay, allowing future changes without redesigning the case shell.

**Default rule:** separate stable structure, wear parts, contents-specific inserts, electronics, and decoration. Make later changes local. Reserve expansion space deliberately rather than counting leftover slivers as future capacity.

### 4. A tested-interface memory prevented repeated work

The magnet register preserved pocket diameter, depth, roof thickness, spacing, and application. This allowed known geometry to be reused while still respecting that a miniature-retention result does not automatically qualify a lid-retention load case.

**Default rule:** maintain a reusable interface register containing nominal hardware, printed dimensions, material/process conditions, test result, load path, and limits of reuse.

### 5. Version locks stopped successful geometry from drifting

The Foundation version, V2.0 architecture lock, and Interior v1 lock created authoritative baselines. Superseded attempts remained traceable, while later changes were required to start a successor revision.

**Default rule:** after approval, freeze hashes, authoritative sources, dimensions, and claims. Never silently replace released geometry. Documentation-only corrections may remain in the version; geometry changes require a new revision.

## Where rework came from

### 1. The thing in the photograph was not always the thing being designed

The cardboard box around the dice foam appeared in the photographs but was not intended for storage. A rim-width gauge was designed for a support surface that did not belong in the product.

**Process change:** inventory every visible object as one of:

- required content;
- optional content;
- packaging or staging aid;
- scale reference;
- explicitly excluded object.

Do not create geometry until ambiguous objects are classified.

### 2. Photographs were useful for planning, not final fit

Paper-based image calibration provided workable plan estimates, but height and perspective remained uncertain. Physical foam measurements of 107 × 74 × 20 mm and 22 mm loaded height superseded the photographic estimate.

**Process change:** photographs may establish a roomy blockout. Precision interfaces require calipers or direct measurements. For complex contents, request top, side, and end views with a scale in the same plane as the measured feature.

### 3. Use orientation was not explicit enough

An early lid concept misunderstood which surface became the dice tray when the complete lid was removed and inverted. That was an architectural issue, not a detail error.

**Process change:** before CAD, illustrate every operating state: closed, open, removed, inverted, loaded, serviced, carried, and stored. Show which face is up and where the user's hands act.

### 4. Datums were sometimes named imprecisely

The 11.84 mm connector spacing was initially treated as broad outside-face separation when it actually belonged between mounting faces. Two 3 mm datum plates turned that misunderstanding into a roughly 6 mm assembly error.

**Process change:** every critical dimension must name both endpoints and the coordinate system. Draw the datum surfaces, not just the number. Tolerance stacks should list each contributing thickness and clearance.

### 5. Rigid-body collision checks missed flexible systems

The seam could be collision-free while the centered three-wire lead still bound in real assembly. Cables, adhesive, plugs, strain relief, and hand access have swept volumes, not merely static outlines.

**Process change:** model or reserve service envelopes for wires and hands. Include bend radius, connector insertion path, strain relief, adhesive thickness, and removal motion. Test a real harness or a faithful dummy before final shell printing.

### 6. Narrow bearing features created fragile assembly logic

Raised annular magnet pedestals intruded into the opening and made lid seating depend on small contact points. Broad continuous mating ledges were a better architecture.

**Process change:** locate assemblies with dedicated geometry and carry loads through broad, stable bearing surfaces. Magnet pockets should provide retention, not become accidental structural feet.

### 7. External forces needed a structural path

Directly aligning a USB-C board with the case wall would have transferred plugging force into the electronics. A panel-mounted extension and serviceable cradle provided a better load path.

**Process change:** map user forces—plugging, lifting, pressing, pulling, rolling, carrying—and route them into replaceable structural parts rather than circuit boards, delicate artwork, lenses, or stored objects.

### 8. A test is only valid under its actual print conditions

Incorrect infill invalidated an early lithophane thickness conclusion. Spacer preferences also changed after repeated testing. Some successful historical fit reports omitted printer, filament, orientation, or slicer details.

**Process change:** every test record should capture printer, nozzle, material, layer height, walls, top/bottom layers, infill, support setting, orientation, and relevant environmental or electrical settings. If a condition is wrong, invalidate only the affected conclusion and preserve the unaffected results.

### 9. Assembly communication needed to be treated as a deliverable

The Interior v1 parts fit digitally, but their stacking order was not intuitively obvious. A step-by-step top and side assembly picture made the architecture understandable.

**Process change:** before a multi-part release, provide:

- a labeled lower-layer plan;
- an exploded view;
- a side or sectional stack view;
- numbered assembly steps;
- front/up orientation markers;
- hardware placement and polarity where relevant.

If the arrangement cannot be explained clearly in one page, the assembly or the documentation is not finished.

### 10. Successful test geometry must remain scoped to its application

A 5 × 2 mm magnet pocket that works behind a 0.8 mm roof against a steel miniature washer does not automatically validate side-wall lid magnets. Same hardware does not mean same load, orientation, roof, installation access, or failure consequence.

**Process change:** reuse an interface only when hardware stock, printer/material conditions, insertion direction, surrounding geometry, and load path are materially equivalent. Otherwise reuse it as a starting candidate and retest.

## Lessons from the decorated Shire and Mirkwood cases, 2026-11-02

### 1. The method capped the quality

Six scripted Mirkwood blockouts laid bevel curves and primitives on a plain box and never looked carved, even though an AI audit passed revision 6 at 85/100. One 3D-generator pass, wrapped onto the real shell as a height map, matched the concept.

**Process change:** pick a method that can reach the target look before iterating on it. Judge progress by a side-by-side render the user looks at, not by audit scores.

### 2. Concept art carried the wrong proportions

Mirkwood concept r2 showed a box about half the real height. Every faithful model of it read too tall, or stretched the carving 1.8x.

**Process change:** render a neutral guide of the real envelope and draw or generate concepts on top of it.

### 3. Decoration broke the edges

Panel frames on the Shire base stopped at the plain rounded corners and left square-ended lips. Carved bands on the lid refilled its 6 mm round along the straight sides, so the round survived only at the corners.

**Process change:** check corners and edge rounds as their own pass, along every side.

### 4. Organic parts were too fragile, then too lumpy

Generated root feet looked good but had thin roots that would snap. A hand-built replacement was strong but read as dough. Generated stumps made chunky by rule (thick short roots, drip-filled overhangs, fused stems) passed.

**Process change:** generate the organic form, then enforce strength rules on it; do not trade detail for strength by hand.

### 5. Smoothing destroyed fits

A remesh rounded the Shire foot pegs and flared their sides, and they failed the fit test.

**Process change:** add mating geometry last, as exact solids, after any smoothing.

### 6. The lithophane needed a flat, photoreal, bright source

Flattening lid art painted at an angle stretched Bilbo 1.6x. The local image model drifted to cartoon over three rounds. David's own photoreal image, brightened heavily, gave a test crop and full pane that both looked great.

**Process change:** generate the scene flat at the pane's aspect, escalate to a stronger model or the user's image after two misses, and brighten for backlight.

### 7. Inherited parts hid faults

The V2.1 outer lid STL is stored face-down, and the first carved Shire lid used it unflipped, putting the magnet pockets on top. Separately, the V2.1 tray mounted the lid connector holder 2.92 mm too low for the 11.84 mm mated distance, leaving a 2 mm gap on the connector side.

**Process change:** check the orientation of every inherited file in an assembled render, and write the stack-up for every interface that spans two parts.

### 8. Incomplete print folders cost round trips

David asked several times where the lithophane and the light tray were, because only the changed parts were in the print folder.

**Process change:** one numbered print folder holds every part needed to build the object, with orientation and quantity in each file name.

## Default workflow for future projects

### Gate 1 — Brief and use states

- Define purpose, intended user, environment, hazards, and definition of done.
- Identify all operating states and orientations.
- Record user forces, access paths, service actions, and likely misuse.
- Separate requirements from ideas and provisional assumptions.

**Output:** one-page brief plus use-state sketch.

### Gate 2 — Inventory and measurement

- Classify every photographed object.
- Measure protected contents and actual hardware directly.
- Record hard envelopes and soft allowances separately.
- Include lining, adhesive, connectors, wire bends, fingers, and removal paths.
- Mark each dimension as measured, manufacturer-specified, photograph-estimated, or assumed.

**Output:** measurement table with source and uncertainty.

### Gate 3 — Architecture concept

- Present the visible concept and functional arrangement before detailed CAD.
- Show closed, open, exploded, and service views as applicable.
- Identify stable foundation geometry and replaceable modules.
- Reserve expansion and service volume.
- Obtain explicit approval of the picture, not merely the prose.

**Output:** approved concept sheet and protected-feature list.

### Gate 4 — Dimensional blockout

- Build the complete assembly at final scale with named datums.
- Establish a single coordinate system and assembly origins.
- Include hardware, keep-outs, cable/hand envelopes, and motion paths.
- Check assembled—not exploded—positions.
- Review the dependency order before adding detail.

**Output:** editable blockout, dimension report, keep-out report, and assembled section.

### Gate 5 — Risk-retirement prints

- Rank unknowns by cost and failure consequence.
- Print coupon arrays for clearances rather than guessing one value.
- Test actual hardware stock.
- Declare pass/fail criteria before printing.
- Change only one important variable per test when possible.

**Output:** test record and interface-memory update.

### Gate 6 — Detailed modeling

- Preserve accepted geometry and edit locally.
- Prefer broad load paths, accessible fasteners, replaceable service parts, and support-free orientation.
- Avoid making stored objects or magnets carry unintended structural loads.
- Maintain an element register so every part has a purpose, dependency, interface, and status.

**Output:** authoritative editable source.

### Gate 7 — Digital print audit

- Audit exported files, not only the source scene.
- Verify units, bounds, orientation, closed volume, winding, degeneracy, components, and intersections.
- Slice the complete set with the intended machine/profile.
- Visually inspect critical layers, bridges, thin roofs, magnet pockets, and support removal.
- Treat G-code as disposable machine output unless needed for a specific investigation.

**Output:** mesh report, slicer review, and plate plan.

### Gate 8 — Assembly communication

- Create the assembly picture before the user starts the full print.
- Include a parts list, quantities, hardware, magnet polarity, liners, adhesives, and tool access.
- Show how each module is removed and serviced.

**Output:** one-page assembly guide plus exploded/section views.

### Gate 9 — Physical validation

- Record the exact print conditions.
- Test fit, removal, access, intended load, service, and ordinary handling separately.
- Photograph the assembled result when practical.
- Record rattling, rubbing, excessive force, trapped objects, high points, and wear risks.
- State what was not tested.

**Output:** physical test record and scoped evidence level.

### Gate 10 — Release and archive

- Freeze the authoritative source and exports.
- Provide checksums, version rule, assembly guide, validation limits, and release claim.
- Keep one obvious release package.
- Archive photographs, measurements, concepts, coupons, superseded geometry, and meaningful result records.
- Remove generated G-code, duplicate unpacked bundles, operating-system metadata, and obsolete backups only after archive and release verification.

**Output:** versioned release, integrity record, checkpoint, and development archive.

## Standard physical-test report

Future fit feedback should capture this compact set:

1. Part and revision.
2. Printer, nozzle, filament, layer height, orientation, walls, infill, supports, and scale.
3. Hardware batch or measured actual dimensions.
4. What was loaded or assembled.
5. Fit: loose, free, snug, press fit, or failed.
6. Removal and hand access.
7. Rubbing, rattling, binding, deformation, or trapped wires.
8. Intended-use check performed and number of cycles.
9. Photographs or measurements retained.
10. Decision: lock, revise, reject, or inconclusive.
11. Exact scope of what the result proves.

## Permanent default rules

1. Measure the real thing before finalizing a precision interface.
2. Classify every visible object before treating it as a requirement.
3. Draw every use orientation and service state.
4. Name the endpoints of every critical dimension.
5. Reserve swept volumes for wires, connectors, tools, and hands.
6. Use small coupons to answer expensive questions.
7. Record manufacturing conditions with every physical result.
8. Store successful interfaces with their application and limits.
9. Create assembly visuals before full printing.
10. Freeze successful versions; make geometry changes in successor revisions.
11. Preserve evidence, but keep only one obvious active release.
12. Claim only what the evidence actually demonstrates.
13. Check concept proportions against the real envelope before modeling from it.
14. Choose a method that can reach the target look; do not iterate a method that cannot.
15. Frames, bands and beads wrap corners; relief never fills an edge round.
16. Protruding ornament is chunky and fused, or a separate glued part.
17. Mating features are exact solids added after any smoothing.
18. Lithophanes come from flat, bright, proportion-checked images, tested as a crop first.
19. Write and check the stack-up for every interface that spans two parts, inherited parts included.
20. Ship one numbered print folder with every part, orientation in each file name.

## What remains specific to the Shire Travel Case

The exact magnet pockets, connector datum, seam clearances, optical depths, storage dimensions, artwork range, and case envelope remain project-specific. They are valuable precedents, not universal printer tolerances. Future projects should reuse the method—measure, coupon, record, and scope—not blindly copy the numbers.

The reusable numbers for this box family (magnets, Gridfinity, pane, case, connectors, fonts) are kept in `skills/printable-container/references/box-family-standards.md`.
