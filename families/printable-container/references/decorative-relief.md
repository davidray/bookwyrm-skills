# Decorative relief

Read this before decorating a shell or lid, or adding feet, handles or other ornament.

## Style

- Aim for epic, classical carved relief, not storybook or cartoon. David rejected the first Shire mockup as "too cartoonish" and liked the carved-panel r2.
- Prompt generators with "intricate realistic classical wood carving, deep bas-relief, not cartoon".
- Carve upright walls, not faces printed facing up. Relief on a lid top comes out flat at normal layer heights: Mirkwood's carved top frame printed poorly and David chose a flat top like Shire. Lid tops stay flat for now; print a coupon first if a top must carry relief.
- Build a depth hierarchy: focal forms (trunks, plaques, doors) up to about 10 mm proud; webs, branches and texture 1.5 to 3 mm. Sharp-edged relief takes a dark wash and drybrush well from a one-colour print.

## Pipeline that works

1. Generate carving with Meshy: image-to-3D from a true-proportion concept for a whole box, or text-to-3D "bas-relief carved panel" for one scene. Write the source image prompt for crisp carving and leave depth limits and paint-ease wording out of it; see [image-to-3D input](image-to-3d.md). Track credits and ask before large spends.
2. Raycast the mesh into a depth map (0.2 mm per pixel), subtract the local background, then compress the range (log plus Poisson, or k·tanh(R/s), for example 12·tanh(R/13) for bold focal relief).
3. Wrap the height map onto the real shell wall faces and corners. Mask protected zones first: seam, pull notches, service openings, magnet pockets, connector ports.
4. Apply a 45 degree overhang filter so walls print upright without supports. Expect mushroom caps and similar to become cones or brackets.
5. Union into one closed solid and audit the exported file.

Meshy limits: text-to-3D ornaments come back as minis on round bases, so cut ornaments from carved panels instead. A lid top fed through image-to-3D becomes a diorama. Unseen sides come back blank, so give it views of every side.

Headless Blender (`pip download bpy`) runs Cycles renders in a cloud container; Workbench and EEVEE need a display and do not.

## Edges, frames and corners

- Panel frames, bands and beads run continuously around every corner, top and bottom. A frame that stops at a plain rounded corner leaves a square-ended lip (Shire base r1).
- Relief must not refill an edge round. Clip heightfield solids, including their flat backing slab, away from rounds, then check the edge profile with ray casts or sections along every side, not only at corners (Shire lid r3 kept its 6 mm round only at the corners).
- A thin rim limits its round: a 2.7 mm skirt seated on a 3 mm ledge took only a 1.2 mm round.

## Feet and other protruding ornament

- Organic feet are chunky stumps: short, thick roots (8 mm or more across) fused to the ground and to a solid core. Thin roots were rejected twice as "will break"; hand-built lumpy stumps were rejected as looking like dough.
- Repair generated meshes before use: bisect top and bottom, fill holes, voxel remesh about 0.25 mm, drip-fill under overhangs at 45 degrees, and 3D-close about 1.2 mm to fuse thin stems.
- Print feet and handles as separate parts and glue them. Check floor thickness under each socket before cutting.

## Mating features stay exact

- Pegs, tabs and sockets are exact CSG solids added after any remesh or smoothing. Smoothing rounded the Shire foot pegs and flared their sides, and they failed the fit test. Use plain straight cylinders or prisms with no rounding.
- Key one-way parts with an asymmetric tab (a teardrop worked). A 0.2 mm gap is enough for glued alignment tabs.
