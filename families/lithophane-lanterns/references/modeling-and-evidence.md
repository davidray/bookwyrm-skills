# Modeling and evidence

## Source-scene organization

Use explicit collections or equivalent layers for:

- production frame and structural parts;
- production lithophane panels;
- functional reserves, keep-outs, motion, and service paths;
- presentation-only artwork, glow, lights, backgrounds, and comparison staging.

Name objects by role and face. Store important dimensions and assumptions in scene properties or a sidecar geometry-facts file. Save the authoritative editable source before transforms used only for exploded views.

When scripts generate or revise the model, keep dimensions centralized and outputs versioned. Avoid hard-coded machine-specific paths in reusable generators. Do not overwrite a user-approved source; branch or version the changed system.

## Generated and imported meshes

Treat an AI-generated or downloaded mesh as untrusted geometry. First inspect bounds, units, triangle count, normals, non-manifold edges, disconnected parts, degeneracy, and whether apparently open bays are actually capped by membranes.

A watertight decorative mesh can still be useless as a lantern because it has no real openings, wall plan, panel seats, service path, or printable segmentation. Use it as a visual foundation while rebuilding the functional architecture deliberately. Record which surfaces are preserved, reconstructed, or discarded.

## Review views

Keep cameras stable across revisions. Use matched framing when comparing to concept art. Provide neutral production-only views so shallow geometry cannot hide behind paint or texture. Add grazing-light or orthographic closeups for relief that is difficult to read.

Functional evidence should show:

- installed state;
- cutaway through the light and panel system;
- exploded assembly and actual motion directions;
- underside or service access;
- isolated panel seats and retention;
- print layout or segmentation when relevant.

Color functional reserves distinctly and label them as non-production. Do not let them appear as if they are printed components.

## Evidence freshness

Bind important review packets to the current source and export identities, using hashes when the workflow warrants it. Geometry edits invalidate evidence that depicts or measures the old geometry. Evidence-only rerenders may preserve the geometry identity but should still be versioned and declared as such.

An attractive lit render and a neutral geometry packet answer different questions; retain both. A user visual approval applies only to the identified revision and visible properties presented.
