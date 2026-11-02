---
name: printable-container
description: Design decorative 3D-printable containers from concept art or a brief through dimensional architecture, editable modeling, independent audits, fit tests, printable STL files, and release documentation. Use for boxes, chests, cases, lanterns, enclosures, and similar hollow assemblies; do not use for ordinary standalone miniatures, purely visual renders, or safety-critical pressure, medical, food-contact, mains-voltage, open-flame, or high-energy battery products without domain-specific engineering requirements.
---

# Printable container

Turn a visual idea into a usable, manufacturable container without quietly designing away what made the concept appealing. Treat visual design, protected function, mechanical architecture, manufacturing, physical evidence, and release claims as related but distinct systems.

## Begin with authority and evidence

Before modeling, identify the authoritative references, explicit user requirements, actual contents and hardware, available printers/processes, intended energy or light source, project-specific definition of done, and which decisions remain provisional. Preserve original references and measurements. Do not infer hidden construction, exact dimensions, materials, electronics, or mechanisms from concept art. Hold open-flame or other safety-critical designs unless suitable domain requirements, materials, clearances, tests, and acceptance criteria are supplied; never imply ordinary printed plastic is flame-safe.

Create or update a checkpoint containing the active source, accepted decisions, protected geometry and interfaces, open risks, validation performed, physical feedback, superseded artifacts, and next step. For a new or substantially changed design, read [concept and faithfulness](references/concept-and-faithfulness.md). Use the record forms in [project records](references/project-records.md).

## Work from protected function outward

1. Define the finished usable interior and the envelopes of contents, lining, hands, tools, connectors, cables, hinges, and moving parts.
2. Establish a dependency map: contents and clearances → structural shell → lid/closure/hinge → internal modules → decoration/electronics → interface tests → production parts.
3. Make a complete, inexpensive blockout. Reserve major focal forms, openings, motion, assembly paths, service access, structure, wiring, and supports before detail.
4. Develop the design as editable systems: shell, mechanisms, inserts, decoration, sculpture, lighting/electronics, and release geometry. Preserve accepted sources and change locally.
5. Choose methods by form: dimension-controlled solids for functional geometry; sculpting or reference-driven reconstruction for organic focal elements; controlled integration for the final printable parts.
6. Engineer solid material volumes at final scale. Let the slicer create infill; create voids only when they serve a deliberate function.

Read [engineering and validation](references/engineering-and-validation.md) before designing joints, thin features, segmentation, electronics, print orientation, or final exports.

## Retire uncertainty cheaply

For every consequential unknown, ask what smallest test can answer it. Prefer representative coupons or shallow interface assemblies before full-size parts. Test such things as sliding clearance, magnet pockets, hinge motion, connector engagement, panel retention, feature thickness, optical spacing, hardware envelopes, paint allowance, and support removal using the intended material, printer, orientation, and slicer profile.

Record actual dimensions and outcomes. A successful test locks only the tested interface and conditions; it does not qualify the entire assembly. Physical results outrank unsupported digital confidence.

## Use independent audit gates

For a significant custom build, use a separate auditing agent at the gates below when delegation is available and authorized. The auditor must not be the builder. Give it the brief, authoritative references, current checkpoint, actual current artifacts, and acceptance criteria; do not give it the builder's conclusions. If independent delegation is unavailable, perform a clearly labeled self-review and disclose that it was not independent.

- **Faithfulness gate:** after blockout and again after decorative integration when the concept is a primary design authority.
- **Design-lock gate:** before detailed work makes dimensional or architectural changes expensive.
- **Print-engineering gate:** before committing to full-size exports or long prints.
- **Release gate:** after generating the actual deliverables and before assigning a release claim level.

Do not audit every routine edit. Re-audit after a material change to a governing reference, protected interior, focal silhouette, assembly architecture, process, or previously accepted interface. Read [independent audits](references/independent-audits.md) for inputs, verdicts, and audit boundaries.

## Keep claims separated

Use this evidence ladder and state the highest level actually reached:

1. Visual review
2. Dimensional and geometry audit
3. Exported-mesh audit
4. Slicer, support, and layer review
5. Representative physical coupon
6. Full component fit
7. Complete physical assembly and use test
8. Qualified assembled release

A good render, closed mesh, successful Boolean, one connected component, build-volume fit, or warning-free slice does not prove later levels. Sampled clearances are not exact global bounds. Overlapping decorative shells are not a globally united solid. Clearly distinguish modeled, digitally checked, sliced, physically tested, and released artifacts.

Use claim levels consistently:

- **Digitally validated STL candidate:** exported mesh and slicer evidence only; no physical-fit claim.
- **Prototype release:** printable files supplied for evaluation with unresolved physical behavior stated.
- **Interface-fit-tested release:** named critical interfaces passed representative physical tests under recorded conditions; the whole assembly may remain unqualified.
- **Qualified assembled release:** complete physical assembly and intended-use testing passed, including all safety- or function-critical interfaces and the defined acceptance criteria.

Any multi-part functional interface requires representative physical evidence before claims above prototype level apply to that interface. The builder and auditor identify required tests from the brief, hazards, failure consequences, and definition of done; they may not make tests optional merely to advance the claim.

## Finish with actual deliverables

Audit the exported STLs rather than relying only on the source scene. Verify units, scale, orientation, dimensions, winding, manifoldness, components, positive volume, degeneracy, unintended intersections or gaps, and round-trip import as relevant. Inspect the complete sliced plate and support/layer behavior for the selected process.

Deliver authoritative source and export files, quantities, orientation and material guidance, assembly order, hardware/BOM, tested and untested interfaces, safety constraints, compromise register, validation report, and versioned package when the scope warrants them. Assign only the highest supported release claim level; do not use the ambiguous standalone label “print-ready.”
