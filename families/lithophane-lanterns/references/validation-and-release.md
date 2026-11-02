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

Slice every production part with the intended machine and profile. Inspect first layers, thin walls, small features, bridges, overhangs, supports, seams, panel relief reproduction, total plate fit, and whether support removal can damage visible or optical surfaces. A successful slicer return code alone is not a review.

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
