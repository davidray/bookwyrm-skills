---
name: layered-diorama
description: Develop 3D dioramas from concept art through element decomposition, bottom-up modeling, isolated character development, scene integration, and print engineering. Use for staged diorama builds, revisions, and capturing lessons from them.
---

# Layered diorama

Paths such as `shared/...` and `families/...` are from the root of the bookwyrm-skills repo (`~/code/bookwyrm-skills` on David's Mac). Open them from there: a `../` link resolves wrongly when this skill is opened through a link in `~/.claude/skills/`.

Use this for a hand-modelled scene built in independently editable layers. For a scene whose pieces are mostly generated from one concept under a budget, use `generated-scene-diorama`. The method comes from the Smaug/Dale and Moria builds (2026-09): it gave controllable iteration and passed local fit tests, but no complete, lit, assembled diorama has been qualified with it yet.

Read the project's checkpoint before modeling: the active design attempt, its references and what is protected. Record formats are in [working records](references/working-records.md). Project-specific choices stay in the project checkpoint, not here.

## The pipeline

Concept, story and printer → element register and blockout → environment bottom-up → demanding elements on their own → integration → effects and finish → physical engineering → export, slicing and test parts.

It is a revisitable sequence. Reserve space for later elements early, investigate risky interfaces early, and finish their engineering once scale and composition are stable. A "layer" is an independently editable element or system, not a printer layer or a promise to print it separately.

### 1. Visual target and story

- Keep the original concept. Record the hero view, focal point, story moment, key silhouettes, negative space and provisional dimensions.
- Separate composition, character, surface and lighting references; each governs only its own properties. A later character reference can change a character without changing the composition.
- Labels on a concept sheet are reference content. Dimensions, electronics, materials and assembly features become requirements only when David says so.
- Turn vague descriptions into shape decisions: where something starts, what it touches, which way it moves, what must stay visible.

### Printer and scale

Ask early which printer and setup David means, and the finished size he wants, unless the brief says. The fleet and proven settings are in the [print profile](../../shared/print-profile/print-profile.md) (`shared/print-profile/print-profile.md`). Check the usable build volume in the current slicer profile, allowing for orientation, supports and brim.

David prefers whole parts to parts split for the plate. Choose a scene scale at which the limiting components fit whole in a sensible orientation. If that conflicts with size, detail or strength, show the trade-off before cutting: reorient or scale the scene first, and propose a split, with its location and assembly, only when those fail. Never shrink one element out of proportion to make it fit. If the printer is unknown, keep the scale marked provisional and settle it before scale-dependent detail.

### 2. Decompose and block out

Make an element register: role in the story, governing reference, what it sits on, dependencies, reserved envelope, method, interfaces and status. Typical groups: plinth, terrain or backdrop, architecture, characters, effects, hardware.

Block out the whole scene cheaply with every important volume, fixed units and axes, and repeatable cameras. Reserve feet, wing spans, tail sweeps, flame routes, crossings and likely mounts. Review the composition before refining anything; an attractive part can still be wrong for the scene. Label placeholders so they never become final by inertia.

### 3. Environment bottom-up

Build the plinth and terrain, then what stands on them (buildings, paths, bridges, landings), fitted to the real surfaces. Resolve silhouette, large masses, proportion and open space first, then medium forms, then selective detail. More detail never fixes the wrong structure: spikes plus noise are not geology, and roof tiles don't fix a badly placed village. Keep named collections and editable sources, and delay scene-wide fusion.

### 4. Demanding elements on their own

Choose a method per element. Procedural modeling suits terrain, masonry and layout. For recognisable organic subjects, try reference-driven sculpting or image to 3D early (see [image to 3D](../../shared/image-to-3d/image-to-3d.md), `shared/image-to-3d/image-to-3d.md`) rather than piling detail on a procedural form that lacks likeness.

Focused reference → isolated model → multi-angle review → cleanup → fit to the scene → integration review.

- Settle anatomy, gesture and equipment before texture. Check limb count, left and right, wing roots, hands, grips and load-bearing contacts in real views from several angles: overlapping silhouettes once made a knee look like a fist. Put important accessories (a sword, a whip) in the reference brief rather than retrofitting them.
- Judge geometry in neutral material renders. Colour, glow and dramatic light can't prove a shape.
- Keep the raw reconstruction and its input unchanged, and record the tool, settings and scale. Check the local tools before declaring generation blocked.
- Judge cleanup by kept silhouette and detail as well as topology. Don't chase one-component counts by deleting accessories or merging every near contact.
- If iterations keep polishing the wrong style or structure, change that element's reference or method and leave the rest of the scene alone.

### 5. Integrate one change at a time

Make one reviewable change per iteration, state what it should change, protect everything else, and compare with the baseline before the next. Coupled edits that serve one outcome (move a hand and keep its grip) count as one change.

When a request bundles several independent design decisions, say so briefly, name them and propose an order, and start on the first. Keep the rest queued and work through them without making David resubmit; ask for review only when the next change depends on an open visual decision. Honour an explicit request for a combined pass.

When the same area has needed two corrections without converging, or David repeats a concern, ask for a crop of that part of the concept with enough surroundings to show contact and direction, in a channel that takes images. Inspect a crop he already sent before asking again. Save it as a new reference, translate it into concrete constraints, and check the next model against it. It governs that feature only.

Keep shape changes separate from placement. Fit feet to the actual surface and check clearance between characters and scenery. Before a local edit, name the protected objects and verify them afterwards. Compare with the same cameras and neutral lighting, plus one diagnostic angle for hidden contacts.

Approval is scoped to what was reviewed: image direction, sculpture, placement, effects and engineering each have their own status. Never infer approval from silence, and don't invent a stop at every stage.

### Attempts and restarts

At a restart, find out whether David is replacing the whole design or one element, and record the active attempt, its references, allowed starting files, retained choices and excluded attempts. Within the restarted scope, nothing from an abandoned attempt carries over unless David kept it; a file on disk or an old approval is not authority. Technical methods can carry over once their embedded dimensions, poses and paths are checked. Before review, check source paths against this record.

### 6. Effects and finish

Route effects from the story and real contact surfaces (origin, path, impact, aftermath) before adding turbulence. Keep them separately editable. Protect negative space and silhouettes, and add damage selectively, away from seating surfaces. Show a neutral form view beside each lit presentation view; render light is illustrative until real hardware is tested.

### 7. Physical engineering

Plan mounting, access and any segmentation while composing. Once the design is stable, engineer thickness, load paths, joints, tolerances, supports, access and assembly order for the real printer, scale, material and hardware, and revisit the look if that changes visible geometry.

- **Mounts:** for any mounted character or object, follow [shaped mounting seats](references/mounting-points.md). Keep the accepted object and adapt its support.
- **Solid volumes:** for David's FDM work, model parts as solid and let the slicer set infill, keeping deliberate voids (sockets, light chambers, wire routes, tunnels).
- **Glued joints:** printed male/female tabs, never dowels or filament pins, per [glued joints](../../shared/joints-and-assembly/glued-joints.md) (`shared/joints-and-assembly/glued-joints.md`). Diorama exceptions are in [fabrication and lighting](references/fabrication-and-lighting.md#glued-joints).
- **Testing, repair, export and lighting:** follow [fabrication and lighting](references/fabrication-and-lighting.md).
- **Claims:** keep visual, geometric, manufacturing and physical claims apart, as in [evidence and claims](../../shared/evidence-and-claims/evidence-and-claims.md) (`shared/evidence-and-claims/evidence-and-claims.md`).

## Review and records

- **Small review payloads:** keep originals, full renders, logs and audits on disk. Review one compressed contact sheet per iteration (about 1,200 to 1,600 px, under 500 KB) and load a detail crop only for a specific question. Never print base64 images, mesh arrays or full scene dumps; filter tool output to paths, counts and short summaries. A long image-heavy session once failed with a 64 MiB request-size error; if that happens, stop retrying, save state, and continue from the checkpoint in a fresh task when David asks.
- **Checkpoint:** after each meaningful change, update the active file, reference authority, accepted decisions, protected scope, checks run now (not old ones), open issues and the next step. Archive superseded stages with pointers instead of keeping several "current" sections. A print underway is not a pass.
- **Lessons:** when evidence changes how the next build should go, add it as a rule here, in terms of roles and decisions, and keep named characters and dimensions as examples. Generalise only as far as the evidence goes.

## Saving a version

When David approves a version for printing or as a preview, save it as a draft through the workshop skill (`workshop/SKILL.md`), with the generating scripts and notes committed under `projects/<slug>/` in bookwyrm-dioramas. David promotes it as `v<N>`. At the end of a session that changed a diorama's meshes without saving a draft, say so in one line.
