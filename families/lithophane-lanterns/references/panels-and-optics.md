# Lithophane panels and optics

## Prepare the image for transmitted light

Start from the intended visible crop and final aspect ratio. Protect recognizable faces, silhouettes, gestures, and narrative focal points. Simplify or remove low-value background detail that will become noise at print scale.

Convert and tune in grayscale while monitoring the histogram. Preserve separation in faces and focal forms; avoid broad clipped black areas that become needlessly thick and broad clipped white areas that become fragile. Local contrast is usually more useful than global drama. Process every panel as a member of one set so brightness and relief feel coherent around the lantern.

Record source image identity, crop, rotation, mirroring, grayscale/contrast operations, and face mapping. Verify that text, handedness, and narrative direction have not been mirrored.

## Generate real relief

Map image luminance into a bounded thickness field. In the usual positive lithophane convention:

- bright image value -> thinner material -> more transmitted light;
- dark image value -> thicker material -> less transmitted light.

Verify the convention because displacement direction, normals, image inversion, and viewing from the opposite face can reverse the result. Inspect a thickness or false-color preview before creating a dense final mesh.

Use enough mesh resolution for the image at final size without creating gratuitous density. Preserve a flat seating border when the frame or channel needs one. Apply transforms and verify the final physical thickness range after modifiers. A flat textured plate, shader bump, emission map, or render-only displacement is not a production lithophane.

## Choose parameters by process

Do not copy a thickness recipe blindly between panel sizes, printers, materials, nozzles, layer heights, or light sources. Establish a starting base thickness and relief range appropriate to the process, then print a compact tonal coupon. The coupon should include gradients, faces or other representative detail, thin bright regions, thick dark regions, and the actual border/channel cross-section when practical.

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

## Multi-panel consistency

Name panels by face and viewing direction. Include a face map in the release. Normalize the set so one panel does not dominate because its source image was brighter or its relief range differed. Confirm installed orientation in an assembled test; a correct isolated panel can still be reversed or mirrored in the lantern.
