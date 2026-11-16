# Moving parts and sculpted figures

Read this before designing a hinge, a rotating lid or any print-in-place mechanism, or before building a container around a sculpted figure. The lessons come from the Gollum ring box (`projects/gollum-ring-box/`).

## Print-in-place mechanisms

- Test the mechanism on its own first. A two-hour print of the sphere and hinge alone proved the lid would break free before a day-long figure print.
- Starting gaps that worked on the X2D in PLA at 0.12 mm layers:

| Gap | Value | Note |
| --- | --- | --- |
| Lid-to-bowl seam | 0.5 mm | 0.4 mm fused lightly and needed a knife along the lip |
| Pivot pin, radial | 0.4 mm | Pointed or teardrop-top hole so it prints without support |
| Hub to pocket | 0.5 mm | Through the whole swing |
| Any part bridging over the moving part | 1.2 mm | Fingertips, lips and chin printed over air and may sag a little |

- Check clearance through the whole motion, sampled every few degrees, not only at open and closed. The Gollum hub gap shrank to 0.15 mm at mid-swing, where a flat pocket floor met the round hub, and made the lid stiff. A full round pocket fixed it.
- Give the motion a hard stop, and check zero interference over its full range.
- Make every trapped ceiling self-supporting: 45 degree cones under cores, pointed lid ceilings, teardrop holes. In the slicer, add a support blocker filling the cavity so no support is built between the moving parts.
- Magnets can't be glued into a one-piece print. Use a counterweight (Gollum's weighted front edge), a printed catch, or a print pause to drop them in.
- Write how to free the part in the print guide: cool fully, run a knife along the seam and over any bridged features, then move it gently to its stop.

## Sculpted figures

- Generate the figure with the 3D generator from a resin-sculpt turnaround sheet (front, left, back, right at one scale) through its multi-view call; see [image-to-3D input](../../../shared/image-to-3d/image-to-3d.md). With a single image, use a padded crop of the whole figure; padding stops it flat-cutting the edges. Procedural, part-by-part sculpting looked cartoonish and was dropped.
- Remove fragile or unwanted detail rather than thicken it. David removed the sculpted hair (fake hair is glued on after printing) and the teeth. An SDF opening (Mesh to SDF Grid, offset inward then outward by the same radius, Grid to Mesh) followed by masked Laplacian smoothing does this cleanly.
- The figure grows out of its base. Don't clip rocks or terrain flat; Gollum's back runs down into the rock.
- Size the mechanism to the generated mesh rather than shrinking the figure (the sphere went from 60 to 66 mm to match the generated ball). Leave about 0.5 mm between the figure and a moving part it touches, more where it bridges over it.
- Large meshes: merge doubles first (Meshy imports are split into UV islands; Tripo output may differ; note what you find in [image to 3D](../../../shared/image-to-3d/image-to-3d.md)), decimate to about 2 M triangles, fix non-manifold edges, and use Blender's Manifold boolean solver for the final joins. Bond a fused part through a deliberate contact patch, not incidental touching.
- Generated eyes come back as smooth balls; plan to paint the iris.
- Track credits and state the cost before large spends.

## Material and print time

- Don't hollow a model to save filament on FDM. The slicer already prints walls plus sparse infill; a hollow model adds a second set of walls and an unsupported roof, and often uses more plastic.
- To save filament, use Lightning infill at 5 to 8% and 2 walls, with normal settings over the height range of hinges and mechanisms. Give a filament estimate in the guide and tell the user to trust the slicer's figure.
