from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = PROJECT_ROOT / "skills/printable-container/scripts/delivery_gate_state.py"
FLOW_SCRIPT = PROJECT_ROOT / "skills/printable-container/scripts/exercise_delivery_gate_flow.py"
FLOW_FIXTURE = PROJECT_ROOT / "skills/printable-container/tests/fixtures/delivery-gates"
SPEC = importlib.util.spec_from_file_location("delivery_gate_state", SCRIPT)
assert SPEC and SPEC.loader
GATES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GATES
SPEC.loader.exec_module(GATES)


def gate_state(
    *, second_live_gate: bool = False, later_gate: bool = False
) -> dict[str, Any]:
    gates = [
        {
            "id": "final-visual-review",
            "kind": "final-matched-view-approval",
            "order": 20,
            "non_delegable": True,
            "state": "pending",
            "packet": {
                "id": "matched-view-packet",
                "revision": "v2",
                "sha256": "a" * 64,
            },
            "decision_requested": "Approve this final visual implementation or request revisions.",
            "compromises": ["brass is a printed finish"],
            "authorized_after": ["print-engineering", "release-packaging"],
            "resume_point": "print-engineering",
            "prohibited_downstream": [
                "print-engineering",
                "release-packaging",
                "cold-delivery-audit",
                "hero-spec-verify",
            ],
        }
    ]
    if second_live_gate:
        duplicate = dict(gates[0])
        duplicate["id"] = "alternate-final-review"
        duplicate["packet"] = {
            "id": "alternate-packet",
            "revision": "v2",
            "sha256": "b" * 64,
        }
        gates.append(duplicate)
    if later_gate:
        gates.append(
            {
                "id": "physical-fit-decision",
                "kind": "physical-test-decision",
                "order": 30,
                "non_delegable": True,
                "state": "pending",
                "packet": {
                    "id": "coupon-results",
                    "revision": "v1",
                    "sha256": "e" * 64,
                },
                "decision_requested": "Accept the measured interface or request another coupon.",
                "compromises": [],
                "authorized_after": ["release-packaging"],
                "resume_point": "release-packaging",
                "prohibited_downstream": ["release-packaging", "hero-spec-verify"],
            }
        )
    return {
        "schema_version": 1,
        "delivery_status": "delivering",
        "gates": gates,
        "decision_history": [],
        "superseded_packets": [],
        "closing_work": [
            "completion-ledger",
            "cold-delivery-audit",
            "hero-spec-verify",
        ],
    }


class DeliveryGateStateTests(unittest.TestCase):
    def test_plain_delivery_advances_to_packet_and_pauses_before_downstream_work(self) -> None:
        action = GATES.evaluate_delivery(gate_state())

        self.assertEqual("pause-for-human", action["action"])
        self.assertEqual("matched-view-packet", action["packet"]["id"])
        self.assertEqual("v2", action["packet"]["revision"])
        self.assertEqual("a" * 64, action["packet"]["sha256"])
        self.assertEqual("print-engineering", action["resume_point"])
        self.assertIn("brass is a printed finish", action["compromises"])
        self.assertIn("release-packaging", action["prohibited_downstream"])
        self.assertIn("hero-spec-verify", action["prohibited_downstream"])

    def test_explicit_approval_resumes_same_delivery_through_closing_gates(self) -> None:
        state = gate_state()
        updated, action = GATES.apply_decision(
            state,
            GATES.GateDecision(intent="approved", exact_response="Approved."),
        )

        self.assertEqual("approved", updated["gates"][0]["state"])
        self.assertEqual("Approved.", updated["gates"][0]["exact_decision"])
        self.assertEqual("continue-to-closing-gates", action["action"])
        self.assertEqual(
            ["completion-ledger", "cold-delivery-audit", "hero-spec-verify"],
            action["authorized_work"],
        )
        self.assertEqual("delivering", updated["delivery_status"])

    def test_explicit_approval_advances_to_next_ordered_human_gate(self) -> None:
        state = gate_state(later_gate=True)
        updated, action = GATES.apply_decision(
            state,
            GATES.GateDecision(intent="approved", exact_response="Approved."),
        )

        self.assertEqual("approved", updated["gates"][0]["state"])
        self.assertEqual("pause-for-human", action["action"])
        self.assertEqual("physical-fit-decision", action["gate_id"])
        self.assertEqual("coupon-results", action["packet"]["id"])

    def test_generic_continuation_does_not_approve_or_progress(self) -> None:
        state = gate_state()
        updated, action = GATES.apply_decision(
            state,
            GATES.GateDecision(intent="continue", exact_response="Continue."),
        )

        self.assertEqual(state, updated)
        self.assertEqual("hold", action["action"])
        self.assertEqual("generic-continuation-is-not-approval", action["reason"])
        self.assertEqual("pending", updated["gates"][0]["state"])

    def test_stale_and_ambiguous_approvals_hold(self) -> None:
        state = gate_state()
        updated, stale = GATES.apply_decision(
            state,
            GATES.GateDecision(
                intent="approved",
                exact_response="I approve v1.",
                packet_id="matched-view-packet",
                revision="v1",
                sha256="c" * 64,
            ),
        )
        self.assertEqual(state, updated)
        self.assertEqual("stale-or-mismatched-packet", stale["reason"])

        ambiguous_state = gate_state(second_live_gate=True)
        ambiguous_update, ambiguous = GATES.apply_decision(
            ambiguous_state,
            GATES.GateDecision(intent="approved", exact_response="Approved."),
        )
        self.assertEqual(ambiguous_state, ambiguous_update)
        self.assertEqual("ambiguous-live-packets", ambiguous["reason"])

    def test_revision_request_supersedes_packet_and_requires_new_revision(self) -> None:
        state = gate_state(later_gate=True)
        revised, action = GATES.apply_decision(
            state,
            GATES.GateDecision(
                intent="request-revision",
                exact_response="Revise the focal star.",
            ),
        )

        self.assertEqual("revision-requested", revised["gates"][0]["state"])
        self.assertIsNone(revised["gates"][0]["packet"])
        self.assertEqual("v2", revised["superseded_packets"][0]["revision"])
        self.assertEqual("return-for-revision", action["action"])
        self.assertIn("release-packaging", action["prohibited_downstream"])

        held_state, held = GATES.apply_decision(
            revised,
            GATES.GateDecision(intent="approved", exact_response="Approved."),
        )
        self.assertEqual(revised, held_state)
        self.assertEqual("no-current-packet", held["reason"])

        republished = GATES.publish_revision(
            revised,
            "final-visual-review",
            {"id": "matched-view-packet", "revision": "v3", "sha256": "d" * 64},
        )
        new_action = GATES.evaluate_delivery(republished)
        self.assertEqual("pause-for-human", new_action["action"])
        self.assertEqual("v3", new_action["packet"]["revision"])
        self.assertEqual("d" * 64, new_action["packet"]["sha256"])


class DeliveryGateFlowTests(unittest.TestCase):
    def run_scenario(self, scenario: str) -> tuple[dict[str, Any], Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name) / scenario
        result = subprocess.run(
            [
                sys.executable,
                str(FLOW_SCRIPT),
                "--fixture",
                str(FLOW_FIXTURE),
                "--output",
                str(output),
                "--scenario",
                scenario,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        assertions = json.loads(
            (output / "assertions.json").read_text(encoding="utf-8")
        )
        return assertions, output

    def test_cli_cold_delivery_pauses_and_approval_resumes_without_second_deliver(self) -> None:
        assertions, output = self.run_scenario("approval")

        self.assertEqual(1, assertions["deliver_command_count"])
        self.assertEqual(1, assertions["decision_event_count"])
        self.assertEqual("delivering", assertions["paused_delivery_status"])
        self.assertTrue(assertions["paused_packet_persisted"])
        self.assertTrue(assertions["paused_resume_point_persisted"])
        self.assertTrue(
            all(assertions["prohibited_downstream_absent_before_decision"].values())
        )
        self.assertEqual("continue-to-closing-gates", assertions["next_action"])
        self.assertTrue(assertions["automatic_resume_without_second_deliver"])
        self.assertTrue(assertions["resumed_kickoff_fields_persisted"])
        self.assertEqual(
            {
                "kind": "final-matched-view-approval",
                "state": "approved",
                "packet": {
                    "id": "fixture-matched-view-packet",
                    "revision": "v1",
                    "sha256": "a" * 64,
                },
                "exact_decision": "Approved.",
                "authorized_after": ["release-packaging"],
                "resume_point": "completion-ledger",
            },
            assertions["resumed_gate_record"],
        )
        paused_spec = (output / "paused-spec.md").read_text(encoding="utf-8")
        self.assertIn("status: delivering", paused_spec)
        self.assertIn("fixture-matched-view-packet", paused_spec)
        resumed_spec = (output / "resumed-spec.md").read_text(encoding="utf-8")
        for expected in (
            "final-matched-view-approval",
            "approved",
            "fixture-matched-view-packet",
            "v1",
            "a" * 64,
            "Approved.",
            "release-packaging",
            "completion-ledger",
        ):
            self.assertIn(expected, resumed_spec)
        self.assertTrue((output / "transcript.jsonl").is_file())
        self.assertTrue((output / "resumed-checkpoint.json").is_file())

    def test_cli_retains_expected_hold_and_revision_evidence(self) -> None:
        expected = {
            "generic": ("hold", "generic-continuation-is-not-approval"),
            "stale": ("hold", "stale-or-mismatched-packet"),
            "ambiguous": ("hold", "ambiguous-live-packets"),
            "revision": ("return-for-revision", None),
        }
        for scenario, (action, reason) in expected.items():
            with self.subTest(scenario=scenario):
                assertions, output = self.run_scenario(scenario)
                self.assertEqual(1, assertions["deliver_command_count"])
                self.assertEqual(action, assertions["next_action"])
                self.assertEqual(reason, assertions["next_reason"])
                self.assertFalse(assertions["automatic_resume_without_second_deliver"])
                self.assertTrue((output / "paused-checkpoint.json").is_file())
                self.assertTrue((output / "resumed-action.json").is_file())


if __name__ == "__main__":
    unittest.main()
