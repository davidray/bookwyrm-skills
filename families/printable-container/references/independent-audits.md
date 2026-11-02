# Independent audits

Use these gates for significant custom designs when an independent agent is available and authorized. Independence means the auditing agent did not build the artifact under review. Automated checks supplement the audit; they do not replace it. Physical testing remains separate.

## Common audit protocol

Prepare a clean authority/evidence packet. Separate user-approved facts and raw measurements from builder interpretations, prior audit verdicts, and proposed conclusions. Give the auditor only:

- the user brief and current authoritative references;
- the current source/status facts, project definition of done, and acceptance criteria, omitting prior verdicts unless their disposition is itself under audit;
- the actual current model renders, source data needed for inspection, exports, and validation evidence;
- known user constraints and accepted interfaces.

Do not provide the builder's conclusions, suspected findings, or desired verdict. Ask the auditor to cite evidence, state what it could not verify, and avoid redesigning outside the current scope.

Classify each finding:

- **Blocking:** unsafe, functionally invalid, materially unfaithful without approval, or contradicts a governing requirement.
- **Needs physical evidence:** cannot be qualified without a coupon, full component, or use test.
- **Recommended improvement:** worthwhile but not required for the stated acceptance criteria.
- **Verified:** supported by the reviewed evidence.
- **Not verifiable:** missing evidence or outside the audit method.

The builder must disposition every blocking and physical-evidence finding as fixed, accepted by the user as a compromise, deferred with the release held, or shown inapplicable with evidence. Re-run only the affected audit after a material fix.

## Faithfulness gate

Run after the complete blockout and, for decorative designs, after decorative integration. Read [concept and faithfulness](concept-and-faithfulness.md).

Ask the auditor to compare the actual model against the authority map, assess silhouette, proportion, hierarchy, motif, focal subjects, negative space, story, and intended views, and produce or review the compromise register. The auditor must distinguish required compromise, chosen adaptation, accidental drift, unresolved ambiguity, and faithful modeling.

This audit reports the visual cost of manufacturing choices; it does not silently decide that the cost is acceptable.

## Design-lock gate

Run before detailed work makes architectural changes expensive. Check:

- protected interior and actual contents;
- wall, floor, lid, lining, and hardware allocations;
- dependency order and reserved envelopes;
- hinge, opening, assembly, service, and wiring paths;
- separation of structural and decorative systems;
- unresolved measurements or mechanism choices;
- whether prior-project assumptions entered without authority.

The result should identify which decisions may safely lock and which must remain provisional.

## Print-engineering gate

Run before full-size exports or long prints. Inspect final-scale geometry and the chosen process for:

- load paths, attachment roots, thin and fragile features;
- segmentation, joints, tolerances, paint allowance, and adjustability;
- insertion, removal, support-removal, and maintenance paths;
- orientation, supports, bed contact, anisotropy, drainage, and post-processing;
- electronics safety and service where relevant;
- power/current, thermal, wiring, charging, polarity, strain-relief, and energy-source evidence where relevant;
- whether planned coupons answer the actual high-risk questions;
- whether digital evidence is being overstated.

The output should prioritize the cheapest experiments that retire the largest remaining risks.

## Release gate

Run on the actual package, not a description of it. Inspect authoritative exports, round-trip and mesh reports, slicer evidence, documentation, quantities, filenames, units, orientation, hardware, assembly order, safety notes, compromise disclosure, and tested-versus-untested claims.

The auditor must assign the highest supported claim level from `SKILL.md`. A qualified assembled release requires a complete physical assembly and intended-use test, including all safety- or function-critical interfaces. A multi-part functional interface needs representative physical evidence before any fit-tested claim applies to it. If those tests are missing, the package remains a prototype regardless of clean digital checks.

