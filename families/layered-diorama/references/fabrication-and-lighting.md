# From approved geometry to tested parts

Procedures for turning an approved scene into parts that fit, print and light. Examples come from the Dale and Moria builds (2026-09).

## Separate parts by function

Tell an assembly joint apart from a cut made only to fit the printer. Removable carriers, support caps, service trays and light inserts can keep a character whole while making installation and service possible. If David plans to handle plate cuts in the slicer, don't add seams for them.

Plan assembly with every fixed part present: which parts move together, which supports are absent at each stage, and which fragile accessories go in last. Check the final pose and the motion into it. A carrier-only check can't clear the surrounding bridge or landing. (Dale: a fixed wing seat trapped the dragon; a removable rear support and cap kept the assembled surfaces and let it go in, with the mouth flame fitted afterwards. Moria: checking the whole bridge exposed contacts a partial check had missed.)

## Test the real interface, then protect it

Before a large print, test small pieces cut from the current mating geometry: both halves, the real hardware, the intended material, process and orientation. Label variants so feedback maps to a dimension, and ask whether they seat, rock, bind, snag or need force.

Record the interface, file revision, settings and result. A generic tolerance coupon doesn't qualify an untested interface, a resin result doesn't carry to PLA, and an unchanged pocket doesn't qualify a new carrier. When a mating dimension changes, deliver the matching pair and say which old parts no longer fit.

After a pass, protect those surfaces through later sculpting, repair and export, and compare against the tested file, not just the latest scene. If a change must reach a tested interface, say which test to repeat. Don't quietly improve a working fit. (Dale's first gate LED pocket was tight despite digital checks; revised pocket and slide with entry bevels passed. Moria: a two-notch coupon picked a 1.0 mm bore for 0.8 mm wire. These are case results, not universal clearances.)

## Glued joints

Every glued joint uses printed male/female tabs, never dowels or filament pins: see [glued joints](../../../shared/joints-and-assembly/glued-joints.md) (`shared/joints-and-assembly/glued-joints.md`). No diorama has printed one yet, so the first diorama joint that uses one gets a two-piece coupon cut from the real mating geometry.

Diorama exceptions (say which applies, and why, in the working record):
- A shaped mounting seat that already locates the object (feet in an adhesive seat, a cradle) is the female half.
- Not glued: removable carriers, support caps, service trays, light inserts, magnets and screws. A removable carrier needs its own looser, tested fit.
- Moving joints: hinges, pivots and axles.

Interfaces that have already passed a physical test keep the joints they passed with.

## Repair without discarding working geometry

Record the defects and protected surfaces before editing. Localise real defects before any broad repair, and inspect the result's silhouette, contacts, connectivity and intersections; a lower count in one checker isn't proof of improvement. Broad remeshing can lose rock masses or change soles and sockets; local relaxation, retriangulation or selective remeshing is easier to control. Choose the tool per mesh. When consolidating, include only current parts, never hidden old geometry or hardware placeholders, and keep the editable originals.

Say exactly what is preserved: exact coordinates, sampled surface agreement, or visual similarity. If a small fitted patch had to change, report it rather than claiming the interface is untouched.

## Solid parts still have thin features

Follow the solid-volume rule for FDM, keeping deliberate voids. A solid body can still have thin cloth, membranes, tips and bridges. Use photos of failed prints to find the problem, add material behind the feature where David agrees, and keep the visible sculpt and tested contacts. (Gandalf's cape printed with holes in both hollow and solid versions; a connected cape-to-robe underside fill was the fix to test. Broad fills that hid the folds were rejected.)

## Validate the delivered file and the slicer's reading of it

Reopen each exported file and check units, scale, transforms, object count, bounds, connectivity and topology. Say whether files share assembly coordinates or each has its own print origin.

Keep source checks, export checks, native slicer import, repair reports, slice review and physical results separate, and investigate when they disagree. Don't dismiss a slicer warning because another library says watertight. An indexed 3MF can keep connectivity that STL welding breaks (it did for the Balrog), but verify the round trip. A geometry-only 3MF is not a slicer project or machine file.

If David repairs a model in the slicer, that is a new file. Until you have it, don't reissue the unrepaired export as the repaired one. After orientation and supports, recheck plate centring, the whole support envelope, islands and removal access; an old slice doesn't update itself.

## Lighting

Follow the shared [lighting and electronics](../../../shared/lighting-and-electronics/lighting-and-electronics.md) (`shared/lighting-and-electronics/lighting-and-electronics.md`) method: measure the hardware before cutting pockets, make wired assemblies installable, check concealment, fit and light output separately, and test light paths one variable at a time with the real LED before repeating a design across the scene. List which exported revision includes each real opening.
