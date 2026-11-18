# Lithophane panels and optics

How to make a lit image panel for any family: a lantern's panels, a box's lid pane, a diorama's backlit window. The family skills say where the panel sits and how it is lit; this says how to make the image read.

## Source images for a scene panel

- Never build a panel from art seen at an angle. Flattening a box concept's lid art stretched Bilbo about 1.6× vertically and made him man-sized. Generate the scene flat, at the panel's aspect, and check figure proportions (a hobbit is short, stout and barefoot) before converting.
- Generate at the visible area's aspect, at 5 px per mm or more (a 200 × 150 mm pane is 4:3, 1360 × 1024 px). Crop rather than stretch to make room for text.
- Prefer a bright, foggy background behind dark figures, and avoid large areas of pure black. Brighten dark images heavily (lift shadows, not just exposure): a dark image prints as a featureless slab.
- Which image model to use, and what drift to expect, is in the family's concept or art-pipeline notes.

## Prepare the image for transmitted light

Start from the intended visible crop and final aspect ratio. The visible crop is the final window opening after the frame is fitted, which can be smaller than the panel field; re-crop when the opening changes and keep focal content inside it. Protect recognizable faces, silhouettes, gestures, and narrative focal points. Simplify or remove low-value background detail that will become noise at print scale.

Convert and tune in grayscale while monitoring the histogram. Preserve separation in faces and focal forms; avoid broad clipped black areas that become needlessly thick and broad clipped white areas that become fragile. Local contrast is usually more useful than global drama. Process every panel as a member of one set so brightness and relief feel coherent around the lantern.

Record source image identity, crop, rotation, mirroring, grayscale/contrast operations, and face mapping. Verify that text, handedness, and narrative direction have not been mirrored.

Prep that has worked on David's panels (lanterns and boxes):

- A 1% autocontrast inside the visible field (0.5/99.5% for very dark images, plus a black-point lift so near-black areas still transmit some light).
- For a subject that must glow but is a dark colour in the art (a red dragon), a channel-weighted grey mix such as 0.75R + 0.2G + 0.05B so it prints thin and bright.
- Never crop panel art from an image that shows a lit lithophane, frame, or hand. Its tones already contain fake relief and glow and print muddy. Regenerate it as flat art (see the lanterns art pipeline's panel briefs).
- Generated art often paints its own arch, disc, or grey surround. Mask that away so the panel's own mask sits on or inside it, and keep focal content out of zones the frame covers.
- **Put the textured (relief) side outside, facing the viewer, and the flat side toward the light.** On David's first print with both choices visible (the one-piece Christmas village mini, 2026-11-14), the panels looked best with the texture outside. With the relief outside, the image reads the right way round without mirroring. This is a hard rule, not a preference: David, 2026-11-15, "The flat back should never face out on lithophanes. They don't look good that way." Never design a panel, window or skin with the flat face outside. Check the slot or seat for the relief side outward, and check that renders show the relief outside.

Check the story in the art, not only the tones: a scene can be wrong in content (Bilbo outside his own hall) even when it reads well.

## Generate real relief

Map image luminance into a bounded thickness field. In the usual positive lithophane convention:

- bright image value -> thinner material -> more transmitted light;
- dark image value -> thicker material -> less transmitted light.

Verify the convention because displacement direction, normals, image inversion, and viewing from the opposite face can reverse the result. Inspect a thickness or false-color preview before creating a dense final mesh.

Use enough mesh resolution for the image at final size without creating gratuitous density. Preserve a flat seating border when the frame or channel needs one. Apply transforms and verify the final physical thickness range after modifiers. A flat textured plate, shader bump, emission map, or render-only displacement is not a production lithophane.

## Choose parameters by process

Start from the proven recipe in the [print profile](../print-profile/print-profile.md) (0.8 mm bright to 2.0 mm dark, white PLA, 100% infill, 0.10 mm layers, flat back down, 3.2 mm border) and skip a new tonal coupon unless the material, light distance, or process changes. Otherwise, do not copy a thickness recipe blindly between panel sizes, printers, materials, nozzles, layer heights, or light sources. Establish a starting base thickness and relief range appropriate to the process, then print a compact tonal coupon. The coupon should include gradients, faces or other representative detail, thin bright regions, thick dark regions, and the actual border/channel cross-section when practical.

Print in the intended production orientation. Flat printing is simple and stable but quantizes relief by layer height; edge/upright printing can offer smoother thickness changes but is tall, slower, and more sensitive to wobble and adhesion. Let the actual printer and desired image quality decide.

A new layer height, nozzle or tone map is a process change, so it needs a coupon before any production panel. When the coupon can't be printed first (an autonomous run), ship it with the release, and say that the panels should not be printed until the coupon has been printed, lit and accepted.

## Detail limits

How much detail a flat-printed lithophane holds is set in XY, by the extrusion line and by light scattering inside 0.8–2 mm of PLA. Layer height does not set it. The working limits below come from stress test 3 (Christmas village, 2026-11-06). They were not printed, so replace them with coupon results when those exist.

- **Line width is the floor.** A 0.4 mm nozzle draws lines about 0.42 mm wide. Lines, edges and gaps narrower than about two line widths (0.8–1 mm) won't read when lit. Faces less than about 5 mm tall lose their features. Hatching and engraving lines 1–2 source pixels wide merge into midtone.
- **Thinner layers add tone levels, not sharpness.** Over 0.8–2.0 mm, 0.10 mm layers give 12 levels and 0.08 mm gives 16, but each panel takes 4–5 h. Use 0.08 mm for smooth gradients (sky, glow), not for fine lines.
- **Grid and source resolution.** A height-field grid of about half the line width (0.2 mm on a 0.4 mm nozzle) is enough. A finer one only adds triangles: a 0.15 mm grid gave 2 M triangles and 18 MB per panel. About 3 source px/mm is enough, so a 512 px tile across a 173 mm field already matches the nozzle.
- **Smooth the thickness to the nozzle before quantising.** Most unprintable specks come from image detail finer than one line, not from the dither. Run a median filter over the continuous thickness map, about two line widths across (0.45 mm on a 0.2 mm nozzle). Then round or dither to layers. On a 30 mm crop of a Christmas village panel, this cut the islands with no extrudable layer below them from 1116 to 85. Plain rounding with no filter left 1068.
- **Dither only at or above the line width.** Floyd–Steinberg dither on single 0.15 mm cells made the slicer report "floating regions" on every panel, because the cells are narrower than one line. Use clustered (Bayer 4×4) dots at least one line width across (0.3 mm on a 0.2 mm nozzle), or don't dither. The filter and the dither are in bookwyrm-lanterns `lanterns/christmas-village/v1/source/panels/litho.py`.
- **Count islands, and treat slicer warnings on panels as failed checks.** For each layer, count the regions narrower than one line or with no extrudable layer below them, and aim for close to zero. A "floating regions" or "thin wall" warning on a lithophane means part of the relief can't be drawn. Fix the cause, then re-slice. Christmas village v2 still warned on all four panels, while its coupon and a smooth control ramp sliced clean.
- **A smaller nozzle buys detail with time.** A 0.2 mm nozzle halves the line width but triples the print time: 12.5–14.3 h per panel on the A1, against 4–5 h at 0.4 mm. Its 0.60–2.36 mm relief is outside the proven band and needs its own coupon.
- **Tone-map constants need calibration.** A Beer–Lambert map needs PLA's attenuation `k`. It was guessed at 1.6 /mm and never measured. Calibrate it from a printed step wedge photographed under the real LED before relying on it.
- **Crop small windows to the focal subject.** At about 58 × 37 mm (the Christmas village mini), busy full-size scenes read as mush in a simulated backlight. Crop each panel to its main subject so the main shapes are at least about 1/10 of the window width, and check the simulated backlight at final size.
- **Prefer bold forms in the art** (see the lanterns art pipeline's panel briefs). Large near-white fields, such as snow scenes, leave little tonal room on a 0.8 mm floor and read low-contrast.

## Test before the full panel

- Print a 100 × 100 mm test crop with the focal figure, the thinnest lines and part of any inscription before the full panel. With David's own image on the Mirkwood case it passed first time, and the full pane matched.
- Print flat, relief side up, 100% infill, white filament, and mount relief side out, or any text reads backwards.
- Record the print settings with the result; wrong infill once invalidated a thickness test.
- The simulated backlit preview is a guide only; say so when showing it.
- Lithophane inscriptions need thick strokes (Trattatello worked on the Mirkwood pane).

## Evaluate the physical panel

Inspect under the intended LED, spacing, diffuser, and ambient-light conditions. Record:

- unlit surface quality and structural integrity;
- lit contrast, tonal ordering, facial or focal readability;
- hotspots, dark bands, seams, and edge leakage;
- warping and channel fit;
- whether the thinnest regions survive handling;
- whether the thickest regions waste print time or block too much light.

Tune image curve, thickness range, spacing, or diffusion from this result. A rendered glow preview is useful for composition, not optical qualification.

When a backlit simulation is measured (sharpness, tonal spread, black level, brightness by panel), report the losses beside the recipe's claims in the README and in the message to David. In test 3 the reviewer measured about 85% sharpness loss, but the release and the message to David mentioned only the extra tone levels. Once a coupon has been printed and photographed, fit the simulation's blur and attenuation to the photo.

## Integrated two-colour lithophane skins

A lithophane region can be printed into an opaque wall instead of as a separate panel (the lit-shell architecture). Proven layout from Dragon Mountain:

- Opaque wall at least 3.2 mm (black PLA); the lit region is white PLA (not Matte) that runs all the way through the wall to the hollow.
- White skin in the proven 0.8–2.0 mm range with the hollow directly behind it (Dragon used a uniform 1.6 mm). Any white backed by black reads dark; report the share of white area lit through a thin skin (Dragon: 86%).
- Print on the X2D with both nozzles, within the 235.5 × 256 × 256 mm two-nozzle area, as one object with multiple parts in Bambu Studio.
- Close the lit region's edges against the wall so no gray rock shows between lobes, and keep the region touching the surface it sits on.
- Tonal relief inside the skin is an optional later refinement; a uniform skin is a valid first print.

## Colouring with alcohol ink (tested, set aside)

David tested alcohol ink on lithophanes on 2026-11-18 with a coupon plate: lead-line windows with and without back grooves, and a thickness wedge with bare and primed rows. The generator and test sheet are in davidray/bookwyrm-lanterns, `coupons/alcohol-ink-stained-glass/` (PR #87).

- Ink works best on the **flat back**. That is also the side facing the LEDs, so the colour sits inside the lantern, away from hands.
- David has ideas for using it but has set it aside for now. Don't add ink to a lantern unless he asks.
- When he does, give inked panels **"paint by number" guide lines on the back** that mark each colour region, so he can see where each colour goes while painting from behind. The coupon used 0.8 mm wide, 0.4 mm deep grooves under 3.2 mm lead lines; the back still prints flat on the bed. The groove size is a starting point, not a proven value.
- Painting from the back flips the design left to right, so any labels or maps for the painter must be drawn as seen from the back.

## Multi-panel consistency

Name panels by face and viewing direction. Include a face map in the release README. Generate the set in one style (one shared style line in every prompt, all four in the same pass) and regenerate any panel whose medium differs. Normalize the set so one panel does not dominate because its source image was brighter or its relief range differed. Confirm installed orientation in an assembled test; a correct isolated panel can still be reversed or mirrored in the lantern.
