#!/usr/bin/env python3
"""Validate production-relief, paintability, and physical-optics evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_MODES = {
    "single-color-hand-painted",
    "multi-color-or-material",
    "separate-colored-parts",
    "physical-illumination-or-translucency",
    "presentation-only",
}
PRODUCTION_BOUNDARY_TYPES = {"raised", "recessed", "groove", "separate-part"}
NON_GEOMETRY_EVIDENCE = {
    "shader-only",
    "texture-only",
    "material-assignment",
    "emission",
    "compositor-effect",
}
PRESENTATION_PREFIX = "PRESENTATION_"
NEUTRAL_RENDER_ROLES = {"matched-composition", "focused-legibility"}
LEGIBILITY_REQUIREMENTS = {"standard", "focused-detail"}
PROHIBITED_NEUTRAL_EFFECTS = {
    "painted-material-contrast",
    "emission",
    "bloom",
    "textures",
    "compositor-effects",
    "presentation-only-geometry",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return []
    return value


def _text(value: Any, label: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
        return ""
    return value.strip()


def _sha256(value: Any, label: str, errors: list[str]) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(character not in "0123456789abcdef" for character in value)
    ):
        errors.append(f"{label} must be a lowercase SHA-256 digest")
        return ""
    return value


def _sha256_map(value: Any, label: str, errors: list[str]) -> dict[str, str]:
    item = _object(value, label, errors)
    result: dict[str, str] = {}
    for key, digest in item.items():
        if not isinstance(key, str) or not key.strip():
            errors.append(f"{label} keys must be non-empty strings")
            continue
        result[key] = _sha256(digest, f"{label}.{key}", errors)
    return result


def _unique_ids(items: list[Any], label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(items):
        item = _object(value, f"{label}[{index}]", errors)
        item_id = _text(item.get("id"), f"{label}[{index}].id", errors)
        if item_id:
            if item_id in indexed:
                errors.append(f"duplicate {label} id: {item_id}")
            else:
                indexed[item_id] = item
    return indexed


def _artifact(root: Path, value: Any, label: str, errors: list[str]) -> str:
    item = _object(value, label, errors)
    relative = _text(item.get("path"), f"{label}.path", errors)
    expected = item.get("sha256")
    if not relative:
        return ""
    candidate = Path(relative)
    if candidate.is_absolute():
        errors.append(f"{label}.path must be repository-relative: {relative}")
        return relative
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        errors.append(f"{label}.path escapes project root: {relative}")
        return relative
    if not resolved.is_file():
        errors.append(f"{label}.path does not exist: {relative}")
        return relative
    if not _sha256(expected, f"{label}.sha256", errors):
        return relative
    actual = sha256_file(resolved)
    if actual != expected:
        errors.append(
            f"{label}.sha256 is stale for {relative}: expected {expected}, current {actual}"
        )
    return relative


def validate_record(root: Path, record_path: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    record_path = record_path if record_path.is_absolute() else root / record_path
    record_path = record_path.resolve()
    try:
        record_path.relative_to(root)
    except ValueError:
        return [f"record path escapes project root: {record_path}"]
    try:
        document = json.loads(record_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"record does not exist: {record_path}"]
    except json.JSONDecodeError as exc:
        return [f"record is not valid JSON: {exc}"]
    if not isinstance(document, dict):
        return ["record root must be an object"]
    schema_version = document.get("schema_version")
    if schema_version not in {1, 2}:
        errors.append("schema_version must be 1 or 2")

    resolution = _object(
        document.get("finish_mode_resolution"), "finish_mode_resolution", errors
    )
    if resolution.get("status") != "resolved":
        errors.append("finish_mode_resolution.status must be 'resolved'")
    if resolution.get("source") not in {"user-brief", "user-answer", "explicit-spec"}:
        errors.append(
            "finish_mode_resolution.source must be user-brief, user-answer, or explicit-spec"
        )
    _text(
        resolution.get("evidence"), "finish_mode_resolution.evidence", errors
    )
    modes = _list(resolution.get("modes"), "finish_mode_resolution.modes", errors)
    normalized_modes = {
        mode for mode in modes if isinstance(mode, str) and mode in ALLOWED_MODES
    }
    if len(normalized_modes) != len(modes) or not normalized_modes:
        errors.append(
            "finish_mode_resolution.modes must contain unique supported finish modes"
        )

    properties = _unique_ids(
        _list(document.get("governed_properties"), "governed_properties", errors),
        "governed_properties",
        errors,
    )
    production_properties: set[str] = set()
    finish_plan_properties: set[str] = set()
    optical_properties: set[str] = set()
    focused_detail_properties: set[str] = set()
    declared_transitions: dict[str, set[str]] = {}
    for property_id, item in properties.items():
        authority = item.get("authority")
        if authority not in {"production-geometry", "finish-plan", "physical-optics"}:
            errors.append(
                f"governed property {property_id} has unsupported authority: {authority}"
            )
        elif authority == "production-geometry":
            production_properties.add(property_id)
            if schema_version == 2:
                legibility_requirement = item.get("legibility_requirement")
                if legibility_requirement not in LEGIBILITY_REQUIREMENTS:
                    errors.append(
                        f"governed property {property_id}.legibility_requirement must be standard or focused-detail"
                    )
                elif legibility_requirement == "focused-detail":
                    focused_detail_properties.add(property_id)
            transition_ids = _list(
                item.get("paint_transition_ids"),
                f"governed property {property_id}.paint_transition_ids",
                errors,
            )
            transition_set = {
                transition_id
                for transition_id in transition_ids
                if isinstance(transition_id, str) and transition_id.strip()
            }
            if len(transition_set) != len(transition_ids) or not transition_set:
                errors.append(
                    f"governed property {property_id}.paint_transition_ids must contain unique non-empty ids"
                )
            declared_transitions[property_id] = transition_set
        elif authority == "finish-plan":
            finish_plan_properties.add(property_id)
        elif authority == "physical-optics":
            optical_properties.add(property_id)
        _text(item.get("description"), f"governed property {property_id}.description", errors)

    _artifact(root, document.get("source_artifact"), "source_artifact", errors)

    objects = _unique_ids(
        _list(document.get("source_objects"), "source_objects", errors),
        "source_objects",
        errors,
    )
    for object_id, item in objects.items():
        name = _text(item.get("name"), f"source object {object_id}.name", errors)
        classification = item.get("classification")
        if classification not in {"production", "presentation"}:
            errors.append(
                f"source object {object_id}.classification must be production or presentation"
            )
        if name.startswith(PRESENTATION_PREFIX) and classification == "production":
            errors.append(
                f"source object {object_id} uses {PRESENTATION_PREFIX} naming and cannot be production evidence"
            )

    export_parts = _unique_ids(
        _list(document.get("export_parts"), "export_parts", errors),
        "export_parts",
        errors,
    )
    export_part_objects: dict[str, set[str]] = {}
    for part_id, item in export_parts.items():
        if item.get("export_included") is not True:
            errors.append(f"export part {part_id} is not included in production exports")
        _artifact(root, item.get("export_artifact"), f"export part {part_id}.export_artifact", errors)
        included_object_ids = _list(
            item.get("included_object_ids"),
            f"export part {part_id}.included_object_ids",
            errors,
        )
        export_part_objects[part_id] = {
            object_id for object_id in included_object_ids if isinstance(object_id, str)
        }
        if not included_object_ids:
            errors.append(f"export part {part_id} must identify included source objects")
        for object_id in included_object_ids:
            source = objects.get(object_id)
            if source is None:
                errors.append(
                    f"export part {part_id} references unknown source object {object_id}"
                )
            elif source.get("classification") != "production" or str(
                source.get("name", "")
            ).startswith(PRESENTATION_PREFIX):
                errors.append(
                    f"export part {part_id} includes presentation-only object {object_id}"
                )
        round_trip = _object(
            item.get("round_trip"), f"export part {part_id}.round_trip", errors
        )
        if round_trip.get("verified") is not True:
            errors.append(f"export part {part_id} lacks verified round-trip evidence")
        _artifact(
            root,
            round_trip.get("artifact"),
            f"export part {part_id}.round_trip.artifact",
            errors,
        )
        _text(
            round_trip.get("inspection"),
            f"export part {part_id}.round_trip.inspection",
            errors,
        )

    neutral_renders = _unique_ids(
        _list(document.get("neutral_production_renders"), "neutral_production_renders", errors),
        "neutral_production_renders",
        errors,
    )
    neutral_render_objects: dict[str, set[str]] = {}
    neutral_render_properties: dict[str, set[str]] = {}
    focused_detail_covered: set[str] = set()
    matched_render_ids: set[str] = set()
    for render_id, item in neutral_renders.items():
        _artifact(root, item, f"neutral render {render_id}", errors)
        if item.get("neutral_single_color") is not True:
            errors.append(f"neutral render {render_id} is not neutral single-color evidence")
        if item.get("production_only") is not True:
            errors.append(f"neutral render {render_id} is not production-only evidence")
        included_ids = _list(
            item.get("included_object_ids"),
            f"neutral render {render_id}.included_object_ids",
            errors,
        )
        if not included_ids:
            errors.append(f"neutral render {render_id} must identify included production objects")
        neutral_render_objects[render_id] = {
            object_id for object_id in included_ids if isinstance(object_id, str)
        }
        for object_id in included_ids:
            source = objects.get(object_id)
            if source is None:
                errors.append(
                    f"neutral render {render_id} references unknown source object {object_id}"
                )
            elif source.get("classification") != "production" or str(
                source.get("name", "")
            ).startswith(PRESENTATION_PREFIX):
                errors.append(
                    f"neutral render {render_id} includes presentation-only object {object_id}"
                )
        if schema_version == 2:
            role = item.get("role")
            if role not in NEUTRAL_RENDER_ROLES:
                errors.append(
                    f"neutral render {render_id}.role must be matched-composition or focused-legibility"
                )
            elif role == "matched-composition":
                matched_render_ids.add(render_id)
            property_ids = _list(
                item.get("property_ids"),
                f"neutral render {render_id}.property_ids",
                errors,
            )
            covered = {
                property_id for property_id in property_ids if isinstance(property_id, str)
            }
            neutral_render_properties[render_id] = covered
            if not property_ids:
                errors.append(
                    f"neutral render {render_id} must identify covered production properties"
                )
            for property_id in property_ids:
                if property_id not in production_properties:
                    errors.append(
                        f"neutral render {render_id} references unknown production property {property_id}"
                    )
            if role == "focused-legibility":
                focused_detail_covered.update(covered & focused_detail_properties)
            _text(item.get("review_scale"), f"neutral render {render_id}.review_scale", errors)
            _text(item.get("framing"), f"neutral render {render_id}.framing", errors)
            if item.get("neutral_nondescriptive_material") is not True:
                errors.append(
                    f"neutral render {render_id} does not use one neutral non-descriptive material"
                )
            if item.get("subject_background_separation") is not True:
                errors.append(
                    f"neutral render {render_id} lacks subject/background tonal separation"
                )
            if item.get("legibility_status") != "readable":
                errors.append(
                    f"neutral render {render_id}.legibility_status must be readable"
                )
            if item.get("prohibited_effects_excluded") is not True:
                errors.append(
                    f"neutral render {render_id} lacks prohibited-effect exclusions"
                )
            applied_effects = _list(
                item.get("applied_effects"),
                f"neutral render {render_id}.applied_effects",
                errors,
            )
            prohibited = sorted(
                effect
                for effect in applied_effects
                if effect in PROHIBITED_NEUTRAL_EFFECTS
            )
            if prohibited:
                errors.append(
                    f"neutral render {render_id} uses prohibited presentation effects: {prohibited}"
                )

    if schema_version == 2:
        if not matched_render_ids:
            errors.append("neutral production evidence lacks a matched-composition render")
        covered_properties = set().union(*neutral_render_properties.values()) if neutral_render_properties else set()
        missing_render_coverage = sorted(production_properties - covered_properties)
        if missing_render_coverage:
            errors.append(
                f"production properties lack neutral render coverage: {missing_render_coverage}"
            )
        missing_detail = sorted(focused_detail_properties - focused_detail_covered)
        if missing_detail:
            errors.append(
                f"focused-detail properties lack focused legibility evidence: {missing_detail}"
            )

        packet = _object(
            document.get("neutral_evidence_packet"),
            "neutral_evidence_packet",
            errors,
        )
        _artifact(
            root,
            packet,
            "neutral_evidence_packet",
            errors,
        )
        preflight = _object(
            document.get("legibility_preflight"), "legibility_preflight", errors
        )
        _artifact(root, preflight.get("artifact"), "legibility_preflight.artifact", errors)
        auditor_id = _text(
            preflight.get("auditor_id"), "legibility_preflight.auditor_id", errors
        )
        builder_id = _text(
            preflight.get("builder_id"), "legibility_preflight.builder_id", errors
        )
        if auditor_id and builder_id and auditor_id == builder_id:
            errors.append("legibility_preflight auditor must be independent from builder")
        _text(preflight.get("run_id"), "legibility_preflight.run_id", errors)
        status = preflight.get("status")
        if status != "pass":
            errors.append(
                f"legibility_preflight.status must be pass before scoring, got {status}"
            )
        if preflight.get("scores_or_classifications_assigned_before_preflight") is not False:
            errors.append(
                "legibility_preflight must occur before scores or classifications are assigned"
            )
        packet_sha256 = _sha256(
            preflight.get("packet_sha256"),
            "legibility_preflight.packet_sha256",
            errors,
        )
        current_packet_sha256 = packet.get("sha256")
        if packet_sha256 and packet_sha256 != current_packet_sha256:
            errors.append(
                "legibility_preflight.packet_sha256 does not bind the current neutral evidence packet"
            )
        reviewed_render_hashes = _sha256_map(
            preflight.get("reviewed_render_hashes"),
            "legibility_preflight.reviewed_render_hashes",
            errors,
        )
        current_render_hashes = {
            render_id: item.get("sha256") for render_id, item in neutral_renders.items()
        }
        unknown_bound_render_ids = sorted(
            set(reviewed_render_hashes) - set(current_render_hashes)
        )
        missing_bound_render_ids = sorted(
            set(current_render_hashes) - set(reviewed_render_hashes)
        )
        if unknown_bound_render_ids:
            errors.append(
                f"legibility_preflight.reviewed_render_hashes has unknown render IDs: {unknown_bound_render_ids}"
            )
        if missing_bound_render_ids:
            errors.append(
                f"legibility_preflight.reviewed_render_hashes lacks current render IDs: {missing_bound_render_ids}"
            )
        for render_id in sorted(set(current_render_hashes) & set(reviewed_render_hashes)):
            if reviewed_render_hashes[render_id] != current_render_hashes[render_id]:
                errors.append(
                    f"legibility_preflight reviewed hash does not bind current neutral render {render_id}"
                )
        reviewed_render_ids = set(
            value
            for value in _list(
                preflight.get("reviewed_render_ids"),
                "legibility_preflight.reviewed_render_ids",
                errors,
            )
            if isinstance(value, str)
        )
        reviewed_property_ids = set(
            value
            for value in _list(
                preflight.get("reviewed_property_ids"),
                "legibility_preflight.reviewed_property_ids",
                errors,
            )
            if isinstance(value, str)
        )
        unknown_render_ids = sorted(reviewed_render_ids - set(neutral_renders))
        unknown_property_ids = sorted(reviewed_property_ids - production_properties)
        if unknown_render_ids:
            errors.append(
                f"legibility_preflight references unknown neutral renders: {unknown_render_ids}"
            )
        if unknown_property_ids:
            errors.append(
                f"legibility_preflight references unknown production properties: {unknown_property_ids}"
            )
        missing_preflight_renders = sorted(set(neutral_renders) - reviewed_render_ids)
        missing_preflight_properties = sorted(production_properties - reviewed_property_ids)
        if missing_preflight_renders:
            errors.append(
                f"legibility_preflight does not cover current neutral renders: {missing_preflight_renders}"
            )
        if missing_preflight_properties:
            errors.append(
                f"legibility_preflight does not cover production properties: {missing_preflight_properties}"
            )
        affected_render_ids = _list(
            preflight.get("affected_render_ids"),
            "legibility_preflight.affected_render_ids",
            errors,
        )
        affected_property_ids = _list(
            preflight.get("affected_property_ids"),
            "legibility_preflight.affected_property_ids",
            errors,
        )
        if status == "pass" and (affected_render_ids or affected_property_ids):
            errors.append(
                "passing legibility_preflight must not list affected renders or properties"
            )

        revision = _object(
            document.get("evidence_revision"), "evidence_revision", errors
        )
        change_type = revision.get("change_type")
        if change_type not in {"initial", "evidence-only-rerender", "geometry-change"}:
            errors.append(
                "evidence_revision.change_type must be initial, evidence-only-rerender, or geometry-change"
            )
        if change_type == "evidence-only-rerender":
            if revision.get("geometry_changed") is not False:
                errors.append(
                    "evidence-only rerender cannot declare geometry changes"
                )
            if revision.get("fresh_full_audit_required") is not True:
                errors.append(
                    "evidence-only rerender requires evidence_revision.fresh_full_audit_required true"
                )
            previous_source_sha256 = _sha256(
                revision.get("previous_source_sha256"),
                "evidence_revision.previous_source_sha256",
                errors,
            )
            current_source_sha256 = _object(
                document.get("source_artifact"), "source_artifact", errors
            ).get("sha256")
            if previous_source_sha256 and previous_source_sha256 != current_source_sha256:
                errors.append(
                    "evidence-only rerender changed the source artifact hash"
                )
            previous_export_hashes = _sha256_map(
                revision.get("previous_export_hashes"),
                "evidence_revision.previous_export_hashes",
                errors,
            )
            current_export_hashes = {
                part_id: _object(
                    item.get("export_artifact"),
                    f"export part {part_id}.export_artifact",
                    errors,
                ).get("sha256")
                for part_id, item in export_parts.items()
            }
            if previous_export_hashes != current_export_hashes:
                errors.append(
                    "evidence-only rerender previous export hashes must exactly match current exports"
                )
            previous_render_hashes = _sha256_map(
                revision.get("previous_render_hashes"),
                "evidence_revision.previous_render_hashes",
                errors,
            )
            if set(previous_render_hashes) != set(current_render_hashes):
                errors.append(
                    "evidence-only rerender previous render hashes must cover exactly the current render IDs"
                )
            refreshed_render_ids = {
                value
                for value in _list(
                    revision.get("refreshed_render_ids"),
                    "evidence_revision.refreshed_render_ids",
                    errors,
                )
                if isinstance(value, str)
            }
            if not refreshed_render_ids:
                errors.append(
                    "evidence-only rerender must identify at least one refreshed render"
                )
            unknown_refreshed = sorted(refreshed_render_ids - set(current_render_hashes))
            if unknown_refreshed:
                errors.append(
                    f"evidence-only rerender references unknown refreshed renders: {unknown_refreshed}"
                )
            for render_id in sorted(set(previous_render_hashes) & set(current_render_hashes)):
                changed = previous_render_hashes[render_id] != current_render_hashes[render_id]
                if render_id in refreshed_render_ids and not changed:
                    errors.append(
                        f"evidence-only rerender {render_id} is marked refreshed but its hash is unchanged"
                    )
                if render_id not in refreshed_render_ids and changed:
                    errors.append(
                        f"evidence-only rerender {render_id} hash changed without being marked refreshed"
                    )
            previous_packet_sha256 = _sha256(
                revision.get("previous_packet_sha256"),
                "evidence_revision.previous_packet_sha256",
                errors,
            )
            if previous_packet_sha256 and previous_packet_sha256 == current_packet_sha256:
                errors.append(
                    "evidence-only rerender packet hash must change"
                )
        elif change_type == "geometry-change" and revision.get("geometry_changed") is not True:
            errors.append("geometry-change revision must declare geometry_changed true")

    finish_plans = _list(document.get("finish_plans", []), "finish_plans", errors)
    finish_plan_covered: set[str] = set()
    for index, value in enumerate(finish_plans):
        item = _object(value, f"finish_plans[{index}]", errors)
        _artifact(root, item, f"finish_plans[{index}]", errors)
        if item.get("evidence_role") != "finish-plan":
            errors.append(f"finish_plans[{index}] must be labeled evidence_role 'finish-plan'")
        property_ids = _list(
            item.get("property_ids"), f"finish_plans[{index}].property_ids", errors
        )
        if not property_ids:
            errors.append(f"finish_plans[{index}] must identify governed finish-plan properties")
        for property_id in property_ids:
            if property_id not in finish_plan_properties:
                errors.append(
                    f"finish_plans[{index}] references non-finish-plan property: {property_id}"
                )
            else:
                finish_plan_covered.add(property_id)

    missing_finish_plans = sorted(finish_plan_properties - finish_plan_covered)
    if missing_finish_plans:
        errors.append(
            f"finish-plan properties lack labeled finish-plan evidence: {missing_finish_plans}"
        )

    boundaries = _list(document.get("paint_boundaries"), "paint_boundaries", errors)
    covered_properties: set[str] = set()
    seen_transitions: set[str] = set()
    observed_transitions: dict[str, set[str]] = {
        property_id: set() for property_id in production_properties
    }
    for index, value in enumerate(boundaries):
        item = _object(value, f"paint_boundaries[{index}]", errors)
        transition_id = _text(
            item.get("id"), f"paint_boundaries[{index}].id", errors
        )
        if transition_id:
            if transition_id in seen_transitions:
                errors.append(f"duplicate paint boundary id: {transition_id}")
            seen_transitions.add(transition_id)
        property_id = _text(
            item.get("property_id"),
            f"paint boundary {transition_id}.property_id",
            errors,
        )
        if property_id not in production_properties:
            errors.append(
                f"paint boundary {transition_id} does not map a production-governed property: {property_id}"
            )
        else:
            covered_properties.add(property_id)
            if transition_id:
                observed_transitions[property_id].add(transition_id)
                if transition_id not in declared_transitions.get(property_id, set()):
                    errors.append(
                        f"paint boundary {transition_id} is not declared by governed property {property_id}"
                    )
        object_id = _text(
            item.get("source_object_id"),
            f"paint boundary {transition_id}.source_object_id",
            errors,
        )
        source = objects.get(object_id)
        if source is None:
            errors.append(f"paint boundary {transition_id} references unknown source object {object_id}")
        elif source.get("classification") != "production" or str(
            source.get("name", "")
        ).startswith(PRESENTATION_PREFIX):
            errors.append(
                f"paint boundary {transition_id} is supported only by presentation geometry {object_id}"
            )
        part_id = _text(
            item.get("export_part_id"),
            f"paint boundary {transition_id}.export_part_id",
            errors,
        )
        if part_id not in export_parts:
            errors.append(f"paint boundary {transition_id} references unknown export part {part_id}")
        elif export_parts[part_id].get("export_included") is not True:
            errors.append(f"paint boundary {transition_id} uses export-excluded part {part_id}")
        elif object_id not in export_part_objects.get(part_id, set()):
            errors.append(
                f"paint boundary {transition_id} source object {object_id} is absent from export part {part_id}"
            )
        evidence_kind = item.get("evidence_kind")
        if evidence_kind in NON_GEOMETRY_EVIDENCE or evidence_kind not in {
            "geometry",
            "separate-part",
        }:
            errors.append(
                f"paint boundary {transition_id} uses non-geometric evidence: {evidence_kind}"
            )
        boundary_type = item.get("boundary_type")
        if boundary_type not in PRODUCTION_BOUNDARY_TYPES:
            errors.append(
                f"paint boundary {transition_id}.boundary_type must be raised, recessed, groove, or separate-part"
            )
        dimensions = _object(
            item.get("dimensions"), f"paint boundary {transition_id}.dimensions", errors
        )
        if not dimensions or not all(
            type(value) in {int, float} and value > 0
            for value in dimensions.values()
        ):
            errors.append(
                f"paint boundary {transition_id}.dimensions must contain positive numeric measurements"
            )
        process = _object(
            item.get("process"), f"paint boundary {transition_id}.process", errors
        )
        _text(process.get("kind"), f"paint boundary {transition_id}.process.kind", errors)
        _text(
            process.get("tool_or_resolution"),
            f"paint boundary {transition_id}.process.tool_or_resolution",
            errors,
        )
        _text(
            process.get("viability_evidence"),
            f"paint boundary {transition_id}.process.viability_evidence",
            errors,
        )
        _text(item.get("brush_access"), f"paint boundary {transition_id}.brush_access", errors)
        _text(item.get("masking_access"), f"paint boundary {transition_id}.masking_access", errors)
        render_ids = _list(
            item.get("neutral_render_ids"),
            f"paint boundary {transition_id}.neutral_render_ids",
            errors,
        )
        if not render_ids:
            errors.append(f"paint boundary {transition_id} lacks neutral render evidence")
        for render_id in render_ids:
            if render_id not in neutral_renders:
                errors.append(
                    f"paint boundary {transition_id} references unknown neutral render {render_id}"
                )
            elif object_id not in neutral_render_objects.get(render_id, set()):
                errors.append(
                    f"paint boundary {transition_id} source object {object_id} is absent from neutral render {render_id}"
                )
        if part_id in export_parts:
            round_trip = _object(export_parts[part_id].get("round_trip"), "round_trip", errors)
            if round_trip.get("verified") is not True:
                errors.append(
                    f"paint boundary {transition_id} lacks verified round-trip evidence"
                )

    missing = sorted(production_properties - covered_properties)
    if missing:
        errors.append(f"production-governed properties lack paint-boundary coverage: {missing}")
    for property_id in sorted(production_properties):
        declared = declared_transitions.get(property_id, set())
        observed = observed_transitions.get(property_id, set())
        missing_transitions = sorted(declared - observed)
        unexpected_transitions = sorted(observed - declared)
        if missing_transitions:
            errors.append(
                f"governed property {property_id} has declared paint transitions without boundary records: {missing_transitions}"
            )
        if unexpected_transitions:
            errors.append(
                f"governed property {property_id} has undeclared paint-boundary records: {unexpected_transitions}"
            )

    optical_evidence = _list(
        document.get("physical_optical_evidence", []),
        "physical_optical_evidence",
        errors,
    )
    optical_covered: set[str] = set()
    for index, value in enumerate(optical_evidence):
        item = _object(value, f"physical_optical_evidence[{index}]", errors)
        property_id = _text(
            item.get("property_id"),
            f"physical_optical_evidence[{index}].property_id",
            errors,
        )
        if property_id not in optical_properties:
            errors.append(
                f"physical optical evidence references non-optical property: {property_id}"
            )
        else:
            optical_covered.add(property_id)
        evidence_kind = item.get("evidence_kind")
        if evidence_kind != "physical-test":
            errors.append(
                f"physical optical evidence for {property_id} must be physical-test, not {evidence_kind}"
            )
        _artifact(
            root,
            item.get("light_path_artifact"),
            f"physical optical evidence {property_id}.light_path_artifact",
            errors,
        )
        _artifact(
            root,
            item.get("test_artifact"),
            f"physical optical evidence {property_id}.test_artifact",
            errors,
        )
        _text(
            item.get("test_conditions"),
            f"physical optical evidence {property_id}.test_conditions",
            errors,
        )
    missing_optical = sorted(optical_properties - optical_covered)
    if missing_optical:
        errors.append(f"physical-optics properties lack physical-test evidence: {missing_optical}")

    if (
        "physical-illumination-or-translucency" in normalized_modes
        and not optical_properties
    ):
        errors.append(
            "physical-illumination-or-translucency mode requires a physical-optics governed property"
        )

    if "single-color-hand-painted" in normalized_modes and not production_properties:
        errors.append(
            "single-color-hand-painted mode requires production-governed decorative properties"
        )
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--record", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_record(args.root, args.record)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"PASS production-relief evidence: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
