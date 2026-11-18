# Working records

Use only the sections needed for the current task. These are lightweight record formats, not additional approval gates. Keep the project checkpoint authoritative; link to detailed audits rather than copying them.

## Project brief and element register

Record concept/reference paths, story moment, hero view, focal hierarchy, units/axes, target dimensions and their authority, explicit constraints, and unresolved manufacturing choices.

| Element | Story/visual role | Governing reference | Depends on / contacts | Reserved envelope | Method | Current artifact and status |
| --- | --- | --- | --- | --- | --- | --- |
| Base/terrain | Foundation and negative space | Composition reference | Overall scale | Footprint / heights | Editable masses | Path; provisional or accepted scope |
| Structure | Route, setting, support | Architectural crop | Terrain/landings | Placement reserve | Procedural or modeled | Path; status |
| Character | Focal action | Anatomy/style reference | Footing, sightlines, wing clearance | Pose and span | Sculpt or reconstruction | Path; status |
| Effect | Action and aftermath | Story plus effect crop | Source, impact, visibility | Route reserve | Separate sculpt | Path; status |

These rows are examples. Add a backdrop, hardware, or other systems only when the project calls for them. A dependency map can be a short sentence: terrain supports bridge; bridge determines foot contacts; figure placement determines whip route.

## Printer and scale record

```text
Printer: exact model, process, and selected configuration/profile
Usable build envelope: X/Y/Z, units, source, date verified, restricted areas
Intended material and applicable nozzle/process details: known or unresolved
Preferred finished scene dimensions: requested or provisional
Whole-part preference: avoid cuts for plate fit unless a tradeoff is accepted
Limiting components: dimensions at scene scale and candidate print orientations
Support/adhesion space: estimated during layout; checked in slicer before printing
Chosen coherent scene scale: reason, status, and any accepted tradeoff
Fit evidence: model-only estimate / supported slicer arrangement / physical test
Recheck triggers: scale, pose, component dimensions, printer/profile changes
```

Record unknowns explicitly and ask for the printer early. Do not treat a nominal build envelope as proof of printable fit or an old project's printer as the current selection.

## Mounting study record

Use [the mounting procedure](mounting-points.md) when deriving a receiving seat from any fixed character or object.

```text
Mounted object and receiving support: accepted baselines and fixed properties:
Selected mount method and excluded alternatives:
Permitted support-edit region and intended contact surfaces:
Solid cutter source, caps, coordinate frame, and allowance definition:
Retained source/pre-cut geometry and editable cutter paths:
Feature-clearance relief, retained support, and intentional locating/retention features:
Whole-object insertion/removal path and any staged assembly sequence:
Collision scope: geometry tested, poses sampled, clearance method, exclusions
Preservation evidence and new versus existing mesh defects:
Visual review artifact and status:
Outstanding topology, thickness, load, fit, adhesive, and physical tests:
```

Do not turn a local contact-region path result into a whole-object assembly claim, or a fit study into a proven structural mount.

## Physical test and artifact record

Use [fabrication and lighting](fabrication-and-lighting.md) to choose a representative test and interpret its scope.

```text
Question and exact interface/feature under test:
Source scene, exported file(s), revision/hash, scale, and coordinate frame:
Matching parts and hardware; which old revisions are incompatible:
Printer/process/material; settings actually known versus assumed:
Checks: source mesh / reopened export / native import-repair / layers-supports
Physical result: not started / underway / passed locally / failed; date and reporter
Observed fit, damage, removal behavior, or brightness; photos/measurements path:
Tested dimensions/surfaces to preserve; limits of transfer to other parts:
User-repaired artifact: received path or unavailable; comparison/revalidation status
Next revision or test, and which results remain applicable:
```

For lighting, add board/lead/connector access, retention/service slack, optical path, diffuser/interior material, and controlled comparison settings. A passed unwired pocket is not a passed wired installation. For export, identify geometry-only 3MF, native slicer project, or machine output explicitly.

## Active attempt and carryover record

Complete this at a whole-design or element restart, then keep it in the project checkpoint.

```text
Active attempt ID and root:
Restart scope: whole design or named elements
Current governing brief/references:
Allowed scene/component starting files:
Explicit carryovers: choice or artifact → user decision/current reference
Protected unaffected layers:
Excluded attempts/components/decisions:
Reusable technical methods: source → assumptions removed or revalidated
Unresolved carryover questions:
```

An empty carryover list for a restarted element means no old design choices have been adopted for that element. It does not erase standing user requirements or protected layers outside the restart scope. Do not infer carryover from file presence, old praise, or a generic “continue” message referring to the active attempt. Read the current checkpoint before searching historical files.

## Focused-reference request and result

- **Area and unresolved mismatch:** What remains wrong after the recent revisions?
- **Existing evidence checked:** Relevant full reference or crop already available.
- **Request:** One specific screenshot/crop request and the relationship to clarify.
- **Reference received:** Saved path, original source, and applicable element/property.
- **User clarification:** Concrete form, contact, direction, scale, or visibility constraint.
- **Next comparison:** Actual-model detail alongside the crop plus a scene check.

Do not request the same image again when it is already available. If no new image is available, use the existing reference to isolate the uncertainty and ask for a description or annotation; do not label your interpretation confirmed.

## Iteration record

- **Decision being tested:** One clear visual or technical question.
- **Current tweak:** One independently reviewable outcome; note any coupled edits it requires.
- **Remaining requested changes:** Ordered queue, including dependencies; retain items until completed or explicitly dropped.
- **Scope feedback, when needed:** Separate decisions identified, reason to split them, and recommended first change/order; record any user preference for a combined pass.
- **Starting artifact:** Exact scene/component path and relevant reference.
- **Change:** What changed and why; shape, placement, material, or lighting.
- **Protected scope:** Objects/properties that should remain established.
- **Result:** New editable file and compact actual-model comparison path.
- **Evidence:** User response and/or checks, with scope and method.
- **Status:** Candidate; accepted for the specified property; rejected; superseded.
- **Uncertainty and next step:** What the result does not establish and what resolves it.

Example: an accepted dragon translation establishes placement. It does not establish mount strength, and a subsequent flame study does not reopen the dragon pose by default.

## Project checkpoint

```text
Updated: date and change
Active attempt and restart scope:
Allowed sources / explicit carryovers / excluded prior attempts:
Current editable candidate: path
Last accepted baseline: path and accepted scope
Visual authority: original concept, element references, later clarifications
Constraints: active user decisions, printer/profile and usable envelope, whole-part preference, units/scale, protected layers
Completed: changes and inspected review artifact
Checks run this iteration: method, result, scope, audit path
Physical passes and protected interfaces: exact artifacts, scope, source of report
Delivered/repaired export authority: current files, superseded files, unavailable copies
Active print/test jobs: submitted or user-reported, awaiting result; avoid duplication
Historical checks relied on: source and continued applicability
Not yet qualified: specific remaining visual/engineering questions
Superseded/rejected sources: identities and restrictions
Next step: one concrete action
Reproduction: scripts/environment; running jobs if any
```

Do not copy a historical document's “current-session” wording into a new checkpoint as if the checks just ran.

## New lesson

When evidence changes how the next build should go, write it as a rule in `SKILL.md`: what was observed, what to do differently, the evidence and its limits. Keep exact poses, styles, hardware and repair parameters in the project's own records.
