# Project records

Use these compact records to make long builds restartable and auditable. Adapt them to the project's scale; do not create paperwork that does not change decisions.

## Initial design record

- Purpose and intended use
- Definition of done and project-specific acceptance criteria
- Authoritative references and the property each governs
- Explicit user requirements
- Exact contents list in the user's own words and quantities
- Photographed-object inventory: required content, optional content, packaging, scale reference, or excluded
- Operating states and orientations: which face is up, what moves, where hands act
- Measurement source for each critical dimension: measured, manufacturer, photo estimate, or assumption
- Coordinate system and named datums for critical interfaces
- How color will be made: single-color hand-painted, multi-color, separate parts, illumination, or presentation only
- Concept-art decision: image and revision, approved visible properties, open assumptions
- Protected usable interior
- Contents and measured envelopes
- Available printers, processes, materials, and known profiles
- External planning envelope
- Visual identity: focal point, principal views, silhouette, motifs, materials, story
- Functional systems: closure, hinges, inserts, electronics, lighting, service
- Intended energy/light source and applicable safety boundary
- Element register: element, role, method, dependencies, interfaces, status
- Dependency order
- Provisional assumptions and measurements still needed
- Highest-risk uncertainties and proposed smallest tests

## Current checkpoint

- Date and current stage
- Active editable source and authoritative exports
- Active design attempt and excluded/superseded sources
- Accepted visual decisions
- Accepted physical interface dimensions and test conditions
- Protected objects, geometry, transforms, and interfaces
- Interface memory: hardware, measured stock, printed dimensions, process conditions, load path, result, and limits of reuse
- Changes in this revision
- Validation run now and its exact limits
- Physical feedback received
- Compromise register changes
- Review findings and dispositions
- Open risks, held artifacts, and next step

## Test record

- Question being tested
- Predeclared pass/fail criteria
- Part or coupon version
- Governing dimensions
- Printer, nozzle, material, scale, layer height, walls, infill, supports, orientation, and slicer profile
- Hardware batch or measured actual dimensions
- Assembly or measurement procedure
- Measurement method, reasonable uncertainty, and repetition/cycle count
- Fit: loose, free, snug, press fit, or failed; removal and hand access; rubbing, rattling or binding
- Result and observation
- Photographs or measurements retained
- Decision: lock, revise, reject, or inconclusive
- Scope of the conclusion
- Geometry and artifacts superseded by the result

## Compromise record

- Governing concept property
- Modeled departure
- Classification
- Reason and supporting evidence
- Visible effect and affected views
- Alternatives and tradeoffs
- Builder recommendation
- User decision
- Required follow-up review or test

## Release and lock

Finished work ends in a versioned release. Use the same layout for every box and board:

1. Folder `projects/<box>/release-vX.Y/` (or `shared/<area>/<part>/release-vX.Y/`), with numbered parts whose file names carry part, revision, quantity and print orientation. Editable sources and superseded files stay outside it.
2. `README.md` with a part table giving each part's physical status (printed, fit-tested, approved for looks, not reported), hardware, assembly steps, digital checks done, what is not yet tested, and what the release doesn't claim. `projects/mirkwood-travel-case/release-v1.0/README.md` is the model.
3. `LOCK.md` recording who locked it, when, and their words. Documentation fixes keep the version; any change to a mesh, size, clearance, pocket or assembly position starts vX.Y+1.
4. `SHA256SUMS.txt` and a mesh audit (bounds, closed, components). Make the folder read-only on the Mac.
   Add `piece.json` for the library (bookwyrm-rpg `services/library/docs/piece-json.md`): `version` is `vX.Y`, `kind` is `container`, every print file is named by a component, and Middle-earth or Zelda boxes are `personal-use-only`. `python tools/check_piece_json.py projects/ shared/` must be clean. The publish-to-the-hoard skill (bookwyrm-rpg `services/library/skills/publish-to-the-hoard/SKILL.md`) covers this step and what follows the merge: The Hoard imports the version, nobody runs `import_piece` from a build project.
5. Commit on a branch and open a pull request; never push to main without the user's say-so. A lock freezes the design; it adds no test evidence.
6. Git LFS has limited space, so only release meshes go in it, stored as 3MF where the STL is large (Mirkwood went from 244 to 65 MB). Check each 3MF against its STL for triangle count, bounds and area. The cloud container can't reach lfs.github.com, so mesh uploads go from the Mac clone (`~/code/bookwyrm-boxes`); give the user the command block.

## Release record

- Version and authoritative source
- Included files and quantities
- Units, scale, and provided orientation
- Process/material assumptions
- Hardware/BOM and assembly sequence
- Mesh and round-trip audit summary
- Slicer/support review summary
- Physical tests passed and exact conditions
- Remaining untested behavior
- Safety limitations
- Accepted compromises
- Assembly pictures: exploded view, sectional stack, numbered steps, orientation markers, magnet polarity
- What the release does not claim
- One obvious active release folder, with superseded files kept outside it
