# Dave's art pipeline

Use this for Dave's lantern projects when generating concept art, part art, panel art, or AI meshes. It records tools and habits, not lantern design; recheck tool availability and prices before relying on them.

## Tools (as of 2026-11-05)

- Image and 3D generation run through Meshy from the user's Mac, via the Blender MCP or the Meshy MCP server. Image models used: nano-banana-pro (image-to-image, text-to-image) and gpt-image-2.5-flare. 3D: image-to-3D (meshy-7.1 or latest), and retexture.
- The OpenAI image route through bookwyrm-rpg had run out of credits on 2026-11-04; check before using it.
- Generated files live on the Mac in `~/code/bookwyrm-rpg-lantern-art/<lantern>/`. Copy what reviews need into the project folder; large meshes stay on the Mac and are referenced by path and task ID.
- Each Meshy tool needs a Claude Code permission rule in the Mac session (for example `mcp__meshy-mcp-server__meshy_text_to_image`). The user adds it; give them the exact rule text rather than changing permissions yourself.
- Blender scenes edited on the Mac are not saved automatically. Export approved work to files (GLB or STL) before moving on, and say when a scene is unsaved.

## Spending

- Ask before each spend, with the estimated cost, and cap it. A device-side permission check may require the user's approval in the same thread.
- Record task IDs, credits spent, and the balance in the checkpoint.
- Rough costs seen: about 9 credits per image, about 20 per image-to-3D, 10 per retexture.

## What works

- **Part art to 3D.** Image-to-3D is faithful when the part is shown alone, centred, on a plain mid-grey backdrop, in a three-quarter view from slightly above. Ask for geometry only unless colour is needed to segment materials.
- **Variants.** Image-to-image from an approved part image keeps style, camera, and backdrop. Use it for siblings that change only the dressing (Mirkwood trees: fungus, ivy, spider web, moss).
- **New compositions need a fresh start.** Image-to-image and edit passes keep the reference's layout: they came back nearly identical when a composition had to change (Dragon a2, a3, d2; the Bag End party scene, which kept Bilbo outside). Use text-to-image with no reference image instead.
- **Colour for segmentation.** A retexture of the same model gives colours that separate materials geometry cannot (Dragon flame from rock). Geometry-only output can be retextured later.
- **Panel art briefs.** Large calm tonal shapes, brightest values in sky and light sources, darkest in silhouettes, nothing important smaller than about 1/12 of the image width, no text, focal content clear of the frame mask. Generated images often paint their own arch or disc on grey; mask it before relief.

## Review habits the user relies on

- Show the raw generated model before any fitting.
- Put the approved art beside every model render.
- Check generated art for story errors as well as tone (who is inside or outside, which way a figure faces).
