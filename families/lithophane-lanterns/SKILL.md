---
name: lithophane-lanterns
description: Design, model, test, and package 3D-printable LED lithophane (lithopane) lanterns with image-bearing translucent panels, serviceable lighting, and evidence-backed fit and release claims. Use for new lanterns, adaptations of visual or mesh references, panel and light-source redesigns, scale changes, print troubleshooting, and release review. Exclude open-flame lanterns and ordinary opaque lamps without lithophane panels.
---

# Lithophane lanterns

Create an illuminated object whose exterior, panels, light path, assembly, and print process work as one product. A convincing render is only visual evidence; a lithophane lantern succeeds when the printed panels read under the actual light, fit and remain retained, and the light can be installed, switched, and removed.

For a complete printable-product lifecycle, also apply `$printable-container`. This skill supplies the lantern-specific decisions and evidence that the general container workflow does not cover.

## Establish the real design inputs

Record before committing to architecture:

- authoritative concept or reference views and the visible properties to preserve;
- intended printer, nozzle, material, layer height, and maximum build volume when known;
- the exact low-voltage LED, tea light, cable, switch, controller, or battery envelope;
- panel count, artwork, viewing direction, target size, and whether panels must be removable;
- finish mode: single-color and hand-painted, multicolor, separate materials, or another explicit plan;
- service expectations, handling context, and the requested release level.

Use a battery-powered or otherwise low-voltage LED source. Exclude open flame. Do not infer hardware size, switch access, heat behavior, tolerances, hidden construction, or optical performance from concept art or a product label. If the physical light is available, measured dimensions outrank nominal packaging dimensions.

Read [workflow and gates](references/workflow-and-gates.md) for a new build or a material redesign. Read [engineering](references/engineering.md) before fixing dimensions, interfaces, segmentation, or orientation.

For Dave's lantern projects, read [Dave's lantern print profile](references/dave-print-profile.md) before selecting the build envelope, exterior feature sizes, segmentation, material, nozzle, or compatibility target. Treat that profile as a reusable equipment preference only; keep project-specific proportions, visual approvals, hardware, and exceptions in the project checkpoint.

## Select the lighting architecture

For Dave's lantern projects, record one of these standard lighting architectures before fixing the internal structure: **split lighting**, **puck light**, or **tea light**. Do not silently combine their assumptions.

- When **split lighting** is selected, read and apply [standard lighting architectures](references/standard-lighting-architectures.md). The named choice imports the established controller PCB, battery, four-chamber divider, and four-strip lighting topology as one baseline system.
- For **puck light** or **tea light**, model the actual selected light and its service envelope. Do not inherit the split-lighting PCB, battery, divider, or strip topology unless the user explicitly requests a hybrid.

Treat a standard architecture as a reusable starting system, not proof that it fits a new lantern. Preserve its locked interfaces and revalidate the lantern-specific optical spacing, divider fit, service path, heat behavior, and enclosure integration.

## Protect function before decoration

Block out these systems together:

1. actual light-source envelope and insertion/removal path;
2. switch, finger, cable, battery, and ventilation access as applicable;
3. light-to-panel spacing and any diffuser or hotspot-control volume;
4. lithophane panel field, thickness range, frame overlap, clearance, and extraction path;
5. structural frame, base, roof, retention, and intended print segmentation;
6. protected silhouette, focal forms, and decorative hierarchy.

Model clearance and motion reserves as named, visible non-production objects. Do not decorate over them or silently shrink them. A scale change is a redesign whenever it changes the protected hardware envelope, minimum printable features, panel thickness range, light spacing, or service access. Never uniformly scale a finished reference mesh and call the result engineered.

Keep lithophanes as separate replaceable parts by default. Integrate them only when the process and assembly plan make that deliberate. Give every panel a positive seat and retention strategy, plus a plausible assembly and replacement path. Mere intersection with a frame is not retention.

## Build panels as optical parts

Use actual image-derived relief for production panels. Textures, emission, and images mapped onto flat plates are presentation-only. Dark image regions normally become thicker and transmit less light; bright regions become thinner and transmit more. Confirm polarity with a rendered height preview or test strip before generating all panels.

Treat base thickness, relief range, image resolution, tonal curve, border, panel orientation, and light spacing as process-dependent parameters, not universal constants. Preserve important faces and silhouettes through crop and tonal preparation; avoid relying on tiny low-contrast details that disappear in transmitted light.

Read [lithophane panels and optics](references/panels-and-optics.md) whenever creating, replacing, resizing, or diagnosing panels.

## Keep evidence boundaries explicit

In Blender or another source model, separate at minimum:

- export-authoritative structure;
- export-authoritative lithophane geometry;
- functional/service reserves and motion paths;
- presentation-only artwork, materials, glow, and staging.

Use editable source geometry and repeatable generators where they improve reliability. Imported or AI-generated meshes may be visual foundations, reference components, or decorative donors; they are not functional lantern architecture until openings, load paths, panel seats, service paths, segmentation, and printable topology are deliberately rebuilt and verified.

Produce neutral production-only views as well as attractive lit views. A useful review packet normally includes a matched three-quarter view, front/elevation view, neutral geometry view, cutaway, exploded/service view, underside access view, and isolated panel previews. Show reserves only in functional views, with a clear legend.

Read [modeling and evidence](references/modeling-and-evidence.md) when building the source scene, adapting a generated mesh, or preparing review artifacts.

## Retire uncertainty with small physical tests

Use the cheapest representative coupon before a long print. Common coupons include:

- the actual light-source opening or carrier interface;
- panel channel, ledge, latch, or roof-capture cross-section;
- lithophane tonal/thickness strip under the intended LED and material;
- diffuser spacing and hotspot test;
- joint, roof key, detent, cable route, or support-removal sample.

Record the printer, material, orientation, slicer profile, nominal dimensions, measured result, and user verdict. A passing coupon locks only that interface under those conditions. If the physical result contradicts the model, redesign from the physical result and refresh every affected visual, dimensional, and audit artifact.

## Gate claims by evidence

Do not export or label a complete production set while a blocking interface remains only visual or assumed. Audit the actual exported meshes and sliced parts, not only the Blender scene. Inspect units, bounds, components, manifoldness, degeneracy, positive volume, gaps, orientation, supports, layer behavior, and round-trip import.

Keep optical, mechanical, visual, and release claims separate. A lit render does not prove transmission. A watertight mesh does not prove assembly. A successful slice does not prove fit. One fit ring does not qualify the entire lantern.

Read [validation and release](references/validation-and-release.md) before production export, print instructions, packaging, or any claim that files are ready to print or release.

## Deliver a durable project state

Maintain a checkpoint that identifies the active source, exact accepted decisions, protected interfaces, measured hardware, panel parameters, physical results, superseded files, open risks, current evidence level, and next unsatisfied gate. Preserve user-approved visual references and working branches; change locally rather than destructively replacing them.

For release, provide the editable source, production meshes, panel-to-face mapping, quantities, material and orientation guidance, assembly/service order, hardware requirements, tested and untested interfaces, safety boundary, validation results, and the highest supportable claim level. Avoid the unqualified label “print-ready.”
