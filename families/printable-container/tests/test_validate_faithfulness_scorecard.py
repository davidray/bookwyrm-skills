from __future__ import annotations

import copy
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
SCRIPT = PROJECT_ROOT / "skills/printable-container/scripts/validate_faithfulness_scorecard.py"
FIXTURE_RELATIVE = Path("skills/printable-container/tests/fixtures/faithfulness-scorecards")
FIXTURES = PROJECT_ROOT / FIXTURE_RELATIVE

SPEC = importlib.util.spec_from_file_location("faithfulness_validator", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class FaithfulnessValidatorTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        destination = root / FIXTURE_RELATIVE
        destination.parent.mkdir(parents=True)
        shutil.copytree(FIXTURES, destination)
        return temporary, root

    def load_document(self, name: str = "valid-blockout.json") -> dict[str, Any]:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def validate_mutation(
        self,
        mutate: Callable[[dict[str, Any]], None],
        *,
        fixture: str = "valid-blockout.json",
        milestone: str = "blockout",
    ) -> tuple[float | None, list[str]]:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        document = copy.deepcopy(self.load_document(fixture))
        mutate(document)
        scorecard = root / "case.json"
        scorecard.write_text(json.dumps(document), encoding="utf-8")
        return VALIDATOR.validate_scorecard(root, scorecard, milestone)

    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected diagnostic containing {fragment!r}, got {errors!r}",
        )

    def test_valid_blockout_and_decorative_scorecards(self) -> None:
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        blockout_total, blockout_errors = VALIDATOR.validate_scorecard(
            root, root / FIXTURE_RELATIVE / "valid-blockout.json", "blockout"
        )
        decorative_total, decorative_errors = VALIDATOR.validate_scorecard(
            root,
            root / FIXTURE_RELATIVE / "valid-decorative-integration.json",
            "decorative-integration",
        )
        self.assertEqual(94, blockout_total)
        self.assertEqual([], blockout_errors)
        self.assertEqual(96, decorative_total)
        self.assertEqual([], decorative_errors)

    def test_cli_accepts_both_required_milestones(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(PROJECT_ROOT),
                "--require",
                f"blockout={FIXTURE_RELATIVE / 'valid-blockout.json'}",
                "--require",
                f"decorative-integration={FIXTURE_RELATIVE / 'valid-decorative-integration.json'}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS blockout", result.stdout)
        self.assertIn("total=94/100", result.stdout)
        self.assertIn("PASS decorative-integration", result.stdout)
        self.assertIn("total=96/100", result.stdout)

    def test_cli_rejects_missing_scorecard_and_requires_milestone_argument(self) -> None:
        missing = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(PROJECT_ROOT),
                "--require",
                "blockout=missing.json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        empty = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(PROJECT_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(1, missing.returncode)
        self.assertIn("scorecard does not exist", missing.stdout)
        self.assertEqual(2, empty.returncode)
        self.assertIn("at least one --require", empty.stderr)

    def test_rejects_missing_and_extra_criteria(self) -> None:
        _, missing_errors = self.validate_mutation(lambda doc: doc["criteria"].pop())
        self.assert_has_error(missing_errors, "missing canonical criteria")

        def add_extra(document: dict[str, Any]) -> None:
            document["criteria"].append(
                {
                    "id": "invented-criterion",
                    "weight": 0,
                    "score": 5,
                    "evidence_view_ids": ["blockout-closed-match"],
                    "rationale": "This criterion is not canonical.",
                }
            )

        _, extra_errors = self.validate_mutation(add_extra)
        self.assert_has_error(extra_errors, "unexpected criteria")

    def test_rejects_altered_weight_invalid_score_and_unknown_evidence(self) -> None:
        for mutation, diagnostic in (
            (lambda doc: doc["criteria"][0].update(weight=34), "weight must be 35"),
            (lambda doc: doc["criteria"][0].update(score=6), "score must be an integer"),
            (
                lambda doc: doc["criteria"][0].update(evidence_view_ids=["missing-view"]),
                "cites unknown matched-view evidence",
            ),
        ):
            with self.subTest(diagnostic=diagnostic):
                _, errors = self.validate_mutation(mutation)
                self.assert_has_error(errors, diagnostic)

    def test_rejects_incorrect_total_verdict_and_floor(self) -> None:
        _, total_errors = self.validate_mutation(lambda doc: doc.update(claimed_total=99))
        self.assert_has_error(total_errors, "does not match computed total")
        _, verdict_errors = self.validate_mutation(lambda doc: doc.update(verdict="HOLD"))
        self.assert_has_error(verdict_errors, "verdict must be 'PASS'")

        def lower_floor(document: dict[str, Any]) -> None:
            document["criteria"][0]["score"] = 3
            document["claimed_total"] = 80

        _, floor_errors = self.validate_mutation(lower_floor)
        self.assert_has_error(floor_errors, "below floor 4")
        self.assert_has_error(floor_errors, "below blockout threshold")

    def test_rejects_each_stale_artifact_class(self) -> None:
        assets = ("concept.png", "source.blend", "blockout-closed.png")
        for asset in assets:
            with self.subTest(asset=asset):
                temporary, root = self.make_root()
                try:
                    target = root / FIXTURE_RELATIVE / asset
                    target.write_bytes(target.read_bytes() + b"changed")
                    _, errors = VALIDATOR.validate_scorecard(
                        root,
                        root / FIXTURE_RELATIVE / "valid-blockout.json",
                        "blockout",
                    )
                    self.assert_has_error(errors, "sha256 is stale")
                finally:
                    temporary.cleanup()

    def test_rejects_missing_matched_views_and_uncovered_approved_views(self) -> None:
        _, missing_errors = self.validate_mutation(lambda doc: doc.update(matched_views=[]))
        self.assert_has_error(missing_errors, "approved views lack matched evidence")

        def add_uncovered(document: dict[str, Any]) -> None:
            document["approved_views"].append("underside")

        _, uncovered_errors = self.validate_mutation(add_uncovered)
        self.assert_has_error(uncovered_errors, "'underside'")

    def test_rejects_self_audit_and_unresolved_blocking_finding(self) -> None:
        _, identity_errors = self.validate_mutation(
            lambda doc: doc.update(auditor={"id": "model-builder"})
        )
        self.assert_has_error(identity_errors, "auditor must be independent")

        def add_finding(document: dict[str, Any]) -> None:
            document["blocking_findings"] = [
                {"id": "F-1", "disposition": "open"}
            ]

        _, finding_errors = self.validate_mutation(add_finding)
        self.assert_has_error(finding_errors, "is unresolved")

    def test_rejects_pending_identity_compromise(self) -> None:
        def add_compromise(document: dict[str, Any]) -> None:
            document["compromises"] = [
                {
                    "id": "C-1",
                    "identity_changing": True,
                    "user_decision": "pending",
                }
            ]

        _, errors = self.validate_mutation(add_compromise)
        self.assert_has_error(errors, "identity-changing")

    def test_rejects_waived_visual_ac_even_for_prototype(self) -> None:
        def waive_for_prototype(document: dict[str, Any]) -> None:
            document["release_claim"] = "prototype"
            document["visual_acceptance_criteria"][0]["status"] = "waived"

        _, errors = self.validate_mutation(waive_for_prototype)
        self.assert_has_error(errors, "cannot be waived or skipped")

    def test_rejects_focused_reaudit(self) -> None:
        _, errors = self.validate_mutation(lambda doc: doc.update(audit_scope="focused"))
        self.assert_has_error(errors, "focused audits are supplemental only")

    def test_rejects_unsafe_artifact_and_scorecard_paths(self) -> None:
        def escape_source(document: dict[str, Any]) -> None:
            document["artifacts"]["source"]["path"] = "../outside.blend"

        _, artifact_errors = self.validate_mutation(escape_source)
        self.assert_has_error(artifact_errors, "escapes project root")
        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        _, scorecard_errors = VALIDATOR.validate_scorecard(
            root, root.parent / "outside.json", "blockout"
        )
        self.assert_has_error(scorecard_errors, "scorecard path escapes project root")

    def test_rejects_decorative_threshold_and_characteristic_motif_floor(self) -> None:
        def lower_motifs(document: dict[str, Any]) -> None:
            for criterion in document["criteria"]:
                if criterion["id"] == "decorative-motifs":
                    criterion["score"] = 3
            document["claimed_total"] = 88

        _, errors = self.validate_mutation(
            lower_motifs,
            fixture="valid-decorative-integration.json",
            milestone="decorative-integration",
        )
        self.assert_has_error(errors, "decorative-motifs score 3 is below floor 4")
        self.assert_has_error(errors, "below decorative-integration threshold")

    def test_rejects_missing_stale_duplicate_and_wrong_comparisons(self) -> None:
        _, missing_errors = self.validate_mutation(
            lambda doc: doc.update(comparison_artifacts=[])
        )
        self.assert_has_error(missing_errors, "lack comparison artifacts")

        def duplicate_view(document: dict[str, Any]) -> None:
            duplicate = copy.deepcopy(document["comparison_artifacts"][0])
            duplicate["id"] = "duplicate-comparison"
            document["comparison_artifacts"].append(duplicate)

        _, duplicate_errors = self.validate_mutation(duplicate_view)
        self.assert_has_error(duplicate_errors, "duplicate comparison artifact for approved view")

        _, wrong_reference_errors = self.validate_mutation(
            lambda doc: doc["matched_views"][0].update(
                comparison_artifact_id="blockout-open-comparison"
            )
        )
        self.assert_has_error(wrong_reference_errors, "wrong comparison artifact")

        _, multiple_view_errors = self.validate_mutation(
            lambda doc: doc["matched_views"][0].update(
                covers=["closed-hero", "open-interior"]
            )
        )
        self.assert_has_error(multiple_view_errors, "exactly one approved view")

        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        comparison = root / FIXTURE_RELATIVE / "blockout-closed-comparison.pgm"
        comparison.write_bytes(comparison.read_bytes() + b"changed")
        _, stale_errors = VALIDATOR.validate_scorecard(
            root, root / FIXTURE_RELATIVE / "valid-blockout.json", "blockout"
        )
        self.assert_has_error(stale_errors, "sha256 is stale")

    def test_rejects_missing_duplicate_and_broken_property_assessments(self) -> None:
        _, missing_errors = self.validate_mutation(
            lambda doc: doc["property_assessments"].pop()
        )
        self.assert_has_error(missing_errors, "approved properties lack assessments")

        def duplicate_assessment(document: dict[str, Any]) -> None:
            document["property_assessments"].append(
                copy.deepcopy(document["property_assessments"][0])
            )

        _, duplicate_errors = self.validate_mutation(duplicate_assessment)
        self.assert_has_error(duplicate_errors, "duplicate property assessment")

        for field, value, diagnostic in (
            ("criterion_ids", ["unknown-criterion"], "must match its approved-property definition"),
            ("matched_view_ids", ["unknown-match"], "references unknown matched views"),
            (
                "comparison_artifact_ids",
                ["unknown-comparison"],
                "references unknown comparison artifacts",
            ),
        ):
            with self.subTest(field=field):
                _, reference_errors = self.validate_mutation(
                    lambda doc, field=field, value=value: doc["property_assessments"][0].update(
                        {field: value}
                    )
                )
                self.assert_has_error(reference_errors, diagnostic)

    def test_property_classifications_cap_related_scores(self) -> None:
        cases = (("exact", 5), ("minor", 4), ("material", 3), ("missing", 1))
        for classification, cap in cases:
            for score, should_fail in ((cap, False), (cap + 1, True)):
                with self.subTest(
                    classification=classification,
                    score=score,
                    should_fail=should_fail,
                ):
                    def mutate(document: dict[str, Any]) -> None:
                        document["property_assessments"][0]["classification"] = classification
                        document["criteria"][0]["score"] = score
                        document["claimed_total"] = score * 35 / 5 + 59

                    _, errors = self.validate_mutation(mutate)
                    diagnostic = f"exceeds cap {cap}"
                    if should_fail:
                        self.assert_has_error(
                            errors,
                            "score must be an integer" if score > 5 else diagnostic,
                        )
                    else:
                        self.assertFalse(
                            any(diagnostic in error for error in errors), errors
                        )

    def test_rejects_reliquary_style_ninety_two_point_overscore(self) -> None:
        def overscore_material_motif(document: dict[str, Any]) -> None:
            for assessment in document["property_assessments"]:
                if assessment["property_id"] == "motif-property":
                    assessment["classification"] = "material"
            for criterion in document["criteria"]:
                if criterion["id"] == "decorative-motifs":
                    criterion["score"] = 5

        _, errors = self.validate_mutation(
            overscore_material_motif,
            fixture="valid-decorative-integration.json",
            milestone="decorative-integration",
        )
        self.assert_has_error(
            errors,
            "criterion decorative-motifs score 5 exceeds cap 3 from property motif-property",
        )

    def test_rejects_non_independent_or_threshold_aware_provenance(self) -> None:
        _, same_run_errors = self.validate_mutation(
            lambda doc: doc["audit_provenance"].update(
                run_id=doc["audit_provenance"]["builder_run_id"]
            )
        )
        self.assert_has_error(same_run_errors, "distinct from the builder run")

        def reveal_threshold(document: dict[str, Any]) -> None:
            document["audit_provenance"]["input_excluded"].remove("target-threshold")
            document["audit_provenance"]["scores_recorded_before_threshold_check"] = False

        _, threshold_errors = self.validate_mutation(reveal_threshold)
        self.assert_has_error(threshold_errors, "not threshold-blind")
        self.assert_has_error(threshold_errors, "must be true")

    def test_decorative_gate_requires_current_explicit_user_approval(self) -> None:
        for mutation, diagnostic in (
            (
                lambda doc: doc.pop("final_visual_review"),
                "final_visual_review.revision",
            ),
            (
                lambda doc: doc["final_visual_review"].update(decision="pending"),
                "decision must be 'approved'",
            ),
            (
                lambda doc: doc["final_visual_review"].update(source="auditor-verdict"),
                "source must be 'user-message'",
            ),
            (
                lambda doc: doc["final_visual_review"].update(recorded_by="builder"),
                "must be recorded by the orchestrator",
            ),
        ):
            with self.subTest(diagnostic=diagnostic):
                _, errors = self.validate_mutation(
                    mutation,
                    fixture="valid-decorative-integration.json",
                    milestone="decorative-integration",
                )
                self.assert_has_error(errors, diagnostic)

        temporary, root = self.make_root()
        self.addCleanup(temporary.cleanup)
        packet = root / FIXTURE_RELATIVE / "final-visual-review-packet.pgm"
        packet.write_bytes(packet.read_bytes() + b"changed")
        _, stale_errors = VALIDATOR.validate_scorecard(
            root,
            root / FIXTURE_RELATIVE / "valid-decorative-integration.json",
            "decorative-integration",
        )
        self.assert_has_error(stale_errors, "sha256 is stale")


if __name__ == "__main__":
    unittest.main()
