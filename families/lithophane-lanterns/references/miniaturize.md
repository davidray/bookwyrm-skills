# Miniaturize a lantern

How to make a small, one-piece version of a finished lantern that sits over an LED tea light. It was learned from `lanterns/christmas-village-mini/v1/`, which is the full-size Christmas village v3 at 1/3 scale. David printed r3 on 2026-11-14. The code there (`source/build_mini.py`, `check_walls.py`, `export.py`) is the reference implementation.

A mini is its own piece. Give it its own library slug, `<slug>-mini`, and its own folder, `lanterns/<slug>-mini/v1/`. Don't make it a revision of the full-size lantern.

## What scales and what doesn't

- **Scale uniformly:** the exterior, meaning the silhouette and the decoration. Don't thicken anything on assumption. Report what is lost at the new size instead (see below).
- **Re-engineer at mini size:** the light cavity, the windows, the lithophanes and the wall thickness. Lithophane relief stays 0.8–2.0 mm, and opaque walls stay at least 1.6 mm. This is a redesign of the function, not a scaled copy.

## Steps

1. **Pick the scale.** Use the largest of 1/2, 1/3 or 1/4 that leaves a tea-light opening of at least about 45 mm and windows at least about 45 mm wide, and fits the bed in one part. At 1/3 the Christmas village gave a 66 mm opening and 58 mm windows. Say which scale you chose and why.
2. **Load the exterior in the world frame.** Use only the exterior parts: no divider, plate, panels or hardware. Today this is a per-lantern loader (`load_full.py` in the mini). It becomes generic once each lantern's assemble script writes out its part transforms.
3. **Fill solid, then scale.**
   - Fill the hollows with a core that follows the outside surface: ray-cast a heightfield down from above and keep it about 2 mm (full size) under the roof. Never fill with a box or other primitive that can stand proud of the exterior. In r1 and r2 the core box poked four flat planes through the roof hips, and only David caught them.
   - Fill any closed voids that are left. The village roof had 26.
   - Fuse glue-in parts (icicle strips, vanes) to their host. Swell each one by about its groove clearance so it unions with the host. Otherwise it floats as a separate body; the village's 12 strips sat 0.1 mm off the roof.
4. **Carve the cavity.** Make an open-bottom column with a 45° pyramid ceiling, so nothing inside needs supports. Keep every opaque wall at least 1.6 mm, and add material back wherever the cavity would come closer.
5. **Make the lithophanes.**
   - Cut a pocket in each window and union in a gridded heightfield slab. Grid both faces: a flat face fanned to the edge vertices renders black in Cycles.
   - **The textured side goes outside**, toward the viewer (see [panels and optics](panels-and-optics.md)). The r3 print had its texture inside, and David judged texture outside looks better.
   - Limit the relief slope to 45° on whichever face points down at an angle, and chamfer the pocket top at 45°. In r1, a 210 mm² pocket ledge grew tree supports up from the bed inside the cavity.
   - With the texture outside, its downward-facing steps become exterior overhangs on a vertical window. This is untested; check them in the slice.
6. **Re-crop the panels to their focal subjects.** Full-size scenes read as mush at about 58 × 37 mm. Crop each panel so its main shapes are at least about 1/10 of the window width, then check a simulated tea-light backlight. This is the step that needs judgement.
7. **Run the checks before slicing.** Any failure blocks the slice.
   - The model is exactly one body with no internal voids.
   - The outer surface matches the scaled original within about 0.3 mm (Hausdorff distance), with no new flat planes.
   - No surface inside the cavity faces down steeper than 45° (normal z < −0.71).
   - Wall thickness passes. Use a 0.6 mm tolerance band at the cavity skin; without it the voxel check reports false 0.25 mm walls.
8. **Review.**
   - Make clay renders with the full-size lantern beside the mini.
   - Include a contrast-boosted or curvature-shaded view, because white-on-white clay hid the roof planes.
   - Write a "lost at this size" list: features under about 0.4 mm wide or proud. In the village these were the icicle tips, the vane arm tips and the sign letters.
   - Take every number in the README from the facts and check files, not from memory. The r1 README claimed 1.2 mm walls where the check had measured 0.9 mm.
9. **Slice, then register.**
   - Slice on the A1 with tree supports and "on build plate only" **off**. Turning it on can't keep supports out of the cavity, because the cavity floor is the bed.
   - Re-slice after every model fix. The slice is a real gate: it found the inside supports that every digital check had missed.
   - Register the next library revision.

## Not yet proven

- No tea-light baseline is locked yet (see [standard lighting architectures](standard-lighting-architectures.md)). The open bottom fits any tea light up to about 60 mm across.
- Non-square bodies (octagonal, arched windows, lit shells) and lanterns that are already small.
