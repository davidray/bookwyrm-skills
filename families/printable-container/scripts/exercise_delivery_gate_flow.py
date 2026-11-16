#!/usr/bin/env python3
"""Exercise a cold printable-container delivery prompt through a human gate."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from delivery_gate_state import GateDecision, apply_decision, evaluate_delivery


SCENARIOS = ("approval", "generic", "stale", "ambiguous", "revision")
PROHIBITED_FILENAMES = {
    "release-package": "release.zip",
    "cold-delivery-audit": "delivery-audit.md",
    "hero-spec-verify": "hero-verify.json",
}


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected an object in {path}")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _replace_kickoff(spec: str, body: str) -> str:
    start = spec.find("## Kickoff\n")
    if start < 0:
        raise ValueError("fixture spec lacks ## Kickoff")
    next_heading = spec.find("\n## ", start + len("## Kickoff\n"))
    if next_heading < 0:
        next_heading = len(spec)
    return spec[:start] + "## Kickoff\n\n" + body.rstrip() + "\n" + spec[next_heading:]


def _paused_kickoff(action: dict[str, Any]) -> str:
    packet = action["packet"]
    prohibited = ", ".join(action["prohibited_downstream"])
    return (
        "Exercises a pending final visual-review gate.\n\n"
        f"**Status:** delivering — paused at `{action['gate_kind']}` for packet "
        f"`{packet['id']}` revision `{packet['revision']}` (`{packet['sha256']}`).\n\n"
        f"**Pick up at:** record the explicit decision requested: "
        f"{action['decision_requested']}\n\n"
        f"→ resume at `{action['resume_point']}` after approval; while pending, prohibit: "
        f"{prohibited}."
    )


def _approved_gate(state: dict[str, Any]) -> dict[str, Any] | None:
    for gate in state.get("gates", []):
        if gate.get("state") == "approved" and isinstance(gate.get("approved_packet"), dict):
            return gate
    return None


def _resumed_kickoff(action: dict[str, Any], state: dict[str, Any]) -> str:
    if action["action"] == "continue-to-closing-gates":
        gate = _approved_gate(state)
        if gate is None:
            raise ValueError("closing-gate continuation lacks a persisted approved gate")
        packet = gate["approved_packet"]
        authorized = ", ".join(gate.get("authorized_after", []))
        work = ", ".join(action["authorized_work"])
        return (
            "Exercises a resolved final visual-review gate.\n\n"
            f"**Status:** delivering — gate `{gate['kind']}` is `{gate['state']}` for "
            f"packet `{packet['id']}` revision `{packet['revision']}` "
            f"(`{packet['sha256']}`).\n\n"
            f"**Decision:** `{gate['exact_decision']}`\n\n"
            f"**Authorized next stage:** {authorized}.\n\n"
            f"**Pick up at:** resume at `{gate['resume_point']}`, then continue "
            f"automatically through {work}; do not request another delivery command."
        )
    return (
        "Exercises a held final visual-review gate.\n\n"
        f"**Status:** delivering — `{action['action']}` because `{action.get('reason', '')}`.\n\n"
        "**Pick up at:** resolve the current gate without performing prohibited downstream work."
    )


def _decision_for(scenario: str) -> GateDecision:
    if scenario == "approval":
        return GateDecision(intent="approved", exact_response="Approved.")
    if scenario == "generic":
        return GateDecision(intent="continue", exact_response="Continue.")
    if scenario == "stale":
        return GateDecision(
            intent="approved",
            exact_response="I approve v0.",
            packet_id="fixture-matched-view-packet",
            revision="v0",
            sha256="b" * 64,
        )
    if scenario == "ambiguous":
        return GateDecision(intent="approved", exact_response="Approved.")
    return GateDecision(
        intent="request-revision",
        exact_response="Revise the focal star before approval.",
    )


def run(fixture: Path, output: Path, scenario: str) -> dict[str, Any]:
    source_spec = fixture / "fixture-spec.md"
    source_checkpoint = fixture / "checkpoint.json"
    spec = source_spec.read_text(encoding="utf-8")
    state = _read_json(source_checkpoint)
    if scenario == "ambiguous":
        duplicate = copy.deepcopy(state["gates"][0])
        duplicate["id"] = "alternate-final-review"
        duplicate["packet"] = {
            "id": "alternate-packet",
            "revision": "v1",
            "sha256": "c" * 64,
        }
        state["gates"].append(duplicate)

    output.mkdir(parents=True, exist_ok=True)
    workspace = output / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_spec, workspace / "spec.md")

    prompt = "/deliver fixture-printable-container"
    initial_action = evaluate_delivery(state)
    if initial_action["action"] not in {"pause-for-human", "hold"}:
        raise RuntimeError(f"cold delivery did not stop at a human gate: {initial_action}")
    paused_spec = spec.replace("status: planning", "status: delivering", 1)
    if initial_action["action"] == "pause-for-human":
        paused_spec = _replace_kickoff(paused_spec, _paused_kickoff(initial_action))
    else:
        paused_spec = _replace_kickoff(paused_spec, _resumed_kickoff(initial_action, state))
    (workspace / "spec.md").write_text(paused_spec, encoding="utf-8")
    _write_json(workspace / "checkpoint.json", state)
    _write_json(output / "paused-action.json", initial_action)
    (output / "paused-spec.md").write_text(paused_spec, encoding="utf-8")
    _write_json(output / "paused-checkpoint.json", state)

    prohibited = list(initial_action.get("prohibited_downstream", []))
    absent_before_decision = {
        item: not (workspace / PROHIBITED_FILENAMES[item]).exists()
        for item in prohibited
        if item in PROHIBITED_FILENAMES
    }
    if not all(absent_before_decision.values()):
        raise RuntimeError("prohibited downstream evidence exists before approval")

    transcript: list[dict[str, Any]] = [
        {"role": "user", "event": "deliver", "text": prompt},
        {"role": "assistant", "event": "gate-result", "action": initial_action},
    ]
    decision = _decision_for(scenario)
    transcript.append(
        {
            "role": "user",
            "event": "gate-decision",
            "intent": decision.intent,
            "text": decision.exact_response,
        }
    )
    updated, next_action = apply_decision(state, decision)
    transcript.append(
        {"role": "assistant", "event": "delivery-resume", "action": next_action}
    )

    resumed_spec = _replace_kickoff(paused_spec, _resumed_kickoff(next_action, updated))
    (workspace / "spec.md").write_text(resumed_spec, encoding="utf-8")
    _write_json(workspace / "checkpoint.json", updated)
    _write_json(output / "resumed-action.json", next_action)
    (output / "resumed-spec.md").write_text(resumed_spec, encoding="utf-8")
    _write_json(output / "resumed-checkpoint.json", updated)

    transcript_path = output / "transcript.jsonl"
    transcript_path.write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in transcript),
        encoding="utf-8",
    )
    resolved_gate = _approved_gate(updated)
    resolved_packet = resolved_gate.get("approved_packet") if resolved_gate else None
    resumed_gate_record = (
        {
            "kind": resolved_gate["kind"],
            "state": resolved_gate["state"],
            "packet": resolved_packet,
            "exact_decision": resolved_gate["exact_decision"],
            "authorized_after": resolved_gate["authorized_after"],
            "resume_point": resolved_gate["resume_point"],
        }
        if resolved_gate
        else None
    )
    kickoff_tokens = []
    if resumed_gate_record:
        kickoff_tokens = [
            resumed_gate_record["kind"],
            resumed_gate_record["state"],
            resolved_packet["id"],
            resolved_packet["revision"],
            resolved_packet["sha256"],
            resumed_gate_record["exact_decision"],
            *resumed_gate_record["authorized_after"],
            resumed_gate_record["resume_point"],
        ]
    assertions = {
        "scenario": scenario,
        "deliver_command_count": sum(
            event.get("event") == "deliver" for event in transcript
        ),
        "decision_event_count": sum(
            event.get("event") == "gate-decision" for event in transcript
        ),
        "paused_delivery_status": state["delivery_status"],
        "paused_packet_persisted": bool(initial_action.get("packet")),
        "paused_resume_point_persisted": bool(initial_action.get("resume_point")),
        "prohibited_downstream_absent_before_decision": absent_before_decision,
        "next_action": next_action["action"],
        "next_reason": next_action.get("reason"),
        "resumed_gate_record": resumed_gate_record,
        "resumed_kickoff_fields_persisted": bool(kickoff_tokens)
        and all(str(token) in resumed_spec for token in kickoff_tokens),
        "automatic_resume_without_second_deliver": (
            scenario == "approval"
            and next_action["action"] == "continue-to-closing-gates"
            and sum(event.get("event") == "deliver" for event in transcript) == 1
        ),
    }
    _write_json(output / "assertions.json", assertions)
    return assertions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scenario", choices=SCENARIOS, default="approval")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        assertions = run(args.fixture.resolve(), args.output.resolve(), args.scenario)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(
        f"PASS scenario={args.scenario} next={assertions['next_action']} "
        f"evidence={args.output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
