# Tooling

Setup notes that cost time on earlier builds. Recheck versions before relying on them.

## Headless Blender and mesh tools in a cloud container

- Install with pip: `bpy` (matching the Blender version you target), `trimesh`, `libigl`, `manifold3d`, `scikit-image`, `scipy`, `Pillow`, `numpy`.
- Workbench renders fail until EGL is present: `apt-get install -y libegl1`.
- Lake-town v1 (`lanterns/lake-town/v1/source/`) has working examples: blockout and clash check, raw-mesh inspection, winding-number solidify, print booleans with manifold3d, 3MF writing from the solver's own indexing, review sheets.

## Slicing with the Bambu Studio CLI (macOS)

Bambu Studio 2.8.2's CLI does not resolve stock presets the way the app does:

- Flatten each preset's `inherits` chain into one JSON before passing it (`lanterns/lake-town/v1/source/slice/flatten.py`).
- Give the filament and process presets an explicit `compatible_printers` list that names the machine preset.
- Slice bed-centred copies of each 3MF (`oncentre.py`); off-centre parts can be rejected.
- `slice_all.sh` and `slice_all.log` in the same folder show a full run. Read the result, not only the return code (see validation and release), and use `gcode_view.py` to project supports onto the part.
