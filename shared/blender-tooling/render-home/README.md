# Home-library lantern renders

Blender (bpy 5.x, Cycles on CPU) scripts that assemble a lantern from its locked print files and render it lit in a home library. They made `lanterns/<slug>/renders/home-library-v1/` (2026-11-15).

## Run
```sh
python -m venv venv && venv/bin/pip install bpy numpy scipy pillow
ROOM_ASSETS=<assets folder> venv/bin/python scene.py -- specs/<slug>.json front34,back34,close,wide 48 1440x960 <out dir>
```
`batch.sh` runs every lantern. Each render takes about 5 minutes on 4 CPU cores. The specs hold absolute paths from the working session: this repo was at `/home/user/bookwyrm-lanterns`, and a few `ref` STLs come from the project's shared files. Adjust both to run elsewhere.

## Files
- `tmf.py`: reads a 3MF (build and component transforms applied) or an STL.
- `lantern.py`: places each print part in lantern coordinates from a spec. It uses a centre or a reference STL bounding box, rotations, a 4×4 matrix (Christmas village icicle strips), a wedge solve for pie-cut sectors (Doré plinth and body sixths), and rotated copies.
- `lithomat.py`: the lithophane material. It rasterises each panel's own relief into a thickness texture, and transmits `exp(-k (t - 0.8))` with k = 1.0/mm through a translucent BSDF (shadow rays see the same value). Flat panels, square skin tubes (Gollum's Cave) and constant-thickness skins (Dragon flame) are handled.
- `room.py`: the library. Floor, walls, wainscot and rug are Poly Haven CC0 textures. Bookshelves, chair, tables and props are Poly Haven CC0 models. The books are procedural.
- `scene.py`: lights, the four cameras, and render settings. The LEDs are point lights along each strip.
- `specs/*.json`: one per lantern, with every part's placement and its source for it in the lantern's README or facts files.

The room assets are not in the repo. They are in David's `bookwyrm-rpg-lantern-art/renders-v1/assets/` (Poly Haven blocks the cloud proxy, so they were downloaded through Blender on the Mac).
