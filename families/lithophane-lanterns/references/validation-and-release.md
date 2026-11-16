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

When parts are combined into one print, check that the result is exactly one body with no closed voids inside. Parts that are glued into grooves at full size end up separate, floating bodies after a union unless they are swelled by about the groove clearance so they fuse. The Christmas village mini had 12 floating icicle strips and 26 hidden voids in its roof. When a hollow is filled, compare the new outer surface with the original, and reject any new flat plane. In the mini, a fill box taller than the roof poked through the hips, and plain clay renders hid it. Take every number a README claims (wall thickness, size, volume) from the check files rather than retyping it. The mini's README said walls were at least 1.2 mm where its own check had measured 0.9 mm.

Slice every production part with the intended machine and profile. Inspect first layers, thin walls, small features, bridges, overhangs, supports, seams, panel relief reproduction, total plate fit, and whether support removal can damage visible or optical surfaces. A successful slicer return code alone is not a review. Look for floating islands and parts that start above the bed; a zero-clash assembly can still contain a part that cannot print (Lake-town: divider blades started 3 mm above the bed). Project supports from the G-code onto the part to see where they touch carved or visible surfaces. "On build plate only" cannot keep supports out of a cavity that is open to the bed, because the cavity floor is the bed. Before slicing, check the mesh for faces inside such a cavity that point down more steeply than 45° (normal z < −0.71). In the mini, tree supports grew up the cavity to the window-pocket ledges. See [tooling](tooling.md) for slicing from the command line.

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

## Release versions

A version reaches The Hoard as a draft change set (see the workshop skill), which the user promotes. The lantern-art folder on the user's Mac is not a git repository, and new meshes no longer go in bookwyrm-lanterns.

```text
inbox/<lantern>/<change set>/
  README.md
  piece.json  the README's facts for the library (version and status are set at promotion)
  print/    one 3MF per part, named <lantern>_<part>.3mf (blank hardware plate included)
  art/      the approved concept and panel art
  review/   the sheets the user approved
```

Every script that generates the parts and panels, in run order, is committed under `lanterns/<lantern>/` in bookwyrm-lanterns, and `piece.json` `source.commit` names that commit.

The README covers: what the lantern is; what the user approved and when; a per-part table (file, part, size, orientation, supports, material); the panel face map; lighting and hardware (strip, pixels per face, WLED limit, plate); the source pipeline in run order, with tool versions and the source commit; where large source meshes live and their generation task IDs; and known open items, including what has not been printed.

Before saving, check every claim in the README (shell counts, supports, coverage, sizes) against the facts files and slice results it summarises. A README once said every part was a single shell while the body's facts listed 5. Also check that every script takes its paths as arguments, that every 3MF re-imports with the expected bounds and shell count, and that no placeholder or reserve geometry is in a print file. Write `piece.json` with the README: every print file is named by a component, and Middle-earth and Zelda lanterns are `"ip"` `middle-earth` or `zelda` with licence `personal-use-only`. Tell the user the claim level the README states, to use as the status at promotion. A later change is a new draft; a promoted revision is never edited.

In an autonomous run, save the candidate as a draft as soon as it is complete so the user can review it in The Hoard, say in the README and the draft's note that it was not user-approved, and never promote it. Put these at the top of the README and the message to the user:
- any reviewer FAIL that is still unresolved;
- any departure from a standard architecture or series interface;
- every measured loss the reviewer reported, such as simulated sharpness or tonal loss on panels, or detail lost in engineering.
