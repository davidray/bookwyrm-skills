# Art pipeline

Use this in every family when generating concept art, part art, panel art, or AI meshes. It records tools and habits, not product design; recheck tool availability and prices before relying on them. It grew out of the lanterns, so its examples are mostly lanterns.

## Tools

- 3D meshes come from the 3D generator; [image to 3D](../image-to-3d/image-to-3d.md) (`shared/image-to-3d/image-to-3d.md`) names the engines, how a build calls them and their prices. Image models used for art and 3D input: nano-banana-pro (image-to-image, text-to-image) and gpt-image-2.5-flare. Read keys at run time; never write them to a file, log, checkpoint, or the repository.
- Check the OpenAI balance before using the OpenAI image route through bookwyrm-rpg; it has run out before.
- Working files for lanterns live on the Mac in `~/code/bookwyrm-rpg-lantern-art/<lantern>/`. Copy what reviews need into the project folder; large meshes stay on the Mac and are referenced by path and task ID. Anything David should see goes to The Hoard as a draft (see the workshop skill).
- Blender scenes edited on the Mac are not saved automatically. Export approved work to files (GLB or STL) before moving on, and say when a scene is unsaved.

## Spending

- Spend inside the build's approved budget without asking for each call, and ask only to raise it (`workshop` skill, section 1). Work under a cap set to that budget. A device-side permission check may still need David's approval in the same thread.
- Prices and how each engine is called are in [image to 3D](../image-to-3d/image-to-3d.md#engines-and-prices) (`shared/image-to-3d/image-to-3d.md`). Read the live balance before the first spend; checkpoint balances go stale. Record task IDs and credits spent in the ledger and checkpoint.
- With a fixed budget, plan the split before spending: for a lantern with three decor parts and four panels, roughly 10% concepts, 30% part art (two rounds), 30% image to 3D, 20% panel art and 10% reserve. Add art and 3D for each extra decor part. If that leaves no reserve, cut or merge parts first; never cut the reserve. Stop and re-plan when the reserve can't cover one part retry (new art plus new 3D).
- Make panel art as one 2×2 grid image by default: one image instead of four, and the set comes out in one style. Four separate images give more pixels than the printer can draw (see [detail limits](../lithophanes/lithophanes.md#detail-limits), `shared/lithophanes/lithophanes.md`). Buy them only when one grid tile gives fewer than about 3 px per mm of panel field.

## What works

- **Part art to 3D.** Image-to-3D is faithful when the part is shown alone, centred, on a plain backdrop, with the whole part in frame. Ask for geometry only unless colour is needed to segment materials. The painted part art is the approval image. The image sent to 3D is made from it (next section).
- **Variants.** Image-to-image from an approved part image keeps style, camera, and backdrop. Use it for siblings that change only the dressing (Mirkwood trees: fungus, ivy, spider web, moss).
- **New compositions need a fresh start.** Image-to-image and edit passes keep the reference's layout: they came back nearly identical when a composition had to change (Dragon a2, a3, d2; the Bag End party scene, which kept Bilbo outside). Use text-to-image with no reference image instead.
- **Colour for segmentation.** A retexture of the same model gives colours that separate materials geometry cannot (Dragon flame from rock). Geometry-only output can be retextured later.
- **Two failed edits, then change approach.** When two image generations or edits in a row fail the same correction, however the prompt was worded, stop sending edits for it: a third try of the same kind fails the same way (the wizard tower's wyrm failed edits r4, r5 and r6; a hand retouch fixed it). Change the kind of approach: retouch the image by hand (clone, paint over, composite from an approved image), start fresh with text-to-image, give the model a reference that already shows the fix, or ask David to accept, defer or sketch the feature. A new kind of approach gets two tries of its own. Tell David at the next gate which correction failed twice and what you switched to.
- **The reference outranks the prompt.** When a reference image shows a detail the prompt asks to change, the model copies the reference (the celestial trinket box's rune ring came back as the concept's fine, real-alphabet runes twice, after two prompts asking for bold invented ones). Before the call, mask or paint the detail out of the reference, or give a reference that already shows the change; for a detail that will be scripted anyway (runes, beads, stars), treat what comes back as a placeholder and don't spend tries on it.
- **Image-to-image ignores numbers.** It keeps the look but not stated ratios or widths (Lake-town part art missed its proportions twice with explicit numbers). For a part whose proportions matter, give it a reference whose silhouette already has the right ratio (a blockout render or a rough proportion sketch), describe the shape in words ("twice as tall as wide, plank wall around a tall window") rather than numbers, and measure the result before 3D.
- **Aspect ratios.** nano-banana-pro has no 2:3 option; generate 3:4 and crop, or use a GPT image model.
- **Panel art briefs.** Never use the word "lithophane" in an image prompt; it returns photos of lit lithophanes with frames, hands, and text. Ask for a flat, full-bleed illustration with no frame, border, text, or hands, and use one shared style line for all panels in the set. Large calm tonal shapes, brightest values in sky and light sources, darkest in silhouettes, nothing important smaller than about 1/12 of the image width, no text, focal content clear of the frame mask. Ask for tonal washes and bold silhouettes, not fine hatching, engraving or line work: lines that fine print narrower than the nozzle can draw. Avoid scenes that are mostly near-white, such as wide snowfields, or give them a mid-tone ground. Generated images often paint their own arch or disc on grey; mask it before relief.

## The 3D input image and invented hidden mass

See [image to 3D](../image-to-3d/image-to-3d.md) (`shared/image-to-3d/image-to-3d.md`): draw the input as a sculpt, use a four-view sheet when shape matters, scale before judging, and check the sides the art doesn't show.

## Review habits David relies on

- Show the raw generated model before any fitting.
- Put the approved art beside every model render.
- Check generated art for story errors as well as tone (who is inside or outside, which way a figure faces).
