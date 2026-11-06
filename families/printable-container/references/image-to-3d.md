# Image-to-3D input (Meshy)

Read this before sending any image to Meshy (or another image-to-3D generator) for a figure, creature, foot, ornament or carved panel. The rules come from David's tests (Meshy 7.1, tabletop scale, 0.12 mm layers) and the Nov 6 2026 A/B run in `shared/experiments/meshy-input-ab-r1/`.

## The input image decides the detail

- Meshy copies the detail drawn in the picture. Soft input gives soft output. Higher-resolution or upscaled inputs, the 2k mode and polycount settings barely changed the result; Meshy already returns 1 to 4 M faces.
- So spend effort on the input image, not on generator settings. Skip remesh and texture (`should_remesh: false`, `should_texture: false`) when only the geometry matters; that also costs less.

## Draw the input as a sculpt

Prompt the source image as an unpainted resin miniature, whatever the final scale:

> Sculpted like a premium unpainted resin tabletop miniature: deep-cut folds, crisp straps, buckles and engraved emblems, clean sharp-edged surfaces, slightly heroic proportions, sharp focus, high image quality, crisp studio lighting that shows every carved edge. No text, no labels, no colour, no paint.

For carved panels and box walls keep the carving language ("intricate realistic classical wood carving, deep bas-relief, not cartoon") and add the same sharp-edge and crisp-lighting wording.

## Keep printability out of the prompt

Words added for printability, painting ease or older generators erase the detail you want. Don't put these in an image-to-3D source prompt:

- "shallow printable recesses", "softened points", "rounded", "smoothed"
- "bold, simple forms that are easy to paint", "chunky shapes", "no thin spindly parts"
- "relief stays within about N mm" (a depth limit belongs to the height-map compression, not the image)
- "soft studio light", "soft light", "clay-grey matte ... concept render" (soft light and clay renders read as soft geometry)

These were in this project's own prompts: Mirkwood concept r3 (`projects/mirkwood-travel-case/concept-r3-prompt.md`: "bold, simple forms that are easy to paint", "relief stays within about 6 mm", negative "thin spindly strands", "soft studio light") and the Moria concepts ("soft light", "smoothed rock"). They are fine for a concept image the user only looks at; rewrite them before the image goes to 3D.

Handle printability after generation, where it is measurable: height-map compression and the 45 degree overhang filter for relief ([decorative relief](decorative-relief.md)), SDF opening to remove fragile hair or strands, and 3D closing or thickening of thin stems ([moving parts and figures](moving-parts-and-figures.md)). Check thin parts (swords, spider legs, fingers) at print scale and tell the user which are fragile.

## Multi-view sheet for shape

- One detailed image gives the best surface but distorts the shape: figures came out slimmer, and a creature drawn at three-quarter view got a wrong footprint. Hidden sides come back blank or invented.
- Default: a front / left / back / right turnaround sheet drawn in the same resin-sculpt style, sent to `multi-image-to-3d`. Ask for "four views of the SAME model in a 2x2 grid: top-left front, top-right left side, bottom-left back, bottom-right right side; every view at exactly the same scale and height, standing on one shared ground line, orthographic, plain white background". Nano-banana-pro text-to-image at 1:1 produced clean grids.
- Every view must be at the same scale. Split the sheet with `scripts/split_turnaround_sheet.py`, which pastes every view unscaled onto one canvas, and check the view heights it prints agree within a few percent. If they don't, regenerate the sheet rather than guess.
- Restyling a soft image does not sharpen it. Feeding the clay-style concept as the reference for the sheet kept its chunky cartoon forms (A/B run, Bilbo and spider). Generate the sheet from words, or from a reference that already has crisp detail (the painted Gollum concept worked).
- For a figure that must match an approved concept (Gollum), use the concept as the sheet's reference and confirm pose and composition survived before generating 3D: the sheet can drift (Gollum's rocks and back changed).

## Scale before printing

Meshy's raw output is in arbitrary units (standing figures came in about 1.9 units tall, other subjects 1.2 to 1.8). Before any fit or print check, run `scripts/meshy_to_print.py`: Z-up, feet on the plate, scale to the target height (for example 32 mm tabletop, or the box's figure height), optional flat-bottom cut and round base, STL out. Raw Meshy meshes are often not watertight; repair as in [moving parts and figures](moving-parts-and-figures.md) before booleans.

## Judge with real renders

- Compare candidates with `scripts/render_closeups.py` (neutral grey Cycles, same height, front / three-quarter / back / top plus close-ups of the fine-detail areas: face, hands, buckles, emblems, fur) or in the slicer preview.
- Don't judge from a point-cloud render or a numeric smoothness score. A quick point cloud made a real improvement look like a tie, and in the A/B run a smoothing-displacement metric ranked the chunky clay figures higher because it measures big soft forms, not crisp edges.

## Cost

Meshy credits (Nov 2026): nano-banana-pro image 9 credits, image-to-3D or multi-image-to-3D without texture 20. A two-arm test on three subjects cost about 180 credits. Track spend in a ledger beside the outputs and state the cost before large spends.

Calling the API: the Blender MCP add-on stores the Meshy key in its preferences (`bpy.context.preferences.addons['blender_mcp'].preferences.meshy_api_key`), so API calls can run from the user's Blender without copying the key anywhere. The add-on's own `generate_3d` tool sends one image only; use the REST endpoints for multi-image.
