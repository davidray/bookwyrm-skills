# Dave's art pipeline

Use this for Dave's lantern projects when generating concept art, part art, panel art, or AI meshes. It records tools and habits, not lantern design; recheck tool availability and prices before relying on them.

## Tools (as of 2026-11-05)

- 3D meshes come from the 3D generator (the `3d-generator` skill names the current engine, how to call it and its prices). Image models used for art and 3D input: nano-banana-pro (image-to-image, text-to-image) and gpt-image-2.5-flare; their routes are in the same skill. Read keys at run time; never write them to a file, log, checkpoint, or the repository.
- The OpenAI image route through bookwyrm-rpg had run out of credits on 2026-11-04; check before using it.
- Generated files live on the Mac in `~/code/bookwyrm-rpg-lantern-art/<lantern>/`. Copy what reviews need into the project folder; large meshes stay on the Mac and are referenced by path and task ID.
- Blender scenes edited on the Mac are not saved automatically. Export approved work to files (GLB or STL) before moving on, and say when a scene is unsaved.

## Spending

- Ask before each spend, with the estimated cost, and cap it. A device-side permission check may require the user's approval in the same thread.
- Record task IDs, credits spent, and the balance in the checkpoint.
- Per-call prices are in the `3d-generator` skill. The split below uses rough Meshy-era numbers (about 9 per image, 20 per mesh); rescale it to the current engine's prices.
- Read the live balance before the first spend; checkpoint balances go stale.
- With a fixed budget, plan the split before spending. For a 200-credit lantern with three decor parts and four panels: concepts about 20, part art about 60 (two rounds), image-to-3D about 60, panel art about 40, reserve about 20. Stop and re-plan when the reserve can no longer cover one part retry (new art plus new 3D, about 29).
- Scale the split with the part count. Add about 20 for art and 20 for 3D for each decor part beyond three. If that leaves no reserve, cut or merge parts first, and never cut the reserve. Tests 2 and 3 both started with a reserve of 14 or less.
- Make panel art as one 2×2 grid image by default (9 credits, and the set comes out in one style). Four separate images cost 36 and give more pixels than the printer can draw (see the detail limits in panels and optics). Buy them only when one grid tile gives fewer than about 3 px per mm of panel field.

## What works

- **Part art to 3D.** Image-to-3D is faithful when the part is shown alone, centred, on a plain backdrop, with the whole part in frame. Ask for geometry only unless colour is needed to segment materials. The painted part art is the approval image. The image sent to 3D is made from it (next section).
- **Variants.** Image-to-image from an approved part image keeps style, camera, and backdrop. Use it for siblings that change only the dressing (Mirkwood trees: fungus, ivy, spider web, moss).
- **New compositions need a fresh start.** Image-to-image and edit passes keep the reference's layout: they came back nearly identical when a composition had to change (Dragon a2, a3, d2; the Bag End party scene, which kept Bilbo outside). Use text-to-image with no reference image instead.
- **Colour for segmentation.** A retexture of the same model gives colours that separate materials geometry cannot (Dragon flame from rock). Geometry-only output can be retextured later.
- **Image-to-image ignores numbers.** It keeps the look but not stated ratios or widths (Lake-town part art missed its proportions twice with explicit numbers). For a part whose proportions matter, give it a reference whose silhouette already has the right ratio (a blockout render or a rough proportion sketch), describe the shape in words ("twice as tall as wide, plank wall around a tall window") rather than numbers, and measure the result before 3D.
- **Aspect ratios.** nano-banana-pro has no 2:3 option; generate 3:4 and crop, or use a GPT image model.
- **Panel art briefs.** Never use the word "lithophane" in an image prompt; it returns photos of lit lithophanes with frames, hands, and text. Ask for a flat, full-bleed illustration with no frame, border, text, or hands, and use one shared style line for all panels in the set. Large calm tonal shapes, brightest values in sky and light sources, darkest in silhouettes, nothing important smaller than about 1/12 of the image width, no text, focal content clear of the frame mask. Ask for tonal washes and bold silhouettes, not fine hatching, engraving or line work: lines that fine print narrower than the nozzle can draw. Avoid scenes that are mostly near-white, such as wide snowfields, or give them a mid-tone ground. Generated images often paint their own arch or disc on grey; mask it before relief.

## The 3D input image

The input image decides the mesh's detail. The generator already makes 1–2 M faces, and higher-resolution input, 2k mode and polycount settings barely change the result: the mesh copies what is drawn, so soft input gives soft output (David's tests, 2026-11-06, Meshy 7.1). The lantern A/B test (plinth, Lake-town roof, Mirkwood tree; `/mnt/project-files/meshy-input-ab/results.md`) set these defaults:

- **Draw the input as a sculpt.** After the painted part art is approved, make the 3D input by image-to-image from it with the same object and camera: "an unpainted grey resin miniature sculpt, uniform matte resin, no paint, no colour, no metal, every detail real sculpted relief, deep-cut carving, crisp sharp edges, clean sharp-edged surfaces, plain pale backdrop, high image quality, sharp focus, highly detailed", then name the part's specific fine detail (engraved knotwork strands, shingle edges, bark furrows, leaf lobes and veins). Paint and colour fake detail that has no relief behind it. This never made a part worse and clearly sharpened organic detail (the tree's leaves and bark).
- **Leave out wording that flattens detail.** No "nothing thinner than a pencil / matchstick", "nothing finer than 1.5 mm", "bold and chunky", "shallow printable recesses" or "softened points" in image prompts. Handle printability at fit and print time.
- **Use a four-view sheet when shape matters.** A single three-quarter image distorts depth: the tree came out 18% and the roof 7% slimmer front to back than the approved mesh. A front / right / back / left sheet in the same resin style, all views at the same scale, held the footprint within 1%. Ask for a two-by-two grid on one 1:1 canvas: top left front, top right right side, bottom left back, bottom right left side, flat elevations from the same slight height, no three-quarter views, the same size in every view, each view centred in its quarter with margin, no labels or grid lines. Crop the four tiles and send them to multi-image-to-3D with the front first. Check the sheet before spending on 3D: the first roof sheet drew three-quarter views at mixed sizes and had to be redone. Check every tile: it must be a flat elevation of the side it names, and the views must differ the way the part's sides differ. Never send near-identical views. Three almost-identical flat elevations of a shop block came back as a single flat facade slab, not a box (Christmas village). When a tile fails, regenerate the sheet. Dropping the tile lets the generator invent that side.
- **Know what the sheet costs.** At a 1024 px sheet each tile is 512 px, and fine detail suffered (smoother bark, partly garbled knotwork). When both fine detail and footprint matter, run the single view and the sheet (one extra 3D task) and pick from clay renders, or take the footprint from the sheet's mesh.
- **Scale before judging or printing.** Raw output is in arbitrary units. Scale uniformly to the real size, Z-up, base on the plate (see modeling and evidence), then compare in real clay renders with close-ups, never point-cloud previews.
- Endpoints, parameters and per-call costs for each engine are in the `3d-generator` skill.

## Invented hidden mass

Image-to-3D invents every side the input doesn't show. Gollum's Cave roof corners came out 126 mm deep against about 45 mm in the art. The Christmas village roof came back as an L-shaped cross gable with an empty back quadrant. Before fitting, render the raw mesh from the views the art doesn't show (back, underside, the far corner) and compare its footprint and topology with the art. If the hidden side is wrong, either regenerate it or trim only the invented mass and re-check the named properties (see workflow and gates). A mirror repair copies one side's detail onto the others, which costs the part its variety, so record it as a fidelity loss and budget per-face variation for it (signs, emblems, chimney placement).

## Review habits the user relies on

- Show the raw generated model before any fitting.
- Put the approved art beside every model render.
- Check generated art for story errors as well as tone (who is inside or outside, which way a figure faces).
