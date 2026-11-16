# Glued joints: printed male/female tabs

The rule for every family. David set it on 2026-11-15 and made it firm on 2026-11-16: "we don't do dowels, we do alignment tabs."

Wherever two printed faces are glued together, align them with a male tab or plug printed on one face and a matching female socket printed in the other. Never use dowels, filament pins or pin holes for a glued joint. Loose pins are extra parts to cut, count and lose, small holes print undersize, and a printed pair locates the joint in one move. Doré lantern v1.4 replaced the 36 filament pins of v1.2 with 12 printed plugs, and the boxes' glued feet have always worked this way (a teardrop tab in a teardrop socket).

Plan the joints when you choose the segmentation, not after.

## Standard alignment tab (David, 2026-11-16)

- **Male:** 4.0 mm diameter, 4.0 mm tall.
- **Female:** 4.2 mm diameter, 4.2 mm deep.

Use this pair for every joint a round tab can carry. The starting sizes below are for non-round tabs and larger plugs.

## Shape

Use plain straight cylinders or prisms, built as exact CSG after any remesh, repair, smoothing or decimation, which round and flare them. Put a 0.3–0.5 mm chamfer on the male's tip as a lead-in and leave its sides straight. Generate both halves in the same script that makes the cut, keep the cutters editable, and record each feature's position and size in the part's facts file or the checkpoint.

## Starting sizes for other tabs and plugs

- **Clearance for a glued alignment fit:** 0.2 mm all round for tabs (the boxes' teardrop foot tab, printed and fitted) and about 0.1 mm per side for round plugs (Doré v1.4: 5.0 mm plugs in 5.2 mm sockets). These are tighter than a lift-off or drop-in fit on purpose. Dry joints that must come apart need their own tested fit: lantern roof pegs 6.0 in 6.6 mm, base locator tabs 0.3 mm per side, box drop-in panels 0.3 mm per edge.
- **Depth:** make the socket 0.2–0.5 mm deeper than the male stands proud (Doré: 6.0 mm proud in 6.5 mm; box feet: a 1.3 mm tab in a 1.5 mm socket), so glue has somewhere to go and the faces close fully.
- **Size:** at least 4 mm across, standing out no more than about 1.5 × its width, with at least 1.5 mm of material around the socket. Check the wall or floor behind every socket, and that none breaks through a decorated, carved or visible face.
- A size not yet printed in this family gets a two-piece coupon of the pair, cut from the real mating geometry, before the long print.

## Keying

A glued joint should go together only one way. Use one non-round tab (a teardrop or a D shape) or two features placed asymmetrically; one round plug can rotate.

When identical parts repeat, put the males on one face and the sockets on the other, so every copy is the same and still fits only the right way round (Doré v1.4 sixths: males on one cut face, sockets on the other; box feet: the tab on the foot, the socket in the shell). Where a part is the same both ways and its image or decoration must face out, add an asymmetric feature so it can't be flipped.

## Print orientation

Put the male on the part where it prints well: standing up from a face printed top-up, or sideways on a cut face of a part lying flat. A long thin peg printed upright snaps at a layer line, so keep it stubby or make it a wider tab. Never put a male on a face that prints against the bed; put the socket there.

## Cuts made in the slicer

When David splits a part for the bed in Bambu Studio himself, suggest the cut tool's plug connector (a printed male/female pair) rather than its dowel connector.

## Exceptions

Say which one applies, and why, in the product's README or working record. Each family lists its own common cases.

- **The joint is not glued:** anything that lifts off, comes out for service, or is held by magnets, screws or heat-set inserts.
- **Moving joints:** hinges, pivots and axles. A filament or metal pin is a fine axle.
- **The wall is too thin** to hold a socket without breaking through. Add a lug or boss behind the seam to carry the pair, or use a tongue and groove along the edge. Never a dowel or pin.
- **A shaped seat already locates the part** (a post socket, a cradle, feet in an adhesive seat): the seat is the female half and needs no extra tab.

Locked or promoted versions, and interfaces that already passed a physical test, keep the joints they have. Apply this rule to new products and new versions.
