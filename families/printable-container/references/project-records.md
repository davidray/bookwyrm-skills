# Project records

Use these compact records to make long builds restartable and auditable. Adapt them to the project's scale; do not create paperwork that does not change decisions.

## Initial design record

- Purpose and intended use
- Definition of done and project-specific acceptance criteria
- Authoritative references and the property each governs
- Explicit user requirements
- Exact contents list in David's own words and quantities
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

Finished work ends in a versioned release, saved as a draft change set through the workshop skill and promoted by David. Use the same layout for every box and board:

1. A change set for `<box>` holding numbered parts whose file names carry part, revision, quantity and print orientation. Editable sources worth keeping go under `source/`; superseded files stay out.
2. `README.md` with a part table giving each part's physical status (printed, fit-tested, approved for looks, not reported), hardware, assembly steps, digital checks done, what is not yet tested, and what the release doesn't claim. bookwyrm-boxes `projects/mirkwood-travel-case/release-v1.0/README.md` is the model.
3. A mesh audit (bounds, closed, components) in the README. The store records every file's SHA-256, so no checksum file is needed.
4. `piece.json` for the library (bookwyrm-rpg `services/library/docs/piece-json.md`): `kind` is `container`, every print file is named by a component, Middle-earth or Zelda boxes are `personal-use-only`, and `source.commit` names the bookwyrm-boxes commit holding the generating scripts. Version and status are set at promotion.
5. Submit it with `submit_change_set` and tell David what the draft is. When David promotes it, record who promoted it, when, and their words in the project checkpoint. Documentation fixes keep the version; any change to a mesh, size, clearance, pocket or assembly position is a new draft and promotes as vX.Y+1. A promotion freezes the design; it adds no test evidence.
6. Meshes no longer go in Git LFS. `release-vX.Y/` folders already in bookwyrm-boxes stay as they are.

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
