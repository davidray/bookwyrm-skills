# Validation and release

The evidence ladder, the statuses, digital and slicer checks, physical tests and evidence freshness are shared by every family: read [evidence and claims](../../../shared/evidence-and-claims/evidence-and-claims.md). This file adds what a lantern release needs.

Lantern-specific checks:

- In the slicer, inspect panel relief reproduction as well as the usual list, and see [tooling](tooling.md) for slicing from the command line.
- After component coupons, the assembled check covers panel installation, roof and base retention and all-face illumination.

## Release package

Include everything the shared list asks for, plus:

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
