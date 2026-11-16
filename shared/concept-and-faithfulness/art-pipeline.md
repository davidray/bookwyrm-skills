# Dave's art pipeline

Use this in every family when generating concept art, part art, panel art, or AI meshes. It records tools and habits, not product design; recheck tool availability and prices before relying on them. It grew out of the lanterns, so its examples are mostly lanterns.

## Tools (as of 2026-11-05)

- 3D meshes come from the 3D generator; [image to 3D](../image-to-3d/image-to-3d.md) names the engines, how a build calls them and their prices. Image models used for art and 3D input: nano-banana-pro (image-to-image, text-to-image) and gpt-image-2.5-flare. Read keys at run time; never write them to a file, log, checkpoint, or the repository.
- The OpenAI image route through bookwyrm-rpg had run out of credits on 2026-11-04; check before using it.
- Working files for lanterns live on the Mac in `~/code/bookwyrm-rpg-lantern-art/<lantern>/`. Copy what reviews need into the project folder; large meshes stay on the Mac and are referenced by path and task ID. Anything David should see goes to The Hoard as a draft (see the workshop skill).
- Blender scenes edited on the Mac are not saved automatically. Export approved work to files (GLB or STL) before moving on, and say when a scene is unsaved.

## Spending

- Ask before each spend, with the estimated cost, and cap it. A device-side permission check may require the user's approval in the same thread.
- Record task IDs, credits spent, and the balance in the checkpoint.
- Per-call prices are in [image to 3D](../image-to-3d/image-to-3d.md#engines-and-prices). The split below uses rough Meshy-era numbers (about 9 per image, 20 per mesh); rescale it to the current engine's prices.
- Read the live balance before the first spend; checkpoint balances go stale.
- With a fixed budget, plan the split before spending. For a 200-credit lantern with three decor parts and four panels: concepts about 20, part art about 60 (two rounds), image-to-3D about 60, panel art about 40, reserve about 20. Stop and re-plan when the reserve can no longer cover one part retry (new art plus new 3D, about 29).
- Scale the split with the part count. Add about 20 for art and 20 for 3D for each decor part beyond three. If that leaves no reserve, cut or merge parts first, and never cut the reserve. Tests 2 and 3 both started with a reserve of 14 or less.
- Make panel art as one 2×2 grid image by default (9 credits, and the set comes out in one style). Four separate images cost 36 and give more pixels than the printer can draw (see the detail limits in [lithophanes](../lithophanes/lithophanes.md#detail-limits)). Buy them only when one grid tile gives fewer than about 3 px per mm of panel field.

## What works

- **Part art to 3D.** Image-to-3D is faithful when the part is shown alone, centred, on a plain backdrop, with the whole part in frame. Ask for geometry only unless colour is needed to segment materials. The painted part art is the approval image. The image sent to 3D is made from it (next section).
- **Variants.** Image-to-image from an approved part image keeps style, camera, and backdrop. Use it for siblings that change only the dressing (Mirkwood trees: fungus, ivy, spider web, moss).
- **New compositions need a fresh start.** Image-to-image and edit passes keep the reference's layout: they came back nearly identical when a composition had to change (Dragon a2, a3, d2; the Bag End party scene, which kept Bilbo outside). Use text-to-image with no reference image instead.
- **Colour for segmentation.** A retexture of the same model gives colours that separate materials geometry cannot (Dragon flame from rock). Geometry-only output can be retextured later.
- **Image-to-image ignores numbers.** It keeps the look but not stated ratios or widths (Lake-town part art missed its proportions twice with explicit numbers). For a part whose proportions matter, give it a reference whose silhouette already has the right ratio (a blockout render or a rough proportion sketch), describe the shape in words ("twice as tall as wide, plank wall around a tall window") rather than numbers, and measure the result before 3D.
- **Aspect ratios.** nano-banana-pro has no 2:3 option; generate 3:4 and crop, or use a GPT image model.
- **Panel art briefs.** Never use the word "lithophane" in an image prompt; it returns photos of lit lithophanes with frames, hands, and text. Ask for a flat, full-bleed illustration with no frame, border, text, or hands, and use one shared style line for all panels in the set. Large calm tonal shapes, brightest values in sky and light sources, darkest in silhouettes, nothing important smaller than about 1/12 of the image width, no text, focal content clear of the frame mask. Ask for tonal washes and bold silhouettes, not fine hatching, engraving or line work: lines that fine print narrower than the nozzle can draw. Avoid scenes that are mostly near-white, such as wide snowfields, or give them a mid-tone ground. Generated images often paint their own arch or disc on grey; mask it before relief.

## The 3D input image and invented hidden mass

See [image to 3D](../image-to-3d/image-to-3d.md): draw the input as a sculpt, use a four-view sheet when shape matters, scale before judging, and check the sides the art doesn't show.

## Review habits the user relies on

- Show the raw generated model before any fitting.
- Put the approved art beside every model render.
- Check generated art for story errors as well as tone (who is inside or outside, which way a figure faces).
