# Tooling

Setup notes that cost time on earlier builds. Recheck versions before relying on them.

## Headless Blender and mesh tools in a cloud container

- Install with pip: `bpy` (matching the Blender version you target), `trimesh`, `libigl`, `manifold3d`, `scikit-image`, `scipy`, `Pillow`, `numpy`.
- Workbench renders fail until EGL is present: `apt-get install -y libegl1`.
- Lake-town v1 (`lanterns/lake-town/v1/source/`) has working examples: blockout and clash check, raw-mesh inspection, winding-number solidify, print booleans with manifold3d, 3MF writing from the solver's own indexing, review sheets.
- Gollum's Cave v1 (`lanterns/gollums-cave/v1/source/`) adds fit and engineering scripts (`parts/prep_parts.py`, `parts/assemble_review.py`, `print/engineer.py`, `print/make_skins.py`). The checks in them (shell count, volume sign, engagement, window shadow on a face) caught most of that run's corrections. Start from these rather than writing new checks.

## Slicing with the Bambu Studio CLI (macOS)

Bambu Studio 2.8.2's CLI does not resolve stock presets the way the app does:

- Flatten each preset's `inherits` chain into one JSON before passing it (`lanterns/lake-town/v1/source/slice/flatten.py`).
- Give the filament and process presets an explicit `compatible_printers` list that names the machine preset.
- Slice bed-centred copies of each 3MF (`oncentre.py`); off-centre parts can be rejected.
- `slice_all.sh` and `slice_all.log` in the same folder show a full run. Read the result, not only the return code (see validation and release), and use `gcode_view.py` to project supports onto the part.

## Painting guides and renders

- **Painting guides** (Gift stable, Doré, Lonely Mountain, 2026-11-20): illustrated priming and painting PDFs rendered from the locked print 3MFs with pip `bpy` (Cycles CPU; Workbench and EEVEE fail headless), per-vertex masks (paint colour, red keep-clear, amber hidden) computed with trimesh, HTML to PDF with Playwright Chromium. Only describe geometry that exists in the print files (Lonely Mountain's roof cornice has no knotwork on its back side). Each guide is stored in its piece as `docs/painting-guide.pdf`. The Doré scripts are on the Mac in `~/code/bookwyrm-rpg-lantern-art/project-archive/gustave-dore-painting/source/` (`asm.py` holds the print-to-assembly transforms); start a new guide from them.
- **Home-library renders** use `shared/blender-tooling/render-home/`. The lit front three-quarter render is each piece's cover; Gollum's Cave stays out of the catalogue's public view (David, 2026-11-15).
