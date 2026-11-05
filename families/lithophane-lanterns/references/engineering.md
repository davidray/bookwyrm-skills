# Lantern engineering

## Hardware and service

Model the measured light source as an envelope plus access requirements, not as a guessed primitive. Include the controlling diameter or width, height, flame-tip or lens height, switch location and travel, battery door, charging connector, cable bend, finger access, and removal direction as applicable.

Use low-voltage LEDs only. Keep open flame outside this workflow. Treat heat, battery safety, electrical compliance, and material temperature limits as separate requirements when consequential; ordinary visual and mesh checks do not qualify them.

Prefer a service route that does not require disturbing fragile lithophanes. The light should be positively located and remain removable. Verify access in the assembled state, including inversion and handling if those are expected.

## Panel architecture

Specify for each face:

- visible image field;
- finished panel outer dimensions;
- minimum and maximum thickness targets;
- frame overlap and light-blocking border;
- channel or pocket dimensions and clearance;
- bottom support and positive retention;
- insertion/removal path and required external clearance;
- face identity and correct image orientation.

Use a representative channel coupon before locking all faces. Long panels need allowance for printer variation, elephant foot, edge roughness, and warping. Do not choose a clearance solely from a generic tolerance table when a quick physical coupon is possible.

Common service patterns include roof-captured vertical panels, removable frames, side-loading channels, or separately fastened panels. Choose by actual assembly and replacement needs.

**Series default for Dave's square lanterns:** flat 3.2 mm panel plates drop into 3.8 mm slots from the top, rest on the slot floor, and are captured by the roof (0.2 mm above the panel). The relief faces the LEDs and the flat back faces out, so the image is mirrored in the relief. Service order: lift the roof, lift the panel. All three split-lit lanterns use this.

A removable roof needs positive location by default: locating pegs into the body (Bag End: four 6 × 5 mm pegs in 6.6 × 6.5 mm holes) or a keyed lip. Gravity-only seating needs the user's explicit acceptance. A decorative roof may sit over the body like a lid, with a pocket the body top nests into, as long as it still lifts straight off.

## Service face, door, and switch

Put the hardware plate's port window behind a service face. A decorative door can cover it (Bag End: a 38 mm green door held by four 6 × 3 mm magnets, with a full-window clearance pocket in its back). When the user wants a power switch, an SS12D00-type slide switch on the battery positive line before the charger/boost board, operated through a slot behind the door, is the recorded pattern. Without a switch request, keep a switch reserve at the service face.

## Light path

Reserve the full optical volume early. Consider source-to-panel distance, source height, central obstructions, interior reflectance, diffuser placement, venting, and light leakage at seams. A tall central tower can create dark bands; a close point-like tea light can create hotspots. A diffuser can help but also costs brightness and space.

Evaluate all faces, not only the hero view. A four-panel lantern needs reasonably balanced illumination around the full perimeter. Use physical coupons for critical optical decisions because slicer walls, pigment, layer direction, and the actual LED dominate the result.

## Structure and segmentation

Decide which parts are intended to be single connected solids and which are deliberate assemblies. Check load paths and joints after Boolean operations and export. Visual overlap is not union; one object can still contain disconnected components.

Choose segmentation from build volume, support burden, panel installation, service, painting, and repair. Ensure the assembly order is possible without trapping panels, hardware, or fasteners. Keep fragile optical panels separate from high-support structural prints where practical.

## Scaling

Scale the architecture selectively. Keep real hardware, required clearances, printable wall/relief features, and usable access at viable absolute dimensions. Recompose the exterior around them. When a larger light replaces a smaller one, expect footprint, base, and proportion changes; do not hide the change behind a uniform scale or stale visual approval.

Faithful decor parts often grow the lantern (wider plinth to carry the body, taller roof, canopy wider than the walls). That is acceptable when the art needs it. Re-check the build envelope for every part and say how the overall size changed.

Supports: decks that bridge a base bay print upright with tree supports inside the bay only, removed through the open bottom. Keep supports out of hollow lit interiors.

## Finish

For single-color hand-painted frames, design crisp paint boundaries and brush access. Avoid using material color in renders to claim detail that is absent from the exported surface. Lithophane panels remain an optical/material system even when the frame is hand-painted.
