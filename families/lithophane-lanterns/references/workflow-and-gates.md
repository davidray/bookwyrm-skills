# Workflow and gates

Use the earliest unsatisfied gate to decide what work is authorized. Preserve each approved artifact and give revisions stable identities.

## 1. Brief and concept

Reconcile the lantern's use, scale, panel count and story, hardware, finish, and authoritative visual references. If no concept exists, create a visual interpretation before committing to CAD. List what the concept invents.

Concept art is not to scale. Before blockout, measure the concept's key ratios in pixels and record them: body height to width, base or deck width to body width, roof height and overhang to body, panel field aspect. Carry them into the blockout and compare all of them, not only the body, at every matched view. (Lake-town: only body H/W was checked, and the deck came out 1.12× the body against the concept's ~1.4× until assembly.)

Most concepts are three-quarter views, so their ratios are foreshortened. Don't correct them with a formula: a √2 correction made Gollum's Cave's body 1.4 instead of about 1.0. Render a known mesh, such as the blockout, from the same camera, read the same ratios on it, and scale the concept's readings by the difference.

For an asymmetric concept, record which world corner or face each asymmetric feature is on (hero corner, door, figure groups), seen from the concept's own camera. Check that record at blockout and at assembly. A mirrored layout once passed every review for two hours.

Check the overall size against the series. The series sizes are kept consistent (Lonely Mountain is 232 × 232 × 399 mm; Bag End is a deliberate, squatter exception), and every part has to fit a printer's usable bed (see the print profile). When the art implies more, log it as a decision with the reason, and plan any segmentation at gate 2. The Christmas village grew to 559 mm, and its base split was found only at slicing.

Ask for approval of named visible properties such as silhouette, composition, roof language, supports, panel prominence, and illuminated mood. Concept approval authorizes blockout only; it does not validate hidden construction, dimensions, panel performance, mechanics, safety, or printability.

Keep the approved concept's look intact. If you think a visible feature is a printing risk, list it separately as your proposal, with the evidence, and let David decide. Do not record it as an approved "production change". (Dragon: "wings folded" was the agent's idea, written in as if approved; David has printed many open wings without trouble.)

## 2. Functional blockout

Build around the real hardware and panel system, not around the outside silhouette alone. Reserve:

- installed envelopes and removal paths;
- hands, fingers, switches, cables, and connectors;
- panel channels, overlap, extraction, and retention;
- diffuser and light spacing;
- roof/base removal and positive location;
- print segmentation and assembly order.

Run two automated checks before review: a pairwise clash check between every blockout part (target 0 mm³) and a minimum-engagement check for every slot, peg and seat (Lake-town: a panel edge engaged its post by only 0.7 mm until the posts were widened). Check the connector approach path with a ray or swept box.

Also check:

- **LED-to-panel distance** is inside the proven range in the [print profile](../../../shared/print-profile/print-profile.md) (`shared/print-profile/print-profile.md`). If it isn't, change the geometry (strip offset, post section, panel plane) or plan a light coupon. Two runs in a row accepted out-of-range distances with no coupon (41 mm, then 91 mm).
- **Every part fits the usable bed** of its printer, not the nominal one. Plan splits and joints here, not at slicing.

Show assembled, cutaway, exploded, and access states, and say in words how panels go in and how the roof or lid comes off. Record a small geometry-facts artifact with overall bounds, hardware reserve, panel field and thickness assumptions, clearances, service architecture, and known exclusions.

Obtain visual/functional blockout review before expensive detail. A material change to protected hardware, scale, panel architecture, or service direction reopens this gate.

## 3. Decorative integration, part by part

Do not decorate the whole lantern at once. Procedural whole-lantern decor and AI meshes fitted straight onto the whole blockout both fell well short of the concept on every lantern tried. Work part by part:

1. **Split the decoration into a few parts** (for example: plinth, corner column, panel surround, cornice and roof; or plinth plus four trees). Repeated parts are designed once and placed several times. Part boundaries should make sense as print or assembly segments where possible, but the visual split comes first.
2. **Write a part brief** for each: which of the approved concept's named visible properties it owns, what it owns visually, which protected interfaces it must respect, and the key protected dimensions (for example "upper step at least 90% of the lower step's width"). Check the art against the blockout and against the visible properties it owns before turning it into 3D. Plinth art twice came back too narrow to carry the body; Lake-town body art came back as an open frame that dropped the concept's plank walls and still missed its ratio. Art that fails either check is regenerated or the failure goes to David; do not accept it and plan to fix it later.

   A part brief also says:
   - **What the part must not include, and where it ends.** For example: no columns under the roof; no slab or plinth on the body; the body ends at the eave line. When parts are cut from a fused scene, the generator adds the neighbours back.
   - **The seat it must provide, not only its outer ratio.** For example: the base's flat centre must hold the body's foot plus clearance. A base once passed on outer width, but its tray was smaller than the body's foot.
   - **The character of each named property, not only its name.** For example: "icicles: long, dense, varied lengths in clusters, overlapping the window head"; "stalactites taper to points". A property can be present and still have lost its character.

   For any part that carries or hides panels, overlay the blockout's panel plane and slot depth on the part art, in plan and elevation, before 3D. Gollum's Cave body art put its arches inside the panel plane, which was found only after the 3D spend and forced a change of architecture.
3. **Make concept art for each part alone** and get each approved. Brief it in the approved concept's style, alone and centred on a plain mid-grey backdrop, three-quarter view from slightly above, whole part in frame, no text. For a single-colour hand-painted print, all detail must be carved relief (no painted-only detail). Do not put minimum-size or softening wording in the art prompt ("nothing thinner than a pencil", "nothing finer than 1.5 mm", "shallow recesses", "softened points"): the mesh copies the image, so the wording erases the detail. Check minimum features at fit and print time instead.
4. **Model each part separately** from its approved art. Do not send the painted art itself to 3D: make a 3D input image from it first (an unpainted resin-sculpt render, single view or a four-view sheet; see [image to 3D](../../../shared/image-to-3d/image-to-3d.md) (`shared/image-to-3d/image-to-3d.md`)), then image-to-3D. Review it with a three-up sheet: approved art, textured model, bare geometry. The bare view matters because texture can fake detail the print will not have. Also show the raw model before any fitting. A part passes when it is faithful to, or better than, its art.
5. **Variants.** Approve one design, then make sibling art by image-to-image from it (same style, camera, and backdrop; change only the dressing), then model each.
6. **Fit each part to its place** without deforming it (see modeling and evidence). If fitting changes a window or panel opening, record the final visible size and re-crop the panel art to it (Lake-town: the opening shrank from 110 to 100 mm wide and the crops were not redone). Show a part on a ghost of its neighbours when it cannot be judged alone (a quarter canopy).
7. **Re-review after engineering.** Trims, voxel solidify, smoothing, decimation, dropped shells and mirror repairs change form after a part has been judged faithful. Before export, review the engineered meshes again beside the art, with close-ups of the finest named features. Never cut decor flat where the art shows a point: taper or shorten it, or flag it. (Gollum's Cave: stalactites were trimmed flat and blunted by solidify, and the release failed on it.)
8. **Assemble** only after every part has passed, then compare matched views with the overall concept, for character and variety as well as proportion.

The art is the priority. When a faithful part breaks the blockout envelope, change the structure or ask; do not distort the part. When the art conflicts with optics (icicles that hang over a picture window, a figure in front of a panel), that is a decision. Name the conflict, choose, and log it. Don't resolve it silently in geometry. (The Christmas village's icicles came out short and above the window, which lost the concept's long, dense fringe, and no decision recorded why.) Expect natural forms to break the box (a canopy wider than the lantern, roots over the plinth) and ask about overhang early. A cosmetic protected interface may change when the art needs it (a panel mask following a branch arch); record it so panel prep follows.

If the lantern will be hand-painted, convert governed color boundaries into printable and reachable raised, recessed, grooved, or separate geometry. Presentation materials cannot stand in for absent production detail. Check the printability of thin AI-generated detail (leaves, web strands, hanging moss) per part, before assembly.

Obtain a final matched-view approval before print engineering when visual faithfulness is a governing requirement. A focused approval of one component does not approve the whole lantern.

## 4. Print engineering

Resolve segmentation, joined solids or deliberate joints, panel retention, service retention, orientations, supports, minimum features, tolerances, and assembly. Inspect topology and connectivity; overlapping objects are not automatically a united printable part.

Choose the smallest physical tests that retire the largest risks. Do not spend a full-lantern print to discover a light opening or panel channel is wrong.

## 5. Production panels and light test

Generate actual image-bearing relief, verify polarity and mapping, and print a representative optical coupon using the intended material, orientation, layer height, light source, and spacing. Evaluate readability both unlit and lit, hotspotting, contrast, minimum-thickness integrity, warping, and border/channel fit.

## 6. Export, slice, and release review

Export each production part from the current source. Round-trip it, audit the exported geometry, and inspect every sliced plate. Confirm quantities, orientation, material, supports, and assembly sequence. Package only the claim level actually supported by digital and physical evidence.

## Autonomous runs

When David hands every decision to the agent (a stress test, or "make all the decisions"), keep every gate but replace David's approvals with an independent review: a separate agent that is given only the approved art, the current renders, and the gate's checklist, not the builder's reasoning. Use it at gate 1 (concept and named properties), gate 2 (blockout and functional checks), gate 3 (each part, the engineered meshes, and the final matched view) and gate 5 (the panel set, including story and style consistency). Also use it whenever a reopening rule below fires. Self-review missed a mismatched panel set, a figure that read as the wrong character, and a body that had drifted from the concept.

Keep the reviewer independent:
- Give it images, the gate checklist, and a neutral part map (each part, its print orientation, and what is separate or glued on).
- Don't give it the builder's measurements or reasoning: it inherited a wrong ratio once and proposed a stretch from it. It measures for itself.
- Without the part map, it took separately printed icicle strips for islands on the roof.

A reviewer FAIL closes only with a fix and a re-review that passes. The builder can't waive it, and nor can the reviewer, even if it calls the result a "looser fit". If budget or tools rule out a fix, the release lists the FAIL at the top as unresolved, with the reviewer's words. It doesn't go under "known shortfalls". Tests 2 and 3 both waived FAILs.

Using a hybrid of the standard architectures, or departing from one (a decor shell over a standard cage, fused skins with split lighting), reopens gate 2. It needs a reviewer pass, a logged decision, and a line at the top of the release.

Log every decision David would normally make, with the reason, in the checkpoint as it is made. Rewrite the checkpoint's current-state block at every gate and after every decision; in test 3 it went stale for over an hour. Lock the result as described in validation and release, and do not merge it before David's verdict.


## Reopening rules

Refresh affected evidence after any material change to:

- authoritative concept or protected visual identity;
- actual hardware or measured envelope;
- overall scale;
- panel dimensions, thickness range, artwork, or orientation;
- light position, diffuser, or service architecture;
- retention, joints, segmentation, material, or print process.

Do not carry a prior score, pass, or approval across changed geometry unless its governed evidence is demonstrably unchanged.

## Review comments

Users often review by pinning comments on review sheets. Render a close-up of the pinned spot, state how you read the comment, and make the smallest change that fits that reading. If the reading is a guess, say so in the reply. (Lonely Mountain: a pin read as "widen the block sideways" produced a stretch David undid entirely; the intent was a lid that overlaps the frame.)

## Checkpoint

Keep a current-state block at the top of the project checkpoint: gate, evidence level, active source and print files, open decisions, and next step. Rewrite it every session. Keep dated history below it. Do not copy series-wide facts (strip, plate, tolerances) into each checkpoint where they go stale; reference this skill or one series note instead.
