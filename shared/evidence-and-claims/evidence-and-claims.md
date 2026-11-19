# Evidence and claims

What a check proves, what it doesn't, and which status a product may carry in The Hoard. The same for every family; each family's own release reference adds what its products must include.

## The evidence ladder

State the highest level actually reached. Evidence at one level does not imply the next.

1. Visual review.
2. Source-model dimensional and geometry audit.
3. Exported-mesh and round-trip audit.
4. Slicer, support and layer review.
5. Representative physical coupon.
6. Full component fit (and optical test, for lit products).
7. Complete assembly and intended-use test.
8. Qualified assembled release.

Keep the kinds of evidence apart:

- **Visual:** silhouette, anatomy, placement, story and concept fidelity.
- **Dimensional:** measured envelopes, protected space, contacts, clearances and motion.
- **Topology:** finite coordinates, winding, manifoldness, degeneracy, components and intersections, stating exactly what was checked.
- **Manufacturing:** minimum walls and features, load paths, joints, segmentation, orientation, supports and the full layer preview.
- **Physical:** printed fit, strength, stability, assembly, service, lighting and use.
- **Release:** authoritative files, instructions, provenance and accurate claims.

A closed mesh, one connected component, a successful export or a model that fits the build volume does not establish the later claims. Sampled distances are not exact clearance bounds. A warning-free slice is not a physical test.

## Status in The Hoard

The `status` given at promotion (see the workshop skill) is the claim:

| Status | Means |
| --- | --- |
| `concept` | Appearance only. |
| `digitally-validated` | The current exports and slices were checked; no physical-fit claim. A render or a slice is never more than this. |
| `prototype` | Printed, but not yet production in David's view, with unresolved physical behaviour stated. Files that have not been printed are never more than `digitally-validated` (David, 2026-11-19). |
| `interface-fit-tested` | Named critical interfaces passed representative tests under recorded conditions; the whole product may remain unqualified. |
| `qualified` | The complete assembly and intended-use acceptance criteria passed, including mechanical, optical, service and safety-relevant interfaces. |

Never write "print-ready" without a qualifier: readers take it as stronger than digital validation. Don't use "fit-tested" more broadly than the interfaces that passed. A printed multi-part functional design without a complete physical assembly test stays a prototype, or fit-tested only for the named interfaces.

## Digital checks

For each exported part, check as relevant:

- millimetre units, intended scale, expected bounds and print orientation;
- finite coordinates, positive face areas, consistent winding and positive volume;
- no unintended boundary, overused or non-manifold edges;
- the expected connected components, and no unintended duplicate triangles, intersections, gaps or tiny fragments;
- a round-trip import that matches the export;
- equality with, or a documented change from, protected source geometry;
- that presentation-only objects and service reserves are absent.

Lessons that cost reprints:

- **Audit with the indexing the slicer reads.** Merging vertices by position can re-join a boolean library's deliberately split pinch points and report a sound body as many shells (Lake-town lantern: 96 shells from a watertight manifold3d result). Write 3MFs from the solver's own indexing and audit that. Watch for inside-out output (negative volume) from marching cubes and zero-volume slivers from booleans.
- **Combined prints must be one body with no closed voids.** Parts glued into grooves at full size end up as separate floating bodies after a union unless they are swelled by about the groove clearance (the Christmas village mini had 12 floating icicle strips and 26 hidden voids in its roof). When a hollow is filled, compare the new outer surface with the original and reject any new flat plane.
- **Take every number a README claims from the check files**, never retype it. The mini's README said walls were at least 1.2 mm where its own check measured 0.9 mm.

## Slicer review

Slice every production part with the intended machine and profile, and inspect the actual layers and supports: first layers, thin walls, small features, bridges, overhangs, seams, relief reproduction, plate fit, and whether support removal can damage visible surfaces. Record machine, nozzle and process, material profile, layer settings, orientation, supports, warnings, and whether the review was command-line only or visually inspected.

- A successful return code alone is not a review. Look for floating islands and parts that start above the bed; a zero-clash assembly can still hold a part that can't print (Lake-town's divider blades started 3 mm above the bed).
- Project supports from the G-code onto the part to see where they touch carved or visible surfaces.
- "On build plate only" can't keep supports out of a cavity open to the bed, because the cavity floor is the bed. Before slicing, check for faces in such a cavity pointing down more steeply than 45° (normal z < −0.71).

## Physical tests

Record each coupon as a named interface under named conditions: printer, nozzle, material, scale, layer height, walls, top and bottom layers, infill, supports and orientation. When David reports a print result without these, ask for them. When a condition was wrong, invalidate only the conclusions that depend on it.

Use concrete acceptance language: slides without force, stays retained when inverted, switch is reachable, no visible hotspot at normal viewing distance, panel remains legible. Don't turn "snug" or "pass" into claims about untested retention, optics, heat or the whole assembly. Use representative test pieces for uncertain joints and thin features before committing a large print.

After component coupons, check the assembled product: installation of panels and hardware, service access, retention, lighting, stability and intended handling. If that isn't done, it ships as a prototype with the limits stated.

## Evidence freshness

Bind important review packets to the current source and export identities, using hashes when the workflow warrants it. Geometry edits invalidate evidence that depicts or measures the old geometry. Evidence-only rerenders may keep the geometry identity but should still be versioned and declared as such. An attractive lit render and a neutral geometry packet answer different questions; keep both. A user's visual approval applies only to the revision and the visible properties shown.

## What every release states

- the authoritative source and version, and the exact production files;
- quantities, units, finished dimensions and print orientation;
- printer, process and material assumptions, and support and post-processing guidance;
- hardware, assembly and service order, and the safety boundary;
- the validation record with test conditions and known failures;
- tested versus untested interfaces, and the status claimed;
- accepted compromises;
- a warning against older, superseded files.

The store records every file's hash, so a release saved through workshop needs no separate checksum file.
