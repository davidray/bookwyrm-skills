# Modeling and evidence

## Source-scene organization

Use explicit collections or equivalent layers for:

- production frame and structural parts;
- production lithophane panels;
- functional reserves, keep-outs, motion, and service paths;
- presentation-only artwork, glow, lights, backgrounds, and comparison staging.

Name objects by role and face. Store important dimensions and assumptions in scene properties or a sidecar geometry-facts file. Save the authoritative editable source before transforms used only for exploded views.

When scripts generate or revise the model, keep dimensions centralized and outputs versioned. Pass input and output paths as arguments; do not hard-code machine-specific paths such as `/mnt/project-files/...` in generators that will be locked into a release. Do not overwrite a David-approved source; branch or version the changed system.

## Generated and imported meshes

Treat an AI-generated or downloaded mesh as untrusted geometry. First inspect bounds, units, triangle count, normals, non-manifold edges, disconnected parts, degeneracy, and whether apparently open bays are actually capped by membranes.

A watertight decorative mesh can still be useless as a lantern because it has no real openings, wall plan, panel seats, service path, or printable segmentation. Once David has approved a part's mesh, though, keep it as the visible exterior and add the function into it: hollow it, cut slots, seats, bays and lid pockets, and add hidden internals. Do not separate what the art joins (Dragon: cutting the dragon off its mountain caused holes and split limbs; keeping one hollowed piece worked). Record which surfaces are preserved, cut, or added.

### Fitting a part without deforming it

- **Scale uniformly.** Never stretch carved or organic detail along one axis: stretched roots became plates and a stretched diamond boss read as broken. Earlier non-uniform fits (a 1.15× plan-only plinth stretch, compressed frame bands) predate this rule and are not precedents.
- **Change length by modules or bands.** Repeat a repeating module (a column's diamond panel, 3 to 5 per face) or remove plain horizontal bands from the middle of stone rows so each stone keeps its own edges. Inserting a straight band is allowed only where the profile is genuinely constant along the axis (a plain shaft section of a turned post), measured by sections; record the band's position and length, and show the result close up so David can see no plain stretched section reads (Lake-town: a 37 mm band at the posts' flat baluster section).
- **Cover a neighbour with a pocket.** When a part must sit over another (a roof over the body like a lid), scale it uniformly and cut a pocket so the neighbour nests inside.
- **Sink and subtract at contacts.** Where decor meets another part, sink it into the neighbour and boolean-subtract the neighbour. That gives exact glue faces without changing the decor's shape.
- **Move rigidly, don't fill.** To close a gap, move the art onto its neighbour (in rigid slices along a path if it must follow a surface) rather than growing filler geometry.
- **Trim only true blockers.** Remove only what blocks a window, a panel slot, a light box, or a lift path. After any trim, check that each named property the part owns is still there and still has its character (a trim once deleted a hanging lantern). Never cut a pointed form flat: taper it or shorten it to a point.
- **Make hanging and pendant decor separate parts** (a hanging lantern, keys, a pendant sign), pinned or glued in place. On Gollum's Cave, a pendant at the lowest point lifted the roof slab about 120 mm and made the roof 72% support. Fringes print best as separate strips with the tips up (the Christmas village icicles).
- **Split by the art's own pieces when a part must be placed in parts** (trunk, limbs, crown), and map each piece rigidly. Paths that must follow an exact line (a branch arch) can be made by sweeping a length of the art's own surface along it.

### Working with generated meshes

- Raw generator output is in arbitrary units (about 1 to 2 units tall so far). Before any review or fit, scale it uniformly to the part's real size from the blockout, set it Z-up with its base on z = 0, and record the scale factor.
- Pull the full-resolution source for each region you need instead of one decimated copy of the whole model (a trunk went from 11k to 252k triangles).
- When geometry cannot separate two materials (flame from rock, leaf from bark), segment by colour: a retexture of the same model, or the mean texture colour of each UV chart.
- Generated meshes are often open, hollow skins with internal shells. Make them solid by voxel close, fill, and an inset core unioned with the skin, or by generalized winding numbers (libigl) on open or boolean-damaged meshes, then marching cubes. Avoid mesh smoothing plus decimation, which leaves needles and holes; smooth the voxel field instead. Canopies and domes need a solid core under the surface. Voxel size, smoothing and decimation all round off fine tips and thin edges. Compare close-ups of the finest features before and after, and use a smaller voxel for parts with points.

### Boolean and export checks

- After every boolean, confirm each operand is still present and changed the result. Booleans can fail silently (two roof beams vanished; an EXACT boolean did nothing). Retry with another solver and re-check.
- Keep blockout placeholders out of production collections and exports; a placeholder box once shipped as the roof.
- Compare each export's volume, bounds, and shell count with the previous version. Reject an empty or near-empty export.

## Review views

Keep cameras stable across revisions. Use matched framing when comparing to concept art, and put the approved concept or part art on the same sheet as the model. For a part, use a three-up: approved art, textured model, bare geometry. Show the raw generated model before any fitting, and give lids and roofs top and underside views. Provide neutral production-only views so shallow geometry cannot hide behind paint or texture. Add grazing-light or orthographic closeups for relief that is difficult to read. White-on-white clay hides flat planes and shallow steps, so every review sheet gets a contrast-boosted or curvature-shaded view as well. In the Christmas village mini, four flat boxes in the roof were invisible in plain clay until David spotted them. When comparing meshes (two generations, or an A/B test of inputs), render real meshes in Blender or a slicer: a neutral clay material at true scale, the same cameras for every candidate, front, side and top orthographic views for shape and footprint, and grazing-light close-ups of the finest detail areas. A point-cloud or thumbnail preview made a clear improvement look like a tie. Measure footprint depth and width, not only height.

Functional evidence should show:

- installed state;
- cutaway through the light and panel system;
- exploded assembly and actual motion directions;
- underside or service access;
- isolated panel seats and retention;
- print layout or segmentation when relevant.

Color functional reserves distinctly and label them as non-production. Do not let them appear as if they are printed components.

## Evidence freshness

See [evidence and claims](../../../shared/evidence-and-claims/evidence-and-claims.md#evidence-freshness) (`shared/evidence-and-claims/evidence-and-claims.md`): bind review packets to the current geometry, and keep the lit render and the neutral geometry packet both.
