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

Common service patterns include roof-captured vertical panels, removable frames, side-loading channels, or separately fastened panels. Choose by actual assembly and replacement needs. A removable roof also needs positive location and retention; gravity alone may be acceptable only when the use case and evidence support it.

## Light path

Reserve the full optical volume early. Consider source-to-panel distance, source height, central obstructions, interior reflectance, diffuser placement, venting, and light leakage at seams. A tall central tower can create dark bands; a close point-like tea light can create hotspots. A diffuser can help but also costs brightness and space.

Evaluate all faces, not only the hero view. A four-panel lantern needs reasonably balanced illumination around the full perimeter. Use physical coupons for critical optical decisions because slicer walls, pigment, layer direction, and the actual LED dominate the result.

## Structure and segmentation

Decide which parts are intended to be single connected solids and which are deliberate assemblies. Check load paths and joints after Boolean operations and export. Visual overlap is not union; one object can still contain disconnected components.

Choose segmentation from build volume, support burden, panel installation, service, painting, and repair. Ensure the assembly order is possible without trapping panels, hardware, or fasteners. Keep fragile optical panels separate from high-support structural prints where practical.

## Scaling

Scale the architecture selectively. Keep real hardware, required clearances, printable wall/relief features, and usable access at viable absolute dimensions. Recompose the exterior around them. When a larger light replaces a smaller one, expect footprint, base, and proportion changes; do not hide the change behind a uniform scale or stale visual approval.

## Finish

For single-color hand-painted frames, design crisp paint boundaries and brush access. Avoid using material color in renders to claim detail that is absent from the exported surface. Lithophane panels remain an optical/material system even when the frame is hand-painted.
