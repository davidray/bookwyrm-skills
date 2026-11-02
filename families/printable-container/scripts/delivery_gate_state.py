#!/usr/bin/env python3
"""Evaluate printable-container human-gate delivery transitions."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any


PENDING_STATES = {"pending", "revision-requested"}
APPROVAL_WORDS = {"approve", "approved"}
REVISION_WORDS = {"request-revision", "revision-requested"}


class GateStateError(ValueError):
    """Raised when a durable delivery-gate record is invalid."""


@dataclass(frozen=True)
class GateDecision:
    intent: str
    exact_response: str
    packet_id: str | None = None
    revision: str | None = None
    sha256: str | None = None


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GateStateError(f"{field} must be a non-empty string")
    return value


def _live_gates(state: dict[str, Any]) -> list[dict[str, Any]]:
    gates = state.get("gates")
    if not isinstance(gates, list):
        raise GateStateError("gates must be a list")
    live: list[dict[str, Any]] = []
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            raise GateStateError(f"gates[{index}] must be an object")
        _required_text(gate.get("id"), f"gates[{index}].id")
        if gate.get("non_delegable") is not True:
            continue
        gate_state = gate.get("state")
        if gate_state not in {"pending", "approved", "revision-requested"}:
            raise GateStateError(
                f"gates[{index}].state must be pending, approved, or revision-requested"
            )
        if gate_state in PENDING_STATES:
            live.append(gate)
    return live


def _packet(gate: dict[str, Any]) -> dict[str, str]:
    packet = gate.get("packet")
    if not isinstance(packet, dict):
        raise GateStateError(f"gate {gate['id']} requires one current packet")
    return {
        "id": _required_text(packet.get("id"), f"gate {gate['id']} packet.id"),
        "revision": _required_text(
            packet.get("revision"), f"gate {gate['id']} packet.revision"
        ),
        "sha256": _required_text(
            packet.get("sha256"), f"gate {gate['id']} packet.sha256"
        ),
    }


def _pause(gate: dict[str, Any], *, reason: str = "human-decision-required") -> dict[str, Any]:
    packet = _packet(gate)
    return {
        "action": "pause-for-human",
        "reason": reason,
        "gate_id": gate["id"],
        "gate_kind": _required_text(gate.get("kind"), f"gate {gate['id']} kind"),
        "packet": packet,
        "decision_requested": _required_text(
            gate.get("decision_requested"), f"gate {gate['id']} decision_requested"
        ),
        "compromises": list(gate.get("compromises", [])),
        "approval_authorizes": list(gate.get("authorized_after", [])),
        "resume_point": _required_text(
            gate.get("resume_point"), f"gate {gate['id']} resume_point"
        ),
        "prohibited_downstream": list(gate.get("prohibited_downstream", [])),
    }


def evaluate_delivery(state: dict[str, Any]) -> dict[str, Any]:
    """Return the next observable delivery action without mutating state."""

    if state.get("delivery_status") != "delivering":
        raise GateStateError("delivery_status must remain delivering until Hero verification")
    live = _live_gates(state)
    if not live:
        return {
            "action": "continue-to-closing-gates",
            "authorized_work": list(state.get("closing_work", [])),
        }
    earliest_order = min(gate.get("order", 0) for gate in live)
    earliest = [gate for gate in live if gate.get("order", 0) == earliest_order]
    if len(earliest) != 1:
        return {
            "action": "hold",
            "reason": "ambiguous-live-packets",
            "gate_ids": [gate["id"] for gate in earliest],
        }
    gate = earliest[0]
    if gate["state"] == "revision-requested":
        return {
            "action": "return-for-revision",
            "gate_id": gate["id"],
            "resume_point": _required_text(
                gate.get("resume_point"), f"gate {gate['id']} resume_point"
            ),
            "prohibited_downstream": list(gate.get("prohibited_downstream", [])),
        }
    return _pause(gate)


def apply_decision(
    state: dict[str, Any], decision: GateDecision
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply a scoped user decision and return the updated state plus next action."""

    updated = copy.deepcopy(state)
    live = _live_gates(updated)
    if decision.intent not in APPROVAL_WORDS | REVISION_WORDS:
        return updated, {
            "action": "hold",
            "reason": "generic-continuation-is-not-approval",
        }
    earliest_order = min((gate.get("order", 0) for gate in live), default=None)
    current = [gate for gate in live if gate.get("order", 0) == earliest_order]
    if len(current) != 1:
        return updated, {
            "action": "hold",
            "reason": "ambiguous-live-packets" if len(current) > 1 else "no-current-packet",
        }
    gate = current[0]
    if gate["state"] != "pending":
        return updated, {"action": "hold", "reason": "no-current-packet"}
    packet = _packet(gate)
    supplied_identity = (decision.packet_id, decision.revision, decision.sha256)
    expected_identity = (packet["id"], packet["revision"], packet["sha256"])
    if any(value is not None for value in supplied_identity) and supplied_identity != expected_identity:
        return updated, {
            "action": "hold",
            "reason": "stale-or-mismatched-packet",
            "current_packet": packet,
        }

    record = {
        "gate_id": gate["id"],
        "packet": packet,
        "intent": decision.intent,
        "exact_response": _required_text(decision.exact_response, "exact_response"),
    }
    updated.setdefault("decision_history", []).append(record)

    if decision.intent in REVISION_WORDS:
        updated.setdefault("superseded_packets", []).append(packet)
        gate["state"] = "revision-requested"
        gate["packet"] = None
        gate["exact_decision"] = decision.exact_response
        return updated, evaluate_delivery(updated)

    gate["state"] = "approved"
    gate["exact_decision"] = decision.exact_response
    gate["approved_packet"] = packet
    gate["packet"] = None
    return updated, evaluate_delivery(updated)


def publish_revision(
    state: dict[str, Any], gate_id: str, packet: dict[str, str]
) -> dict[str, Any]:
    """Install a new current packet after a recorded revision request."""

    updated = copy.deepcopy(state)
    for gate in updated.get("gates", []):
        if gate.get("id") != gate_id:
            continue
        if gate.get("state") != "revision-requested":
            raise GateStateError(f"gate {gate_id} is not awaiting a revised packet")
        gate["packet"] = {
            "id": _required_text(packet.get("id"), "packet.id"),
            "revision": _required_text(packet.get("revision"), "packet.revision"),
            "sha256": _required_text(packet.get("sha256"), "packet.sha256"),
        }
        gate["state"] = "pending"
        return updated
    raise GateStateError(f"unknown gate: {gate_id}")
