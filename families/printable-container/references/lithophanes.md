# Lithophanes and inscriptions

Read this before making a lit pane, a scene image for one, or a carved or lit inscription.

## Source image

- Never build a pane from art seen at an angle. Flattening the concept's lid art stretched Bilbo about 1.6x vertically and made him man-sized. Generate the scene flat, at the pane's aspect, and check figure proportions (a hobbit is short, stout and barefoot) before converting.
- Generate at the visible area's aspect: 200 x 150 mm is 4:3 (1360 x 1024 px); with a 26 mm inscription strip it is 200 x 124 mm, about 1.61:1 (1408 x 872 px). Minimum is 5 px per mm.
- Local image models drift to illustration. Qwen-Image-Edit in ComfyUI gave ink-cartoon, then charcoal, then "film still" results over three rounds, never photoreal. After two rounds that miss, escalate: the user's own image, or a stronger model through Meshy (such as nano-banana-pro, 9 credits per image) with the credit cost stated first. David's own photoreal image was the one that worked.
- nano-banana-pro rejects 3:2; generate at 16:9 and crop.
- Use an old layout only as a rough guide; feeding it as a strong reference pulls the style back to cartoon.

## Converting to a pane

- Brightness maps to thickness: bright is thin. Brighten dark images heavily (lift shadows, not just exposure). A dark image prints as a featureless slab.
- Prefer a bright, foggy background behind dark figures, and avoid large areas of pure black.
- Crop rather than stretch to make room for text.
- The simulated backlit preview is a guide only; say so when showing it.

## Test and print

- Print a 100 x 100 mm test crop with the focal figure, the thinnest lines and part of the inscription before the full pane. With David's image it passed first time, and the full pane matched.
- Print flat, relief side up, 100% infill, white filament. Mount relief side out or the text reads backwards.
- Record the print settings with the result; wrong infill once invalidated a thickness test.

## Inscriptions

- House default fonts (the user may override per box): **Luminari** for carved inscriptions, **Trattatello** for lithophane inscriptions. Both are macOS system fonts.
- Carved inscriptions on a lid band: about 45 letters per side at 7 mm, or a shorter line larger. The Shire front quote uses 9 mm caps standing 1.9 mm proud, which survives 0.2 mm layers.
- Carved lettering is proven at 7 to 9 mm caps standing 1.9 mm proud. For smaller caps or strokes under 0.8 mm (two nozzle widths), print a coupon of the real text in its real print orientation first. Moria's 5 mm arch lettering is the smallest so far and still untested.
- Small carved text needs a plain bold face. Luminari's thin swashes blurred "ENTER" at 4.4 mm; DejaVu Serif Bold read better. To fit a long quote on an arc, condense the letters (74% width) rather than shrink them. Letters on the steep sides of an arch read worst.
- Lithophane inscriptions need thick strokes; Trattatello worked on the Mirkwood pane.
- Ask which quote to use, and use the exact text the user gives, including punctuation. No Tolkien-style font (Aniron, Ringbearer) is installed; offer to download one if the user wants a closer match.
