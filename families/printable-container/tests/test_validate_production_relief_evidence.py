from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = PROJECT_ROOT / "skills/printable-container/scripts/validate_production_relief_evidence.py"
FIXTURE_RELATIVE = Path("skills/printable-container/tests/fixtures/production-relief")
FIXTURES = PROJECT_ROOT / FIXTURE_RELATIVE

SPEC = importlib.util.spec_from_file_location("production_relief_validator", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ProductionReliefValidatorTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        destination = root / FIXTURE_RELATIVE
        destination.parent.mkdir(parents=True)
        shutil.copytree(FIXTURES, destination)
        return temporary, root

    def load_document(self) -> dict[str, Any]:
        return json.loads(
            (FIXTURES / "valid-hand-painted.json").read_text(encoding="utf-8")
        )

    def validate_mutation(
        self, mutate: Callable[[dict[str, Any]], None]
    ) -> list[str]:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        document = copy.deepcopy(self.load_document())
        mutate(document)
        record = root / "record.json"
        record.write_text(json.dumps(document), encoding="utf-8")
        return VALIDATOR.validate_record(root, record)

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected diagnostic containing {fragment!r}, got {errors!r}",
        )

    def test_valid_single_color_hand_painted_record_and_finish_plan(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        errors = VALIDATOR.validate_record(
            root, root / FIXTURE_RELATIVE / "valid-hand-painted.json"
        )
        self.assertEqual([], errors)
        document = self.load_document()
        self.assertEqual("finish-plan", document["finish_plans"][0]["evidence_role"])
        self.assertIn("exact printed color is intentionally absent", document["finish_plans"][0]["palette_note"])

    def test_schema_v1_remains_valid_without_legibility_contract(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["schema_version"] = 1
            document.pop("neutral_evidence_packet")
            document.pop("legibility_preflight")
            document.pop("evidence_revision")
            for property_record in document["governed_properties"]:
                property_record.pop("legibility_requirement", None)
            for render in document["neutral_production_renders"]:
                for field in (
                    "role",
                    "property_ids",
                    "review_scale",
                    "framing",
                    "neutral_nondescriptive_material",
                    "subject_background_separation",
                    "legibility_status",
                    "prohibited_effects_excluded",
                    "applied_effects",
                ):
                    render.pop(field, None)

        self.assertEqual([], self.validate_mutation(mutate))

    def test_rejects_missing_render_role_and_matched_composition(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["neutral_production_renders"][0].pop("role")

        errors = self.validate_mutation(mutate)
        self.assert_error(errors, ".role must be matched-composition or focused-legibility")
        self.assert_error(errors, "lacks a matched-composition render")

    def test_rejects_incomplete_property_coverage_and_unknown_ids(self) -> None:
        def incomplete(document: dict[str, Any]) -> None:
            for render in document["neutral_production_renders"]:
                render["property_ids"] = []

        errors = self.validate_mutation(incomplete)
        self.assert_error(errors, "must identify covered production properties")
        self.assert_error(errors, "lack neutral render coverage")

        def unknown(document: dict[str, Any]) -> None:
            document["neutral_production_renders"][0]["property_ids"] = ["unknown-property"]
            document["legibility_preflight"]["reviewed_render_ids"].append("unknown-render")
            document["legibility_preflight"]["reviewed_property_ids"].append("unknown-property")

        errors = self.validate_mutation(unknown)
        self.assert_error(errors, "references unknown production property unknown-property")
        self.assert_error(errors, "references unknown neutral renders")
        self.assert_error(errors, "references unknown production properties")

    def test_rejects_missing_shallow_relief_detail(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["neutral_production_renders"] = [
                document["neutral_production_renders"][0]
            ]
            document["legibility_preflight"]["reviewed_render_ids"] = ["neutral-lid"]
            document["paint_boundaries"][0]["neutral_render_ids"] = ["neutral-lid"]

        errors = self.validate_mutation(mutate)
        self.assert_error(errors, "lack focused legibility evidence")

    def test_rejects_missing_background_separation_review_scale_and_unreadable_view(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["neutral_production_renders"][0].update(
                subject_background_separation=False
            )
        )
        self.assert_error(errors, "lacks subject/background tonal separation")

        errors = self.validate_mutation(
            lambda doc: doc["neutral_production_renders"][0].update(review_scale="")
        )
        self.assert_error(errors, "review_scale must be a non-empty string")

        for status in ("clipped", "merged", "underscaled", "obscured"):
            with self.subTest(status=status):
                errors = self.validate_mutation(
                    lambda doc, status=status: doc["neutral_production_renders"][0].update(
                        legibility_status=status
                    )
                )
                self.assert_error(errors, "legibility_status must be readable")

    def test_rejects_builder_authored_failing_or_incomplete_preflight(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"].update(
                auditor_id=doc["legibility_preflight"]["builder_id"]
            )
        )
        self.assert_error(errors, "auditor must be independent from builder")

        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"].update(
                status="evidence-inadequate",
                affected_render_ids=["neutral-lid"],
                affected_property_ids=["focal-star-relief"],
            )
        )
        self.assert_error(errors, "status must be pass before scoring")

        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"].update(
                reviewed_render_ids=["neutral-lid"], reviewed_property_ids=[]
            )
        )
        self.assert_error(errors, "does not cover current neutral renders")
        self.assert_error(errors, "does not cover production properties")

        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"].update(
                scores_or_classifications_assigned_before_preflight=True
            )
        )
        self.assert_error(errors, "must occur before scores or classifications")

    def test_rejects_prohibited_presentation_effects_and_missing_exclusion(self) -> None:
        for effect in (
            "painted-material-contrast",
            "emission",
            "bloom",
            "textures",
            "compositor-effects",
            "presentation-only-geometry",
        ):
            with self.subTest(effect=effect):
                errors = self.validate_mutation(
                    lambda doc, effect=effect: doc["neutral_production_renders"][0][
                        "applied_effects"
                    ].append(effect)
                )
                self.assert_error(errors, "uses prohibited presentation effects")

        errors = self.validate_mutation(
            lambda doc: doc["neutral_production_renders"][0].update(
                prohibited_effects_excluded=False
            )
        )
        self.assert_error(errors, "lacks prohibited-effect exclusions")

    def test_rejects_stale_render_packet_and_preflight_hashes(self) -> None:
        for mutate, fragment in (
            (
                lambda doc: doc["neutral_production_renders"][0].update(sha256="0" * 64),
                "neutral render neutral-lid.sha256 is stale",
            ),
            (
                lambda doc: doc["neutral_evidence_packet"].update(sha256="0" * 64),
                "neutral_evidence_packet.sha256 is stale",
            ),
            (
                lambda doc: doc["legibility_preflight"]["artifact"].update(sha256="0" * 64),
                "legibility_preflight.artifact.sha256 is stale",
            ),
        ):
            errors = self.validate_mutation(mutate)
            self.assert_error(errors, fragment)

    def test_rejects_preflight_hash_binding_gaps_and_unknown_ids(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"]["reviewed_render_hashes"].pop(
                "neutral-lid-detail"
            )
        )
        self.assert_error(errors, "lacks current render IDs")

        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"]["reviewed_render_hashes"].update(
                {"unknown-render": "1" * 64}
            )
        )
        self.assert_error(errors, "has unknown render IDs")

        errors = self.validate_mutation(
            lambda doc: doc["legibility_preflight"].update(packet_sha256="1" * 64)
        )
        self.assert_error(errors, "does not bind the current neutral evidence packet")

    def test_rejects_new_render_and_packet_with_stale_preflight_binding(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        document = copy.deepcopy(self.load_document())
        fixture_root = root / FIXTURE_RELATIVE
        render_path = fixture_root / "neutral-production.pgm"
        packet_path = fixture_root / "neutral-evidence-packet.txt"
        render_path.write_bytes(render_path.read_bytes() + b"\n# rerendered\n")
        packet_path.write_text(
            packet_path.read_text(encoding="utf-8") + "Replacement packet.\n",
            encoding="utf-8",
        )
        document["neutral_production_renders"][0]["sha256"] = hashlib.sha256(
            render_path.read_bytes()
        ).hexdigest()
        document["neutral_evidence_packet"]["sha256"] = hashlib.sha256(
            packet_path.read_bytes()
        ).hexdigest()
        record = root / "record.json"
        record.write_text(json.dumps(document), encoding="utf-8")

        errors = VALIDATOR.validate_record(root, record)
        self.assert_error(errors, "does not bind the current neutral evidence packet")
        self.assert_error(errors, "does not bind current neutral render neutral-lid")

    def test_accepts_evidence_only_rerender_invariants_and_rejects_geometry_change(self) -> None:
        def valid_rerender(document: dict[str, Any]) -> None:
            document["evidence_revision"] = {
                "change_type": "evidence-only-rerender",
                "geometry_changed": False,
                "fresh_full_audit_required": True,
                "previous_source_sha256": document["source_artifact"]["sha256"],
                "previous_export_hashes": {
                    part["id"]: part["export_artifact"]["sha256"]
                    for part in document["export_parts"]
                },
                "previous_render_hashes": {
                    "neutral-lid": "1" * 64,
                    "neutral-lid-detail": document["neutral_production_renders"][1]["sha256"],
                },
                "refreshed_render_ids": ["neutral-lid"],
                "previous_packet_sha256": "2" * 64,
            }

        self.assertEqual([], self.validate_mutation(valid_rerender))

        def invalid_rerender(document: dict[str, Any]) -> None:
            valid_rerender(document)
            document["evidence_revision"]["geometry_changed"] = True
            document["evidence_revision"]["previous_export_hashes"]["lid-production"] = "3" * 64

        errors = self.validate_mutation(invalid_rerender)
        self.assert_error(errors, "cannot declare geometry changes")
        self.assert_error(errors, "previous export hashes must exactly match current exports")

        def false_preservation_claim(document: dict[str, Any]) -> None:
            valid_rerender(document)
            document["evidence_revision"].update(
                source_hash_preserved=True,
                export_hashes_preserved=True,
                previous_source_sha256="4" * 64,
            )

        errors = self.validate_mutation(false_preservation_claim)
        self.assert_error(errors, "changed the source artifact hash")

        def false_refresh_claim(document: dict[str, Any]) -> None:
            valid_rerender(document)
            document["evidence_revision"].update(render_hashes_refreshed=True)
            document["evidence_revision"]["previous_render_hashes"]["neutral-lid"] = document[
                "neutral_production_renders"
            ][0]["sha256"]

        errors = self.validate_mutation(false_refresh_claim)
        self.assert_error(errors, "is marked refreshed but its hash is unchanged")

        def false_packet_refresh_claim(document: dict[str, Any]) -> None:
            valid_rerender(document)
            document["evidence_revision"].update(packet_hash_refreshed=True)
            document["evidence_revision"]["previous_packet_sha256"] = document[
                "neutral_evidence_packet"
            ]["sha256"]

        errors = self.validate_mutation(false_packet_refresh_claim)
        self.assert_error(errors, "packet hash must change")

    def test_cli_exercises_valid_record(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(PROJECT_ROOT),
                "--record",
                str(FIXTURE_RELATIVE / "valid-hand-painted.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS production-relief evidence", result.stdout)

    def test_cli_returns_nonzero_with_exact_failure(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        document = self.load_document()
        document["paint_boundaries"][0]["evidence_kind"] = "shader-only"
        record = root / "record.json"
        record.write_text(json.dumps(document), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--record",
                "record.json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("uses non-geometric evidence: shader-only", result.stdout)

    def test_rejects_missing_property_coverage(self) -> None:
        errors = self.validate_mutation(lambda doc: doc.update(paint_boundaries=[]))
        self.assert_error(errors, "lack paint-boundary coverage")
        self.assert_error(errors, "declared paint transitions without boundary records")

    def test_rejects_undeclared_or_unmapped_paint_transitions(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["governed_properties"][0].update(
                paint_transition_ids=["star-to-outline", "outline-to-field"]
            )
        )
        self.assert_error(errors, "declared paint transitions without boundary records")

        errors = self.validate_mutation(
            lambda doc: doc["governed_properties"][0].update(
                paint_transition_ids=["different-transition"]
            )
        )
        self.assert_error(errors, "is not declared by governed property")
        self.assert_error(errors, "has undeclared paint-boundary records")

    def test_rejects_cross_property_transition_swap(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["governed_properties"].append(
                {
                    "id": "moon-relief",
                    "description": "Moon relief remains printable and paintable.",
                    "authority": "production-geometry",
                    "paint_transition_ids": ["moon-to-ring"],
                }
            )
            second_boundary = copy.deepcopy(document["paint_boundaries"][0])
            document["paint_boundaries"][0]["id"] = "moon-to-ring"
            second_boundary.update(
                id="star-to-outline",
                property_id="moon-relief",
            )
            document["paint_boundaries"].append(second_boundary)

        errors = self.validate_mutation(mutate)
        self.assert_error(
            errors,
            "paint boundary moon-to-ring is not declared by governed property focal-star-relief",
        )
        self.assert_error(
            errors,
            "paint boundary star-to-outline is not declared by governed property moon-relief",
        )
        self.assert_error(
            errors,
            "governed property focal-star-relief has declared paint transitions without boundary records",
        )
        self.assert_error(
            errors,
            "governed property moon-relief has declared paint transitions without boundary records",
        )

    def test_rejects_stale_source_and_boundary_absent_from_neutral_render(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["source_artifact"].update(sha256="0" * 64)
        )
        self.assert_error(errors, "source_artifact.sha256 is stale")

        errors = self.validate_mutation(
            lambda doc: doc["neutral_production_renders"][0].update(
                included_object_ids=[]
            )
        )
        self.assert_error(errors, "must identify included production objects")
        self.assert_error(errors, "is absent from neutral render")

    def test_rejects_presentation_only_source_support(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["source_objects"][0].update(
                name="PRESENTATION_FocalStar", classification="presentation"
            )

        errors = self.validate_mutation(mutate)
        self.assert_error(errors, "supported only by presentation geometry")

    def test_rejects_presentation_object_in_neutral_render(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["source_objects"].append(
                {
                    "id": "presentation-glow",
                    "name": "PRESENTATION_Glow",
                    "classification": "presentation",
                }
            )
            document["neutral_production_renders"][0]["included_object_ids"].append(
                "presentation-glow"
            )

        errors = self.validate_mutation(mutate)
        self.assert_error(errors, "includes presentation-only object")

    def test_rejects_export_exclusion_and_missing_round_trip(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["export_parts"][0].update(export_included=False)
        )
        self.assert_error(errors, "not included in production exports")

        errors = self.validate_mutation(
            lambda doc: doc["export_parts"][0]["round_trip"].update(verified=False)
        )
        self.assert_error(errors, "lacks verified round-trip evidence")

        errors = self.validate_mutation(
            lambda doc: doc["export_parts"][0].update(included_object_ids=[])
        )
        self.assert_error(errors, "must identify included source objects")
        self.assert_error(errors, "is absent from export part")

    def test_rejects_stale_round_trip_hash_and_unsafe_path(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["export_parts"][0]["round_trip"]["artifact"].update(
                sha256="0" * 64
            )
        )
        self.assert_error(errors, "sha256 is stale")

        errors = self.validate_mutation(
            lambda doc: doc["neutral_production_renders"][0].update(path="../escape.png")
        )
        self.assert_error(errors, "escapes project root")

        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        errors = VALIDATOR.validate_record(root, root.parent / "outside.json")
        self.assert_error(errors, "record path escapes project root")

    def test_rejects_unresolved_or_unsupported_finish_mode(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["finish_mode_resolution"].update(status="ambiguous")
        )
        self.assert_error(errors, "status must be 'resolved'")

        errors = self.validate_mutation(
            lambda doc: doc["finish_mode_resolution"].update(modes=["paint-someday"])
        )
        self.assert_error(errors, "unique supported finish modes")

    def test_rejects_incomplete_boundary_dimensions_and_paint_access(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["paint_boundaries"][0].update(dimensions={})
        )
        self.assert_error(errors, "dimensions must contain positive numeric measurements")

        for field in ("brush_access", "masking_access"):
            with self.subTest(field=field):
                errors = self.validate_mutation(
                    lambda doc, field=field: doc["paint_boundaries"][0].update(
                        {field: ""}
                    )
                )
                self.assert_error(errors, f"{field} must be a non-empty string")

    def test_rejects_shader_texture_material_emission_and_compositor_support(self) -> None:
        for evidence_kind in (
            "shader-only",
            "texture-only",
            "material-assignment",
            "emission",
            "compositor-effect",
        ):
            with self.subTest(evidence_kind=evidence_kind):
                errors = self.validate_mutation(
                    lambda doc, evidence_kind=evidence_kind: doc["paint_boundaries"][0].update(
                        evidence_kind=evidence_kind
                    )
                )
                self.assert_error(errors, "uses non-geometric evidence")

    def test_requires_finish_plan_property_traceability(self) -> None:
        errors = self.validate_mutation(
            lambda doc: doc["finish_plans"][0].update(property_ids=[])
        )
        self.assert_error(errors, "must identify governed finish-plan properties")
        self.assert_error(errors, "lack labeled finish-plan evidence")

    def test_rejects_bloom_only_physical_optical_claim(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["finish_mode_resolution"]["modes"].append(
                "physical-illumination-or-translucency"
            )
            document["governed_properties"].append(
                {
                    "id": "physical-glow",
                    "description": "The star physically illuminates.",
                    "authority": "physical-optics",
                }
            )
            document["physical_optical_evidence"] = [
                {
                    "property_id": "physical-glow",
                    "evidence_kind": "emission",
                    "light_path_artifact": {
                        "path": str(FIXTURE_RELATIVE / "light-path.pgm"),
                        "sha256": "290d8d32bc0a45af18a500b188ebc489d061a795d3faa247003f5f4f5f583735",
                    },
                    "test_artifact": {
                        "path": str(FIXTURE_RELATIVE / "optical-test.txt"),
                        "sha256": "9d4a381733bd5e33d5161ffabe1b52a6c0a521dee7e6ac6cb3b2be2ae0f49e5a",
                    },
                    "test_conditions": "Rendered bloom only.",
                }
            ]

        errors = self.validate_mutation(mutate)
        self.assert_error(errors, "must be physical-test, not emission")

    def test_accepts_separate_physical_optical_test_evidence(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["finish_mode_resolution"]["modes"].append(
                "physical-illumination-or-translucency"
            )
            document["governed_properties"].append(
                {
                    "id": "physical-glow",
                    "description": "The star physically illuminates.",
                    "authority": "physical-optics",
                }
            )
            document["physical_optical_evidence"] = [
                {
                    "property_id": "physical-glow",
                    "evidence_kind": "physical-test",
                    "light_path_artifact": {
                        "path": str(FIXTURE_RELATIVE / "light-path.pgm"),
                        "sha256": "290d8d32bc0a45af18a500b188ebc489d061a795d3faa247003f5f4f5f583735",
                    },
                    "test_artifact": {
                        "path": str(FIXTURE_RELATIVE / "optical-test.txt"),
                        "sha256": "9d4a381733bd5e33d5161ffabe1b52a6c0a521dee7e6ac6cb3b2be2ae0f49e5a",
                    },
                    "test_conditions": "Bench test with named LED, diffuser, voltage, and camera exposure.",
                }
            ]

        self.assertEqual([], self.validate_mutation(mutate))


if __name__ == "__main__":
    unittest.main()
