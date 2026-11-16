# Miniaturize a lantern

How to make a small version of a finished lantern that sits over an LED tea light. The body prints in one piece, and the lithophane panels print separately and are glued in from the outside. This was learned from `lanterns/christmas-village-mini/v1/`, which is the full-size Christmas village v3 at 1/3 scale. David printed r3 on 2026-11-14. That build integrated the lithophanes into the body, and David then chose separate glued-in panels for minis (2026-11-15). Its code (`source/build_mini.py`, `check_walls.py`, `export.py`) is still the reference for the body.

A mini is its own piece. Give it its own library slug, `<slug>-mini`, and its own folder, `lanterns/<slug>-mini/v1/`. Don't make it a revision of the full-size lantern.

## What scales and what doesn't

- **Scale uniformly:** the exterior, meaning the silhouette and the decoration. Don't thicken anything on assumption. Report what is lost at the new size instead (see below).
- **Re-engineer at mini size:** the light cavity, the window seats, the lithophane panels and the wall thickness. Lithophane relief stays 0.8–2.0 mm, and opaque walls stay at least 1.6 mm. This is a redesign of the function, not a scaled copy.

## Steps

1. **Scale: 1/3 by default** (David, 2026-11-15). Check that the cavity clears the locked tea-light envelope (48 mm across, 55 mm tall; see [standard lighting architectures](standard-lighting-architectures.md)), that the windows are at least about 45 mm wide, and that the body fits the bed in one part. At 1/3 the Christmas village gave a 66 mm opening and 58 mm windows. Use a different scale only if 1/3 fails one of these checks or David asks, and say why.
2. **Load the exterior in the world frame.** Use only the exterior parts: no divider, plate, panels or hardware. Today this is a per-lantern loader (`load_full.py` in the mini). It becomes generic once each lantern's assemble script writes out its part transforms.
3. **Fill solid, then scale.**
   - Fill the hollows with a core that follows the outside surface: ray-cast a heightfield down from above and keep it about 2 mm (full size) under the roof. Never fill with a box or other primitive that can stand proud of the exterior. In r1 and r2 the core box poked four flat planes through the roof hips, and only David caught them.
   - Fill any closed voids that are left. The village roof had 26.
   - Fuse glue-in parts (icicle strips, vanes) to their host. Swell each one by about its groove clearance so it unions with the host. Otherwise it floats as a separate body; the village's 12 strips sat 0.1 mm off the roof.
4. **Carve the cavity.** Make an open-bottom column with a 45° pyramid ceiling, so nothing inside needs supports. Keep every opaque wall at least 1.6 mm, and add material back wherever the cavity would come closer.
5. **Seat the windows for glued-in panels.** David chose this on 2026-11-15: no slots, and nothing has to pass through the inside.
   - From the outside, cut a recess in each window about as deep as the panel's border. Leave a lip about 2 mm wide all round as a glue land. Inside the lip, cut the window through to the cavity.
   - Give the panel 0.3 mm of clearance per side in the recess, which is the proven pane-seat clearance.
   - Chamfer the top edge of the through-opening at 45°. Otherwise it is a flat ledge facing down into the cavity, and tree supports grow up to it from the bed, as they did to r1's pocket top (210 mm²).
   - The lip, the recess and the through-opening are part of the body, so the one-body and overhang checks in step 8 cover them.
   - Panels are separate, so the body can be any colour of PLA. Only the panels need white PLA.
6. **Make the panels as separate prints.**
   - Use the proven flat recipe: white PLA (not Matte), 100 % infill, 0.10 mm layers, printed flat with the back down. Relief runs 0.8 mm bright to 2.0 mm dark, inside a flat border that matches the lip.
   - **Glue the textured side outside**, toward the viewer, with the flat back on the lip toward the light (see [panels and optics](panels-and-optics.md)). The r3 print had its texture inside, and David judged texture outside looks better.
   - Printing flat avoids the upright-relief overhangs that integrated panels have.
   - Panels can be reprinted or swapped without reprinting the body.
7. **Re-crop the panels to their focal subjects.** Full-size scenes read as mush at about 58 × 37 mm. Crop each panel so its main shapes are at least about 1/10 of the window width, then check a simulated tea-light backlight. This is the step that needs judgement.
8. **Run the checks before slicing.** Any failure blocks the slice.
   - The model is exactly one body with no internal voids.
   - The outer surface matches the scaled original within about 0.3 mm (Hausdorff distance), with no new flat planes.
   - No surface inside the cavity faces down steeper than 45° (normal z < −0.71).
   - Wall thickness passes. Use a 0.6 mm tolerance band at the cavity skin; without it the voxel check reports false 0.25 mm walls.
9. **Review.**
   - Make clay renders with the full-size lantern beside the mini.
   - Include a contrast-boosted or curvature-shaded view, because white-on-white clay hid the roof planes.
   - Write a "lost at this size" list: features under about 0.4 mm wide or proud. In the village these were the icicle tips, the vane arm tips and the sign letters.
   - Take every number in the README from the facts and check files, not from memory. The r1 README claimed 1.2 mm walls where the check had measured 0.9 mm.
10. **Slice, then register.**
   - Slice on the A1 with tree supports and "on build plate only" **off**. Turning it on can't keep supports out of the cavity, because the cavity floor is the bed.
   - Re-slice after every model fix. The slice is a real gate: it found the inside supports that every digital check had missed.
   - Slice the panels on their own plate with the proven flat recipe.
   - Register the next library revision, with the body and the panels as separate components.

## Not yet proven

- The tea-light size is nominal (38 mm, not measured). The baseline envelope covers the uncertainty, so the light never needs to fit exactly.
- The glued-in seat (about a 2 mm lip, recess as deep as the border) has not been printed yet, and neither has a glue choice.
- Non-square bodies (octagonal, arched windows, lit shells) and lanterns that are already small.
