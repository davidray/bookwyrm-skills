# Dice towers

Read this for any piece that dice travel through: a dice tower, a tower with a tray, a chute built into a box or diorama. It comes from the wizard tower dice tower (bookwyrm-boxes `projects/wizard-tower-dice-tower/`, 2026-11-19), which was checked digitally but never rolled, so every number here is a starting point, not a proven value.

## Which dice

- Design for the largest die David will roll. Ask once. Without an answer, the house set is 16 mm dice with a d20 of about 22 mm (from listings, not measured), and the wizard tower designed for a 25 mm die to cover it.
- Record the die size in the brief as a choice, with its source.

## Passages

- **Tumbling passages** (chute, ramps, tunnel, exit door): start at 1.5 × the design die (37.5 mm for 25 mm) in every gap a die can tumble through. The margin is untested; a roll test replaces it.
- **Entries dice are dropped through by hand** (a hopper, belfry arches) need less: the die is placed, not tumbling. The wizard tower's arches pass 35.8 mm against 37.5 mm, and David accepted that ("Yes, both", 2026-11-19).
- Steps where parts join face downstream, so a die drops off them and never catches on them.
- The exit floor must not rise toward the door; check the threshold after any cut or boolean.
- Bounce-out: a die can fly out of an open entry opposite the one it went in. A low lip inside the far openings stops it; record it as a risk until a roll test shows otherwise.

## Keep dice and light apart

A lit tower shares one shell between the dice and the lamp. Split them with an opaque internal wall: lantern chamber and windows on one side, chute and ramps on the other, and a tunnel under the chamber to the door. No die reaches the lamp, and no ramp shadows a window. Every opening must be checked against that split: an opening on the chute side exposes the chute and lights nothing.

Layouts weighed and not chosen on the wizard tower: two masses on one tray (David: "I don't love the extra building"); a stacked tower (the dice still have to pass the lantern, so it needs the same split); a spiral ramp round a lantern core (spiral ramps jam and need tuned clearances).

## Check the path on the exported meshes

Run a swept-sphere check on the exported print parts as assembled, not on the parametric model: generated art and later cuts change the passages.

1. Voxelise the parts at 1 mm in Blender (a BVH ray cast up each column).
2. Take the distance from every free voxel to the nearest solid one; a sphere of radius r fits where that distance is at least r.
3. Flood-fill from outside each entry to the tray, and report the largest sphere that passes from each entry and where it pinches.

bookwyrm-boxes `projects/wizard-tower-dice-tower/scripts/check_dice_path_r1.py` does all three. At 1 mm voxels the result is good to about ±1 mm and leans optimistic, so treat a pass within 1 mm of the target as marginal. Check the parts the sphere passes near as well: the tail of a sculpted creature on the tray, a glued-on head at an entry.

## What a digital pass does not prove

A sphere is not a die. It says nothing about dice catching on edges, tumbling evenly, bouncing out, or noise. Before claiming the path works, roll David's largest die and a full set through the printed path (or a coupon of its tightest section) and record the result.
