# Lithophane panels and optics

## Prepare the image for transmitted light

Start from the intended visible crop and final aspect ratio. Protect recognizable faces, silhouettes, gestures, and narrative focal points. Simplify or remove low-value background detail that will become noise at print scale.

Convert and tune in grayscale while monitoring the histogram. Preserve separation in faces and focal forms; avoid broad clipped black areas that become needlessly thick and broad clipped white areas that become fragile. Local contrast is usually more useful than global drama. Process every panel as a member of one set so brightness and relief feel coherent around the lantern.

Record source image identity, crop, rotation, mirroring, grayscale/contrast operations, and face mapping. Verify that text, handedness, and narrative direction have not been mirrored.

Prep that has worked on Dave's panels:

- A 1% autocontrast inside the visible field (0.5/99.5% for very dark images, plus a black-point lift so near-black areas still transmit some light).
- For a subject that must glow but is a dark colour in the art (a red dragon), a channel-weighted grey mix such as 0.75R + 0.2G + 0.05B so it prints thin and bright.
- Generated art often paints its own arch, disc, or grey surround. Mask that away so the panel's own mask sits on or inside it, and keep focal content out of zones the frame covers.
- When panels sit behind the relief-faces-LEDs convention, mirror the image in the relief so it reads correctly from outside.

Check the story in the art, not only the tones: a scene can be wrong in content (Bilbo outside his own hall) even when it reads well.

## Generate real relief

Map image luminance into a bounded thickness field. In the usual positive lithophane convention:

- bright image value -> thinner material -> more transmitted light;
- dark image value -> thicker material -> less transmitted light.

Verify the convention because displacement direction, normals, image inversion, and viewing from the opposite face can reverse the result. Inspect a thickness or false-color preview before creating a dense final mesh.

Use enough mesh resolution for the image at final size without creating gratuitous density. Preserve a flat seating border when the frame or channel needs one. Apply transforms and verify the final physical thickness range after modifiers. A flat textured plate, shader bump, emission map, or render-only displacement is not a production lithophane.

## Choose parameters by process

For Dave's lanterns, start from the proven recipe in the print profile (0.8 mm bright to 2.0 mm dark, white PLA, 100% infill, 0.10 mm layers, flat back down, 3.2 mm border) and skip a new tonal coupon unless the material, light distance, or process changes. Otherwise, do not copy a thickness recipe blindly between panel sizes, printers, materials, nozzles, layer heights, or light sources. Establish a starting base thickness and relief range appropriate to the process, then print a compact tonal coupon. The coupon should include gradients, faces or other representative detail, thin bright regions, thick dark regions, and the actual border/channel cross-section when practical.

Print in the intended production orientation. Flat printing is simple and stable but quantizes relief by layer height; edge/upright printing can offer smoother thickness changes but is tall, slower, and more sensitive to wobble and adhesion. Let the actual printer and desired image quality decide.

## Evaluate the physical panel

Inspect under the intended LED, spacing, diffuser, and ambient-light conditions. Record:

- unlit surface quality and structural integrity;
- lit contrast, tonal ordering, facial or focal readability;
- hotspots, dark bands, seams, and edge leakage;
- warping and channel fit;
- whether the thinnest regions survive handling;
- whether the thickest regions waste print time or block too much light.

Tune image curve, thickness range, spacing, or diffusion from this result. A rendered glow preview is useful for composition, not optical qualification.

## Integrated two-colour lithophane skins

A lithophane region can be printed into an opaque wall instead of as a separate panel (the lit-shell architecture). Proven layout from Dragon Mountain:

- Opaque wall at least 3.2 mm (black PLA); the lit region is white PLA (not Matte) that runs all the way through the wall to the hollow.
- White skin in the proven 0.8–2.0 mm range with the hollow directly behind it (Dragon used a uniform 1.6 mm). Any white backed by black reads dark; report the share of white area lit through a thin skin (Dragon: 86%).
- Print on the X2D with both nozzles, within the 235.5 × 256 × 256 mm two-nozzle area, as one object with multiple parts in Bambu Studio.
- Close the lit region's edges against the wall so no gray rock shows between lobes, and keep the region touching the surface it sits on.
- Tonal relief inside the skin is an optional later refinement; a uniform skin is a valid first print.

## Multi-panel consistency

Name panels by face and viewing direction. Include a face map in the release. Normalize the set so one panel does not dominate because its source image was brighter or its relief range differed. Confirm installed orientation in an assembled test; a correct isolated panel can still be reversed or mirrored in the lantern.
