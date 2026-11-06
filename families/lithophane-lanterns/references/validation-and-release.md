# Validation and release

## Evidence ladder

State the highest level actually reached:

1. visual review;
2. source-model dimensional and geometry audit;
3. exported-mesh and round-trip audit;
4. slicer, support, and layer review;
5. representative physical coupon;
6. full component fit and optical test;
7. complete assembly and intended-use test;
8. qualified assembled release.

Evidence at one level does not imply the next.

## Digital checks

For each exported part, verify units, scale, bounds, orientation, triangle/face health, manifoldness as appropriate, normals/winding, positive volume, disconnected components, unintended gaps or intersections, and round-trip import. Check that presentation-only objects and service reserves are absent.

Audit round-trips with the indexing the slicer reads. Merging vertices by position can re-join a boolean library's deliberately split pinch points and report a sound body as many shells (Lake-town: 96 shells from a watertight manifold3d result); write 3MFs from the solver's own indexing and audit that. Watch for inside-out output (negative volume) from marching cubes and zero-volume slivers from booleans.

Slice every production part with the intended machine and profile. Inspect first layers, thin walls, small features, bridges, overhangs, supports, seams, panel relief reproduction, total plate fit, and whether support removal can damage visible or optical surfaces. A successful slicer return code alone is not a review. Look for floating islands and parts that start above the bed; a zero-clash assembly can still contain a part that cannot print (Lake-town: divider blades started 3 mm above the bed). Project supports from the G-code onto the part to see where they touch carved or visible surfaces. See [tooling](tooling.md) for slicing from the command line.

## Physical tests

Record each coupon as a named interface under named conditions. Useful acceptance language is concrete: slides without force, remains retained under inversion, switch is reachable, no visible hotspot at normal viewing distance, or panel remains legible. Avoid turning “snug” or “pass” into claims about untested retention, optics, heat, or the full assembly.

After component coupons, perform an assembled check of panel installation, hardware installation, service access, roof/base retention, all-face illumination, stability, and intended handling. If this is not done, release as a prototype with the limitations stated.

## Claim levels

- **Visual concept:** appearance only.
- **Digitally validated candidate:** current exports and slices were checked; no physical-fit claim.
- **Prototype release:** printable files supplied for evaluation with unresolved physical behavior stated.
- **Interface-fit-tested release:** named critical interfaces passed representative tests under recorded conditions; whole-lantern behavior may remain unqualified.
- **Qualified assembled release:** the complete assembly and intended-use acceptance criteria passed, including critical mechanical, optical, service, and safety-relevant interfaces.

Do not use “print-ready” without a qualifier because readers interpret it as stronger than digital validation.

## Release package

Include:

- authoritative editable source and exact production exports;
- face-labeled lithophane files and installation map;
- quantities, units, and finished dimensions;
- printer/material/profile assumptions and part orientation;
- support and post-processing guidance;
- assembly, panel installation, and light-service order;
- hardware/BOM and safety boundary;
- validation record, physical-test conditions, and known failures;
- tested versus untested interfaces and assigned claim level;
- version identity and superseded-file warning.

Do not release stale candidate STLs after a later visual, hardware, scale, or interface revision.

## Locked versions

When the user approves a version for printing, lock it by pull request in this repository (the lantern-art folder on the user's Mac is not a git repository):

```text
lanterns/<lantern>/v<N>/
  README.md
  print/    one 3MF per part, named <lantern>-v<N>_<part>.3mf (blank hardware plate included)
  source/   every script that generates the parts and panels, in run order
  art/      the approved concept and panel art
  review/   the sheets the user approved
```

The README covers: what the lantern is; what the user approved and when; a per-part table (file, part, size, orientation, supports, material); the panel face map; lighting and hardware (strip, pixels per face, WLED limit, plate); the source pipeline in run order, with tool versions; where large source meshes live and their generation task IDs; and known open items, including what has not been printed.

Before locking, check that every script takes its paths as arguments, that every 3MF re-imports with the expected bounds and shell count, and that no placeholder or reserve geometry is in a print file. A later change is a new `v<N+1>` folder; never edit a locked version in place.

In an autonomous run, open the locking PR as soon as the candidate is complete so the user can review it, say in the README and PR that the version was not user-approved, and leave it unmerged until the user's verdict.
