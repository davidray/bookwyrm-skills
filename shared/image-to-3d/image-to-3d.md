# Image to 3D

Read this before sending any image to the 3D generator in any family: a lantern's decor part, a box's figure or carved panel, a diorama's building. The rules come from David's tests (made with Meshy 7.1, tabletop scale, 0.12 mm layers; they are about the input image, so they hold for Tripo too), the boxes' A/B run of 2026-11-06 (bookwyrm-boxes `shared/experiments/meshy-input-ab-r1/`) and the lanterns' A/B run (plinth, Lake-town roof, Mirkwood tree; `/mnt/project-files/meshy-input-ab/results.md`). This file replaces the `3d-generator` skill that earlier notes referred to; that skill never existed.

## Engines and prices

Check current prices before a batch; these were right on 2026-11-16.

- **Tripo** is the default 3D generator for every build (David, 2026-11-17): about $0.40 a detailed-geometry call, $0.20 for the standard one. Start with standard; use detailed for a hero part or when standard loses the detail the image shows.
- **Meshy 7.1** only when David asks for it by name: 20 credits a mesh-only image-to-3D or multi-image-to-3D call (about $0.40).
- **Images** (nano-banana-pro and the other image models Meshy routes) still cost about 9 Meshy credits each. So one part costs an image plus one Tripo call.
- Keys are read at run time from the environment and are never written to a file, log, checkpoint or repository.
- **How a build calls them:** on the Mac, over the Blender MCP. One image: `generate_3d(image=<absolute path>, provider="tripo")`, never `provider="auto"` (it can pick another engine). A multi-view sheet or anything the tool doesn't offer: a small helper run inside Blender that calls Tripo's API with `TRIPO_API_KEY`. Either way, keep one ledger per project that refuses a call when committed spend plus the estimate would pass the cap (the generated-scene-diorama `bk.py` helper and its ledger are the model; give a Tripo call its dollar estimate). Miniatures go through Builder's reconstruct tools instead, which have their own approvals.
- Ask before each spend with the estimate, read the live balance before the first one, and record task IDs and credits in the ledger and checkpoint.

## The input image decides the detail

- The generator copies the detail drawn in the picture. Soft input gives soft output. Higher-resolution or upscaled inputs, the 2k mode and polycount settings barely changed the result; the generator already returns 1 to 4 M faces.
- So spend effort on the input image, not on generator settings. Ask for untextured geometry when only the shape matters; that also costs less.

## Show the part alone

Image-to-3D is faithful when the part is shown alone, centred, on a plain backdrop, with the whole part in frame. The painted part art is the approval image; the image sent to 3D is made from it, as below.

## Draw the input as a sculpt

Paint and colour fake detail that has no relief behind it. After the painted art is approved, make the 3D input by image-to-image from it with the same object and camera, prompted as an unpainted resin miniature, whatever the final scale. In the lantern A/B run this never made a part worse and clearly sharpened organic detail (the tree's leaves and bark). Then name the part's own fine detail (engraved knotwork strands, shingle edges, bark furrows, leaf lobes and veins). A prompt that worked for figures:

> Sculpted like a premium unpainted resin tabletop miniature: deep-cut folds, crisp straps, buckles and engraved emblems, clean sharp-edged surfaces, slightly heroic proportions, sharp focus, high image quality, crisp studio lighting that shows every carved edge. No text, no labels, no colour, no paint.

For a lantern part, the A/B run used: "an unpainted grey resin miniature sculpt, uniform matte resin, no paint, no colour, no metal, every detail real sculpted relief, deep-cut carving, crisp sharp edges, clean sharp-edged surfaces, plain pale backdrop, high image quality, sharp focus, highly detailed".

For carved panels and box walls keep the carving language ("intricate realistic classical wood carving, deep bas-relief, not cartoon") and add the same sharp-edge and crisp-lighting wording.

## Keep printability out of the prompt

Words added for printability, painting ease or older generators erase the detail you want. Don't put these in an image-to-3D source prompt:

- "shallow printable recesses", "softened points", "rounded", "smoothed"
- "bold, simple forms that are easy to paint", "chunky shapes", "no thin spindly parts"
- "relief stays within about N mm" (a depth limit belongs to the height-map compression, not the image)
- "soft studio light", "soft light", "clay-grey matte ... concept render" (soft light and clay renders read as soft geometry)
- "nothing thinner than a pencil / matchstick", "nothing finer than 1.5 mm"

These were in the boxes' own prompts: Mirkwood concept r3 (bookwyrm-boxes `projects/mirkwood-travel-case/concept-r3-prompt.md`: "bold, simple forms that are easy to paint", "relief stays within about 6 mm", negative "thin spindly strands", "soft studio light") and the Moria concepts ("soft light", "smoothed rock"). They are fine for a concept image the user only looks at; rewrite them before the image goes to 3D.

Handle printability after generation, where it is measurable: height-map compression and the 45 degree overhang filter for relief ([decorative relief](../../families/printable-container/references/decorative-relief.md)), SDF opening to remove fragile hair or strands, and 3D closing or thickening of thin stems ([moving parts and figures](../../families/printable-container/references/moving-parts-and-figures.md)). Check thin parts (swords, spider legs, fingers) at print scale and tell the user which are fragile.

## Multi-view sheet for shape

- One detailed image gives the best surface but distorts the shape: figures came out slimmer, a creature drawn at three-quarter view got a wrong footprint, and the lanterns' tree came out 18% and roof 7% slimmer front to back. Hidden sides come back blank or invented.
- Default: a front / left / back / right turnaround sheet drawn in the same resin-sculpt style, sent to the generator's multi-view call. Ask for "four views of the SAME model in a 2x2 grid: top-left front, top-right left side, bottom-left back, bottom-right right side; every view at exactly the same scale and height, standing on one shared ground line, orthographic, plain white background". Nano-banana-pro text-to-image at 1:1 produced clean grids. A four-view sheet held a lantern part's footprint within 1%. Crop the tiles and send them with the front first.
- Every view must be at the same scale. Split the sheet with the boxes' [`split_turnaround_sheet.py`](../../families/printable-container/scripts/split_turnaround_sheet.py), which pastes every view unscaled onto one canvas, and check the view heights it prints agree within a few percent. If they don't, regenerate the sheet rather than guess.
- Restyling a soft image does not sharpen it. Feeding the clay-style concept as the reference for the sheet kept its chunky cartoon forms (A/B run, Bilbo and spider). Generate the sheet from words, or from a reference that already has crisp detail (the painted Gollum concept worked).
- Check every tile before spending on 3D: it must be a flat elevation of the side it names, and the views must differ the way the part's sides differ. Never send near-identical views: three almost-identical elevations of a shop block came back as a single flat facade slab (Christmas village). When a tile fails, regenerate the sheet; dropping the tile lets the generator invent that side.
- The sheet costs detail. At a 1024 px sheet each tile is 512 px, and fine detail suffered (smoother bark, partly garbled knotwork). When both fine detail and footprint matter, run the single view and the sheet (one extra 3D task) and pick from clay renders, or take the footprint from the sheet's mesh.
- For a figure that must match an approved concept (Gollum), use the concept as the sheet's reference and confirm pose and composition survived before generating 3D: the sheet can drift (Gollum's rocks and back changed).

## Scale before printing

Raw generator output is in arbitrary units (standing figures have come in about 1.9 units tall, other subjects 1.2 to 1.8). Before any fit or print check, run the boxes' [`glb_to_print.py`](../../families/printable-container/scripts/glb_to_print.py): Z-up, feet on the plate, scale to the target height (for example 32 mm tabletop, or the box's figure height), optional flat-bottom cut and round base, STL out. Raw meshes are often not watertight; repair as in [moving parts and figures](../../families/printable-container/references/moving-parts-and-figures.md) before booleans.

## Judge with real renders

- Compare candidates with the boxes' [`render_closeups.py`](../../families/printable-container/scripts/render_closeups.py) (neutral grey Cycles, same height, front / three-quarter / back / top plus close-ups of the fine-detail areas: face, hands, buckles, emblems, fur) or in the slicer preview.
- Don't judge from a point-cloud render or a numeric smoothness score. A quick point cloud made a real improvement look like a tie, and in the A/B run a smoothing-displacement metric ranked the chunky clay figures higher because it measures big soft forms, not crisp edges.

## Invented hidden mass

Image-to-3D invents every side the input doesn't show. Gollum's Cave roof corners came out 126 mm deep against about 45 mm in the art, and the Christmas village roof came back as an L-shaped cross gable with an empty back quadrant. Before fitting, render the raw mesh from the views the art doesn't show (back, underside, the far corner) and compare its footprint and topology with the art. If the hidden side is wrong, regenerate it or trim only the invented mass and re-check the approved properties. A mirror repair copies one side's detail onto the others, which costs the part its variety, so record it as a fidelity loss.

## Cost

A two-arm test on three subjects cost about 180 credits. Track spend in a ledger beside the outputs and state the cost before large spends. For budget splits across concepts, art, meshes and reserve, see the [art pipeline](../concept-and-faithfulness/art-pipeline.md#spending) and the generated-scene-diorama skill.
