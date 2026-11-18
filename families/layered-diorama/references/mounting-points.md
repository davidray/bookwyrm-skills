# Shaped mounting seats and assembly clearance

Use when mounting any character, prop, building, scenic element, or other object to a support such as terrain, a base, a wall, or another object. Preserve the accepted object and derive the mating support from its contact geometry. Smaug is a worked example. Choose retention for the actual object and intended use; this workflow does not require adhesive or establish structural adequacy by itself.

## Start from the accepted assembly and selected mount approach

Identify the mounted object, receiving support, fixed placement/scale, permitted edit region, intended retention method, and assembly sequence. Record excluded alternatives. Keep the accepted exterior and tested interfaces fixed unless their change is authorized. Adapt the support locally where possible rather than changing the object to make a convenient mount.

Keep source files intact. Save a revision with editable construction tools and a baseline for geometry/transform comparisons. Inspect the support mesh before modifying it so existing defects are distinguishable from new ones. A visually accepted support may still be unsuitable for manufacturing.

For David's FDM work, model parts as solid and let the slicer set infill, keeping deliberate voids (sockets, LED chambers, wire routes, tunnels).

## Build and refine the seats incrementally

1. **Find the actual contact regions.** Use the object in its accepted world-space placement. Inspect its intended contact patches and nearby support from useful angles; identify gaps, overlaps, likely entry/removal directions, and surfaces that must remain visible. Stay inside the authorized edit region.
2. **Bring support material to the object.** Add or expand the receiving support locally, using a transition appropriate to its material and form. Smooth rock expansion is one option; a shaped ledge, cradle, or socket may suit another support. Preserve the surrounding silhouette and unrelated elements. A small contact can be a useful visual experiment without providing enough structural support.
3. **Make a solid tool from the exterior contact shape.** Copy the relevant exterior region, trim it to the intended interface extent, cap any open cut boundaries, orient it, and verify a valid solid cutter. Work in a consistent coordinate frame. If the source is thin or hollow, do not assume subtracting its shell removes the enclosed space: use the exterior envelope to avoid trapped support material. Keep the visible object unchanged.
4. **Add adjustable mating allowance to the tool.** Offset the hidden cutter, then subtract it from the receiving support. Record whether the allowance is a normal/vertex offset, measured gap, or another construction parameter; these are not interchangeable guarantees. Choose final allowances for the intended process and retention method through fit tests, rather than copying the case's numbers.
5. **Inspect and repair the local result.** Check failed cuts, new seams, trapped material, detached fragments, and fragile projections between object details. Compare defect locations before/after; local repairs do not establish that the entire support is watertight. Retain the original support, pre-cut revision, and cutters in hidden construction collections.
6. **Relieve unwanted interlocking.** If an exact negative creates obstructing fingers or catches between adjacent features, subtract a shared clearance envelope where needed. Examples include gaps between toes, projections on a prop, or an overhanging edge. Retain useful seating surfaces and intentional locating keys; do not erase required retention or alter other mounts incidentally. Review the relief as a focused change.
7. **Open the insertion approach.** A matching final pocket is not sufficient. Define how the object enters and remove obstructing lips/undercuts using a tool representing its swept volume. A convex envelope of endpoint geometry can conservatively approximate a straight translational passage, as in the Smaug example, but may remove excess support. Rotational or curved approaches need an appropriate sweep. If no practical route preserves the accepted interface, consider an authorized removable support section or staged assembly rather than automatically widening every seat.
8. **Test movement as well as the final pose.** Test the actual object surface through intermediate positions, record collisions and sampled clearance, and show the exposed seat alongside the assembly. Add sampling at close approaches; discrete checks do not prove continuous collision-free motion. Keep the object in its accepted final placement in the saved review scene.

Before considering assembly feasible, test the whole rigid object against every interacting component. All its contact regions must follow one compatible path; clearance for one patch does not prove clearance for another or for protrusions elsewhere. For staged assemblies, test each part in order against the parts already installed, and test removal when serviceability is required. A local contact study, a complete digital path check, and a physical fit test are separate evidence.

## Worked example: Smaug

On Dale, nearby rock was built out to Smaug's fixed feet, and capped copies of the outer feet, offset 0.10 mm, cut the seats. A 0.65 mm envelope then cleared stone between the far toes, and an endpoint hull opened a straight entry 40 mm in from the front and 1.5 mm up; the foot had no collisions at 41 sampled poses. Smaug never moved. Only the local foot region was tested that way; a removable rear support and cap later made whole-body installation possible, and a small receiver and wing kit passed a physical fit. An early pin-and-sleeve prototype and a full-body Boolean merge were rejected; new glued joints use printed tabs (see [fabrication and lighting](fabrication-and-lighting.md#glued-joints)).

## Review and qualification record

Record the fixed object and receiving-support baselines, permitted support changes, mount method, cutter source and limits, allowance definition, retained contact regions, assembly approach, protected-object checks, new versus pre-existing defects, and precise collision-test scope. Use one compact comparison showing before/after, an exposed seat, and enough of the assembly to judge visibility.

Keep visual acceptance, local fit, whole-assembly access, and load and retention performance separate. Before production, resolve wall thickness and topology, evaluate contact area and load path, test fit and the chosen retention method with the actual materials, and check the complete assembly sequence. Do not enlarge contacts or add other supports merely because a preliminary seat exists; stay within the requested design scope and present unresolved support needs.
