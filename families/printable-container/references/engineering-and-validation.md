# Engineering and validation

Read this before detailed mechanical design, segmentation, electronics integration, print preparation, or release.

## Functional architecture

Protect the finished usable interior after accounting for lining, paint, fasteners, locators, hinges, wiring, and any false floor. Size compartments around actual contents and include finger access rather than only nominal object envelopes.

Design the complete lifecycle as geometry:

- printing orientation and support access;
- assembly sequence and insertion paths;
- hinge sweep, lid stop, and closure alignment;
- tool, finger, connector, and unplug travel;
- wire path and bend radius;
- battery safety and removal;
- paint and glue access;
- resin drainage, washing, and curing access;
- maintenance, replacement, and disassembly.

A collision-free final pose does not prove an assembly or service path.

Before detailed modeling, show every applicable operating state: closed, open, removed, inverted, loaded, serviced, carried, and stored. Mark which face is up, where hands and tools act, what moves, and what must stay reachable. A misunderstood use orientation is an architecture error, not a detail to repair later.

Define a coordinate system and named datum surfaces for critical interfaces. Every critical dimension names both endpoints, and every tolerance stack lists the contributing thicknesses, clearances, finish or adhesive allowances, and measurement uncertainty. Do not let a dimension silently change from mounting-face spacing to outside-face spacing.

For a heavy or highly decorated lid, evaluate center of mass, open-lid tipping, hinge torque, hinge and fastener loads, lid-stop loads, opening stability, and repeated-cycle wear. Do not treat a hinge that merely fits as load-qualified.

## Structure and decoration

Provide explicit load paths through structural walls, cores, ribs, ledges, bosses, rails, backing, and broad attachment roots. Do not rely on incidental overlap or decorative contact. Keep brittle ornament, inscriptions, foliage, thin membranes, and panel edges out of primary handling loads unless deliberately reinforced.

Locate assemblies with dedicated geometry and carry loads through broad, stable bearing surfaces. Magnets retain; they should not become accidental feet or narrow seating datums. Route user forces (plugging, lifting, pressing, pulling, carrying) into structural or replaceable parts, not circuit boards, lenses, artwork, or stored objects.

Prefer reversible adjustment where it reduces reprints: shims, removable retainers, service panels, replaceable mounts, separate inserts, and independently printable ornaments. Protect glue lands and mating surfaces from finish buildup.

Model parts as solid material volumes and let the slicer determine infill. Retain only intentional voids such as sockets, wire channels, light chambers, drainage paths, and service bays. Hollowing a model for FDM adds a second set of walls and an unsupported roof, so it often uses more plastic; save filament with Lightning infill and fewer walls instead (see [moving parts and figures](moving-parts-and-figures.md)).

### Production relief and paint access

Classify decorative objects as production or presentation. Only production geometry that survives the export counts as printable relief; helpers, shaders, textures and compositor effects do not. Check carving on neutral single-color renders of the exported part, with a grazing-light or close-up view for shallow detail.

For each intended paint transition on a hand-painted part, know its boundary type (raised, recessed, grooved, or separate part), its depth and width, and whether a brush and masking can reach it. There is no universal paint-boundary size; judge it against the process, primer and paint allowance, and technique. `scripts/validate_production_relief_evidence.py` can check a full evidence record when a project wants that rigor.

## Process allocation

Select process and material per function. FDM often suits shells and load-bearing structure; resin may suit compact high-detail ornament. This is a decision criterion, not a fixed allocation. Evaluate final scale, nozzle or pixel size, layer direction, anisotropy, brittleness, heat, optical behavior, painting, post-processing, support damage, and actual supported build envelope.

Print orientation is part of the design. Consider bed contact, bridging, overhangs, tall-part wobble, support scars, support removal, seam location, strength direction, and accessible finished surfaces before finalizing geometry.

## Energy, lighting, and electronics safety

For LED scenes, WLED and circuit-board lessons, see [lighting and electronics](../../../shared/lighting-and-electronics/lighting-and-electronics.md).

Classify the intended source before designing around it: unpowered, low-voltage battery/LED, externally powered low-voltage, mains-powered, heat-producing lamp, or open flame. Ordinary printed-plastic lanterns should default to LED-only. Hold mains, open-flame, high-energy battery, or other safety-critical designs unless appropriate domain requirements and evidence are provided.

For low-voltage electronics, record as relevant:

- voltage, worst-case current and power budget;
- battery chemistry, protection, charging method, and safe removal;
- wire gauge, insulation, polarity/keying, strain relief, and short protection;
- component and connector ratings;
- worst-case heat sources, ventilation, material temperature limits, and a defined thermal test;
- switch, USB, connector, and fuse access;
- magnet polarity, retention, and possible interference with electronics;
- failure state and safe shutdown.

An electrical configuration read-back or illuminated render does not verify temperature, wiring quality, power integrity, optical uniformity, light transmission, diffusion, leakage, or safe use. Emission and bloom are presentation only. Record the physical light path and test conditions, and hold optical, electrical or thermal claims whose physical evidence is missing.

## Glued joints: printed male/female tabs

Every glued joint uses printed alignment tabs, never dowels or filament pins: see [glued joints](../../../shared/joints-and-assembly/glued-joints.md) for the standard 4.0/4.2 mm tab, the starting sizes, keying and print orientation. The family's glued feet are the printed example: a teardrop tab (tip toward the corner) on each foot, its socket in the shell, a 1.3 mm tab in a 1.5 mm socket with 0.2 mm all round. Keep mating features exact after any relief smoothing (see [decorative relief](decorative-relief.md)).

Box exceptions (say which applies, and why, in the box's README):
- Not glued: lift-off and magnetic lids, light trays, drop-in and basement panels, Gridfinity bins, screws and inserts, anything taken apart for service.
- Moving joints: hinges, pivots and axles (the treasure chest's 1.75 mm filament hinge pin is a fine axle). See [moving parts and figures](moving-parts-and-figures.md).
- A shaped seat that already locates the part (the Gollum box's sphere socket, a cradle).

## Interface experiments

Treat tolerances as interface- and process-specific. Start with explicit provisional values, then test the intended printer, material, orientation, and profile. Useful experiments include:

- stepped sliding or press-fit coupons;
- magnet-pocket arrays;
- peg/socket or tongue/groove sections;
- representative thin relief and lettering;
- hinge and closure sections;
- connector holder, engagement, and cable-access gauges;
- optical thickness and LED-spacing samples;
- shallow full-footprint seam assemblies when overall alignment matters.

Lock the successful dimensions and conditions in the checkpoint. Do not generalize a result to a different feature, orientation, material, or printer without evidence. Where practical, make the final design adjustable rather than relying on one nominal dimension.

Before printing, define pass/fail criteria, measurement method and reasonable uncertainty, number of repetitions or cycles when wear matters, and what result triggers a revision. A single successful insertion may establish basic fit but does not automatically establish retention, durability, or safe repeated use.

## Stack-ups across separable parts

When an interface spans two printed parts, such as mated connectors between lid and base, write the stack-up before release: each mounting face's height from the seam, each part thickness, and the required mated distance. Then check it in the assembled pose with a section. The Shire lid sat about 2 mm high on the connector side because the base holder face was 8.92 mm below the seam, the V2.1 tray put the lid holder at the seam, and the mated Set B pair needs 11.84 mm. The tray was 2.92 mm short; tray r3 added a 2.92 mm pocket. Inherited parts are not exempt: this fault predated the carved shell.

## Source orientation

Before decorating or re-exporting an inherited part, confirm which way its file is stored. The V2.1 outer lid STL is stored face-down for printing; used unflipped, the carved Shire lid r1 had its magnet pockets on top. Check landmarks (magnet pockets face the mating part, pull bays at the seam, rounded edge on the visible top) in an assembled render.

## Shared tools and files

Several threads can drive the same Blender app. Before generating or saving, check which file is open and whether it has unsaved changes (`bpy.data.is_dirty`). Keep each project's objects in its own file, and never save or close a file another job opened.

## Evidence and validation

Keep these distinct:

- **Visual:** appearance and concept fidelity.
- **Dimensional:** measured envelopes, protected space, contacts, clearances, and motion.
- **Topology:** finite coordinates, winding, manifoldness, degeneracy, components, and intersections.
- **Manufacturing:** minimum walls/features, load paths, segmentation, orientation, supports, and complete layer preview.
- **Physical:** printed fit, strength, stability, assembly, service, lighting, and use.
- **Release:** authoritative deliverables, instructions, provenance, and accurate claims.

For exported STLs, check as relevant:

- millimetre units and intended scale;
- expected bounds and print orientation;
- finite coordinates, positive face areas, consistent winding, and positive volume;
- zero unintended boundary, overused, or non-manifold edges;
- expected connected components;
- no unintended duplicate triangles, intersections, gaps, or tiny fragments;
- round-trip import matching the export;
- equality or documented change relative to protected source geometry.

When the user reports a print result, ask for the printer, filament and main slicer settings if they weren't given, so the release can record them. For physical print evidence, record the printer, nozzle, material, scale, layer height, walls, top and bottom layers, infill, supports, and orientation. When a condition was wrong, invalidate only the conclusions that depend on it.

Then inspect the selected slicer's actual layer and support result. Record machine, nozzle/process, material profile, layer settings, orientation, supports, warnings, and whether the review was CLI-only or visually inspected. A warning-free slice is not a physical test.

## Release threshold

Do not use the ambiguous standalone label “print-ready.” Describe evidence as `SKILL.md` does, and do not use “fit-tested” or equivalent wording more broadly than the evidence. A multi-part functional design without a complete physical assembly test remains a prototype, or fit-tested only for the named interfaces that passed. A release should identify:

- authoritative source and version;
- printable files, quantity, units, and orientation;
- printer/process and material assumptions;
- hardware and assembly order;
- validated interfaces and exact test conditions;
- remaining untested behavior and safety constraints;
- accepted compromises;
- checksums or a reproducible package when appropriate.

