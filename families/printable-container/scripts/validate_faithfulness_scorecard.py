#!/usr/bin/env python3
"""Validate printable-container faithfulness scorecards against current artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Rubric:
    criteria: dict[str, int]
    threshold: float
    floors: dict[str, int]


RUBRICS = {
    "blockout": Rubric(
        criteria={
            "blockout-silhouette": 35,
            "blockout-composition": 30,
            "blockout-protected-function": 25,
            "blockout-assumptions": 10,
        },
        threshold=85,
        floors={
            "blockout-silhouette": 4,
            "blockout-protected-function": 4,
        },
    ),
    "decorative-integration": Rubric(
        criteria={
            "decorative-silhouette": 25,
            "decorative-focal-identity": 25,
            "decorative-motifs": 20,
            "decorative-hierarchy": 15,
            "decorative-surface-intent": 5,
            "decorative-compromises": 10,
        },
        threshold=90,
        floors={
            "decorative-silhouette": 4,
            "decorative-focal-identity": 4,
            "decorative-motifs": 4,
        },
    ),
}

PASS_FINDING_DISPOSITIONS = {"resolved", "accepted-by-user", "inapplicable"}
PASS_COMPROMISE_DECISIONS = {"accepted", "revised"}
PROPERTY_SCORE_CAPS = {"exact": 5, "minor": 4, "material": 3, "missing": 1}
REQUIRED_AUDIT_EXCLUSIONS = {
    "builder-conclusions",
    "prior-verdicts",
    "target-threshold",
    "desired-outcome",
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


def _identity(value: Any, label: str, errors: list[str]) -> str:
    identity = _object(value, label, errors).get("id")
    if not isinstance(identity, str) or not identity.strip():
        errors.append(f"{label}.id must be a non-empty string")
        return ""
    return identity.strip()


def _unique_strings(value: Any, label: str, errors: list[str]) -> set[str]:
    values = _list(value, label, errors)
    normalized = {
        item.strip() for item in values if isinstance(item, str) and item.strip()
    }
    if len(normalized) != len(values) or not normalized:
        errors.append(f"{label} must contain unique non-empty strings")
    return normalized


def _artifact_path(
    root: Path, artifact: Any, label: str, errors: list[str]
) -> tuple[str, Path] | None:
    item = _object(artifact, label, errors)
    relative = item.get("path")
    expected_hash = item.get("sha256")
    if not isinstance(relative, str) or not relative:
        errors.append(f"{label}.path must be a non-empty repository-relative path")
        return None
    candidate = Path(relative)
    if candidate.is_absolute():
        errors.append(f"{label}.path must be repository-relative: {relative}")
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        errors.append(f"{label}.path escapes project root: {relative}")
        return None
    if not resolved.is_file():
        errors.append(f"{label}.path does not exist: {relative}")
        return None
    if (
        not isinstance(expected_hash, str)
        or len(expected_hash) != 64
        or expected_hash.lower() != expected_hash
        or any(character not in "0123456789abcdef" for character in expected_hash)
    ):
        errors.append(f"{label}.sha256 must be a lowercase SHA-256 digest")
        return relative, resolved
    actual_hash = sha256_file(resolved)
    if actual_hash != expected_hash:
        errors.append(
            f"{label}.sha256 is stale for {relative}: expected {expected_hash}, current {actual_hash}"
        )
    return relative, resolved


def validate_scorecard(
    root: Path, scorecard_path: Path, required_milestone: str
) -> tuple[float | None, list[str]]:
    errors: list[str] = []
    root = root.resolve()
    scorecard_path = (
        scorecard_path if scorecard_path.is_absolute() else root / scorecard_path
    )
    scorecard_path = scorecard_path.resolve()
    try:
        scorecard_path.relative_to(root)
    except ValueError:
        return None, [f"scorecard path escapes project root: {scorecard_path}"]
    try:
        with scorecard_path.open(encoding="utf-8") as handle:
            document = json.load(handle)
    except FileNotFoundError:
        return None, [f"scorecard does not exist: {scorecard_path}"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"cannot read scorecard {scorecard_path}: {exc}"]
    document = _object(document, "scorecard", errors)

    if document.get("schema_version") != 2:
        errors.append("schema_version must equal 2")
    milestone = document.get("milestone")
    if milestone != required_milestone:
        errors.append(
            f"milestone must equal required milestone {required_milestone!r}, got {milestone!r}"
        )
    rubric = RUBRICS.get(required_milestone)
    if rubric is None:
        errors.append(f"unsupported required milestone: {required_milestone}")
        return None, errors
    if document.get("audit_scope") != "full":
        errors.append("audit_scope must be 'full'; focused audits are supplemental only")
    if document.get("verdict") != "PASS":
        errors.append("verdict must be 'PASS' for a progression gate")
    audited_at = document.get("audited_at")
    if not isinstance(audited_at, str) or not audited_at.strip():
        errors.append("audited_at must be a non-empty string")
    auditor = _identity(document.get("auditor"), "auditor", errors)
    builder = _identity(document.get("builder"), "builder", errors)
    if auditor and builder and auditor.casefold() == builder.casefold():
        errors.append("auditor must be independent from builder")

    provenance = _object(document.get("audit_provenance"), "audit_provenance", errors)
    audit_run_id = provenance.get("run_id")
    builder_run_id = provenance.get("builder_run_id")
    if not isinstance(audit_run_id, str) or not audit_run_id.strip():
        errors.append("audit_provenance.run_id must be a non-empty string")
    if not isinstance(builder_run_id, str) or not builder_run_id.strip():
        errors.append("audit_provenance.builder_run_id must be a non-empty string")
    if (
        isinstance(audit_run_id, str)
        and isinstance(builder_run_id, str)
        and audit_run_id.casefold() == builder_run_id.casefold()
    ):
        errors.append("audit provenance must be distinct from the builder run")
    if provenance.get("review_mode") != "fresh-independent":
        errors.append("audit_provenance.review_mode must be 'fresh-independent'")
    excluded_inputs = _unique_strings(
        provenance.get("input_excluded"),
        "audit_provenance.input_excluded",
        errors,
    )
    missing_exclusions = REQUIRED_AUDIT_EXCLUSIONS - excluded_inputs
    if missing_exclusions:
        errors.append(
            f"audit provenance is not threshold-blind; missing exclusions: {sorted(missing_exclusions)}"
        )
    if provenance.get("scores_recorded_before_threshold_check") is not True:
        errors.append(
            "audit_provenance.scores_recorded_before_threshold_check must be true"
        )

    artifacts = _object(document.get("artifacts"), "artifacts", errors)
    concepts = _list(artifacts.get("concepts"), "artifacts.concepts", errors)
    if not concepts:
        errors.append("artifacts.concepts must contain at least one governing reference")
    concept_paths: set[str] = set()
    for index, concept in enumerate(concepts):
        result = _artifact_path(root, concept, f"artifacts.concepts[{index}]", errors)
        if result:
            concept_paths.add(result[0])
    _artifact_path(root, artifacts.get("source"), "artifacts.source", errors)

    renders = _list(artifacts.get("renders"), "artifacts.renders", errors)
    if not renders:
        errors.append("artifacts.renders must contain at least one current-model render")
    render_ids: set[str] = set()
    for index, render in enumerate(renders):
        item = _object(render, f"artifacts.renders[{index}]", errors)
        render_id = item.get("id")
        if not isinstance(render_id, str) or not render_id:
            errors.append(f"artifacts.renders[{index}].id must be a non-empty string")
        elif render_id in render_ids:
            errors.append(f"duplicate render id: {render_id}")
        else:
            render_ids.add(render_id)
        _artifact_path(root, item, f"artifacts.renders[{index}]", errors)

    approved_views = _unique_strings(
        document.get("approved_views"), "approved_views", errors
    )

    comparisons = _list(
        document.get("comparison_artifacts"), "comparison_artifacts", errors
    )
    comparison_ids: set[str] = set()
    comparison_by_view: dict[str, str] = {}
    for index, comparison in enumerate(comparisons):
        item = _object(comparison, f"comparison_artifacts[{index}]", errors)
        comparison_id = item.get("id")
        approved_view_id = item.get("approved_view_id")
        if not isinstance(comparison_id, str) or not comparison_id.strip():
            errors.append(
                f"comparison_artifacts[{index}].id must be a non-empty string"
            )
        elif comparison_id in comparison_ids:
            errors.append(f"duplicate comparison artifact id: {comparison_id}")
        else:
            comparison_ids.add(comparison_id)
        if approved_view_id not in approved_views:
            errors.append(
                f"comparison_artifacts[{index}].approved_view_id must reference an approved view"
            )
        elif approved_view_id in comparison_by_view:
            errors.append(
                f"duplicate comparison artifact for approved view: {approved_view_id}"
            )
        elif isinstance(comparison_id, str) and comparison_id:
            comparison_by_view[approved_view_id] = comparison_id
        artifact = _artifact_path(root, item, f"comparison_artifacts[{index}]", errors)
        if artifact and Path(artifact[0]).suffix.casefold() not in {
            ".jpeg",
            ".jpg",
            ".pgm",
            ".png",
            ".ppm",
            ".webp",
        }:
            errors.append(
                f"comparison_artifacts[{index}].path must reference an image artifact"
            )
    missing_comparisons = approved_views - set(comparison_by_view)
    if missing_comparisons:
        errors.append(
            f"approved views lack comparison artifacts: {sorted(missing_comparisons)}"
        )

    matched_views = _list(document.get("matched_views"), "matched_views", errors)
    matched_view_ids: set[str] = set()
    covered_views: set[str] = set()
    for index, match in enumerate(matched_views):
        item = _object(match, f"matched_views[{index}]", errors)
        match_id = item.get("id")
        if not isinstance(match_id, str) or not match_id:
            errors.append(f"matched_views[{index}].id must be a non-empty string")
        elif match_id in matched_view_ids:
            errors.append(f"duplicate matched-view id: {match_id}")
        else:
            matched_view_ids.add(match_id)
        if item.get("concept_path") not in concept_paths:
            errors.append(
                f"matched_views[{index}].concept_path must reference a governing concept artifact"
            )
        if item.get("render_id") not in render_ids:
            errors.append(
                f"matched_views[{index}].render_id must reference a current render"
            )
        comparison_id = item.get("comparison_artifact_id")
        if comparison_id not in comparison_ids:
            errors.append(
                f"matched_views[{index}].comparison_artifact_id must reference a current comparison artifact"
            )
        if not isinstance(item.get("view"), str) or not item.get("view", "").strip():
            errors.append(
                f"matched_views[{index}].view must name the compared orientation"
            )
        if not isinstance(item.get("method"), str) or not item.get("method", "").strip():
            errors.append(
                f"matched_views[{index}].method must name the comparison method"
            )
        covers = _list(item.get("covers"), f"matched_views[{index}].covers", errors)
        valid_covers = {view for view in covers if isinstance(view, str) and view.strip()}
        if len(valid_covers) != len(covers) or not valid_covers:
            errors.append(
                f"matched_views[{index}].covers must contain non-empty approved-view IDs"
            )
        elif len(valid_covers) != 1:
            errors.append(
                f"matched_views[{index}].covers must identify exactly one approved view"
            )
        unknown = valid_covers - approved_views
        if unknown:
            errors.append(
                f"matched_views[{index}] covers unknown approved views: {sorted(unknown)}"
            )
        covered_views.update(valid_covers)
        if len(valid_covers) == 1 and comparison_id in comparison_ids:
            covered_view = next(iter(valid_covers))
            if comparison_by_view.get(covered_view) != comparison_id:
                errors.append(
                    f"matched_views[{index}] references the wrong comparison artifact for {covered_view}"
                )
    uncovered = approved_views - covered_views
    if uncovered:
        errors.append(f"approved views lack matched evidence: {sorted(uncovered)}")

    criteria = _list(document.get("criteria"), "criteria", errors)
    seen_criteria: dict[str, dict[str, Any]] = {}
    for index, criterion in enumerate(criteria):
        item = _object(criterion, f"criteria[{index}]", errors)
        criterion_id = item.get("id")
        if not isinstance(criterion_id, str) or not criterion_id:
            errors.append(f"criteria[{index}].id must be a non-empty string")
            continue
        if criterion_id in seen_criteria:
            errors.append(f"duplicate criterion id: {criterion_id}")
        seen_criteria[criterion_id] = item
    expected_ids = set(rubric.criteria)
    actual_ids = set(seen_criteria)
    if missing := expected_ids - actual_ids:
        errors.append(f"missing canonical criteria: {sorted(missing)}")
    if extra := actual_ids - expected_ids:
        errors.append(f"unexpected criteria: {sorted(extra)}")

    approved_properties = _list(
        document.get("approved_properties"), "approved_properties", errors
    )
    property_definitions: dict[str, set[str]] = {}
    for index, approved_property in enumerate(approved_properties):
        item = _object(approved_property, f"approved_properties[{index}]", errors)
        property_id = item.get("id")
        if not isinstance(property_id, str) or not property_id.strip():
            errors.append(f"approved_properties[{index}].id must be a non-empty string")
            continue
        if property_id in property_definitions:
            errors.append(f"duplicate approved property id: {property_id}")
        criterion_ids = _unique_strings(
            item.get("criterion_ids"),
            f"approved_properties[{index}].criterion_ids",
            errors,
        )
        unknown_criteria = criterion_ids - expected_ids
        if unknown_criteria:
            errors.append(
                f"approved property {property_id} references unknown criteria: {sorted(unknown_criteria)}"
            )
        if not isinstance(item.get("description"), str) or not item.get(
            "description", ""
        ).strip():
            errors.append(
                f"approved_properties[{index}].description must be a non-empty string"
            )
        property_definitions[property_id] = criterion_ids
    if not property_definitions:
        errors.append("approved_properties must contain at least one protected property")

    property_assessments = _list(
        document.get("property_assessments"), "property_assessments", errors
    )
    assessed_properties: set[str] = set()
    criterion_caps: dict[str, list[tuple[str, int]]] = {
        criterion_id: [] for criterion_id in expected_ids
    }
    for index, assessment in enumerate(property_assessments):
        item = _object(assessment, f"property_assessments[{index}]", errors)
        property_id = item.get("property_id")
        if property_id not in property_definitions:
            errors.append(
                f"property_assessments[{index}].property_id must reference an approved property"
            )
            continue
        if property_id in assessed_properties:
            errors.append(f"duplicate property assessment: {property_id}")
        assessed_properties.add(property_id)
        classification = item.get("classification")
        if classification not in PROPERTY_SCORE_CAPS:
            errors.append(
                f"property {property_id} classification must be one of {sorted(PROPERTY_SCORE_CAPS)}"
            )
            continue
        criterion_ids = _unique_strings(
            item.get("criterion_ids"),
            f"property_assessments[{index}].criterion_ids",
            errors,
        )
        if criterion_ids != property_definitions[property_id]:
            errors.append(
                f"property {property_id} criterion_ids must match its approved-property definition"
            )
        matched_ids = _unique_strings(
            item.get("matched_view_ids"),
            f"property_assessments[{index}].matched_view_ids",
            errors,
        )
        unknown_matches = matched_ids - matched_view_ids
        if unknown_matches:
            errors.append(
                f"property {property_id} references unknown matched views: {sorted(unknown_matches)}"
            )
        cited_comparisons = _unique_strings(
            item.get("comparison_artifact_ids"),
            f"property_assessments[{index}].comparison_artifact_ids",
            errors,
        )
        unknown_comparisons = cited_comparisons - comparison_ids
        if unknown_comparisons:
            errors.append(
                f"property {property_id} references unknown comparison artifacts: {sorted(unknown_comparisons)}"
            )
        if not isinstance(item.get("rationale"), str) or not item.get(
            "rationale", ""
        ).strip():
            errors.append(f"property {property_id} must include concrete rationale")
        for criterion_id in criterion_ids & expected_ids:
            criterion_caps[criterion_id].append(
                (property_id, PROPERTY_SCORE_CAPS[classification])
            )

    missing_properties = set(property_definitions) - assessed_properties
    if missing_properties:
        errors.append(
            f"approved properties lack assessments: {sorted(missing_properties)}"
        )
    extra_assessments = assessed_properties - set(property_definitions)
    if extra_assessments:
        errors.append(
            f"property assessments are not approved properties: {sorted(extra_assessments)}"
        )
    for criterion_id, caps in criterion_caps.items():
        if not caps:
            errors.append(
                f"criterion {criterion_id} has no linked approved-property assessment"
            )

    total = 0.0
    for criterion_id, expected_weight in rubric.criteria.items():
        item = seen_criteria.get(criterion_id)
        if item is None:
            continue
        if item.get("weight") != expected_weight:
            errors.append(
                f"criterion {criterion_id} weight must be {expected_weight}, got {item.get('weight')!r}"
            )
        score = item.get("score")
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 5:
            errors.append(f"criterion {criterion_id} score must be an integer from 0 through 5")
            continue
        caps = criterion_caps.get(criterion_id, [])
        if caps:
            limiting_property, score_cap = min(caps, key=lambda pair: pair[1])
            if score > score_cap:
                errors.append(
                    f"criterion {criterion_id} score {score} exceeds cap {score_cap} from property {limiting_property}"
                )
        total += score * expected_weight / 5
        evidence_ids = _list(
            item.get("evidence_view_ids"),
            f"criterion {criterion_id}.evidence_view_ids",
            errors,
        )
        if not evidence_ids:
            errors.append(f"criterion {criterion_id} must cite matched-view evidence")
        for evidence_id in evidence_ids:
            if evidence_id not in matched_view_ids:
                errors.append(
                    f"criterion {criterion_id} cites unknown matched-view evidence: {evidence_id!r}"
                )
        if not isinstance(item.get("rationale"), str) or not item.get(
            "rationale", ""
        ).strip():
            errors.append(f"criterion {criterion_id} must include concrete rationale")
        floor = rubric.floors.get(criterion_id)
        if floor is not None and score < floor:
            errors.append(f"criterion {criterion_id} score {score} is below floor {floor}")

    claimed_total = document.get("claimed_total")
    if isinstance(claimed_total, bool) or not isinstance(claimed_total, (int, float)):
        errors.append("claimed_total must be numeric")
    elif abs(float(claimed_total) - total) > 1e-9:
        errors.append(f"claimed_total {claimed_total} does not match computed total {total:g}")
    if total < rubric.threshold:
        errors.append(
            f"computed total {total:g} is below {required_milestone} threshold {rubric.threshold:g}"
        )

    findings = _list(document.get("blocking_findings"), "blocking_findings", errors)
    for index, finding in enumerate(findings):
        item = _object(finding, f"blocking_findings[{index}]", errors)
        if not isinstance(item.get("id"), str) or not item.get("id", "").strip():
            errors.append(f"blocking_findings[{index}].id must be a non-empty string")
        if item.get("disposition") not in PASS_FINDING_DISPOSITIONS:
            errors.append(f"blocking_findings[{index}] is unresolved")

    compromises = _list(document.get("compromises"), "compromises", errors)
    for index, compromise in enumerate(compromises):
        item = _object(compromise, f"compromises[{index}]", errors)
        if not isinstance(item.get("id"), str) or not item.get("id", "").strip():
            errors.append(f"compromises[{index}].id must be a non-empty string")
        if item.get("identity_changing") is not True and item.get(
            "identity_changing"
        ) is not False:
            errors.append(f"compromises[{index}].identity_changing must be boolean")
        if (
            item.get("identity_changing") is True
            and item.get("user_decision") not in PASS_COMPROMISE_DECISIONS
        ):
            errors.append(
                f"compromises[{index}] is identity-changing without an accepted or revised user decision"
            )

    visual_acs = _list(
        document.get("visual_acceptance_criteria"),
        "visual_acceptance_criteria",
        errors,
    )
    if not visual_acs:
        errors.append("visual_acceptance_criteria must contain at least one criterion")
    for index, acceptance_criterion in enumerate(visual_acs):
        item = _object(
            acceptance_criterion,
            f"visual_acceptance_criteria[{index}]",
            errors,
        )
        if not isinstance(item.get("id"), str) or not item.get("id", "").strip():
            errors.append(
                f"visual_acceptance_criteria[{index}].id must be a non-empty string"
            )
        if item.get("status") != "satisfied":
            errors.append(
                f"visual_acceptance_criteria[{index}] must be satisfied; visual requirements cannot be waived or skipped"
            )

    if required_milestone == "decorative-integration":
        final_review = _object(
            document.get("final_visual_review"), "final_visual_review", errors
        )
        if not isinstance(final_review.get("revision"), str) or not final_review.get(
            "revision", ""
        ).strip():
            errors.append("final_visual_review.revision must be a non-empty string")
        _artifact_path(
            root,
            final_review.get("packet"),
            "final_visual_review.packet",
            errors,
        )
        reviewed_comparisons = _unique_strings(
            final_review.get("comparison_artifact_ids"),
            "final_visual_review.comparison_artifact_ids",
            errors,
        )
        if reviewed_comparisons != comparison_ids:
            errors.append(
                "final_visual_review must cover every current comparison artifact exactly"
            )
        if final_review.get("decision") != "approved":
            errors.append("final_visual_review.decision must be 'approved'")
        if final_review.get("source") != "user-message":
            errors.append("final visual approval source must be 'user-message'")
        if final_review.get("recorded_by") != "orchestrator":
            errors.append(
                "final visual approval must be recorded by the orchestrator, not the builder or auditor"
            )
        if not isinstance(final_review.get("exact_response"), str) or not final_review.get(
            "exact_response", ""
        ).strip():
            errors.append("final_visual_review.exact_response must be non-empty")
        if not isinstance(final_review.get("decided_at"), str) or not final_review.get(
            "decided_at", ""
        ).strip():
            errors.append("final_visual_review.decided_at must be non-empty")

    return total, errors


def parse_requirement(value: str) -> tuple[str, Path]:
    milestone, separator, path = value.partition("=")
    if not separator or milestone not in RUBRICS or not path:
        raise argparse.ArgumentTypeError(
            "requirement must be blockout=<path> or decorative-integration=<path>"
        )
    return milestone, Path(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate hash-bound printable-container faithfulness scorecards."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="project root used to resolve scorecard and artifact paths (default: current directory)",
    )
    parser.add_argument(
        "--require",
        action="append",
        type=parse_requirement,
        default=[],
        metavar="MILESTONE=PATH",
        help="required milestone and repository-relative scorecard path; repeat for both gates",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.require:
        parser.error("at least one --require argument is required")
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR project root is not a directory: {root}", file=sys.stderr)
        return 2
    seen: set[str] = set()
    failed = False
    for milestone, path in args.require:
        if milestone in seen:
            print(f"ERROR duplicate required milestone: {milestone}", file=sys.stderr)
            failed = True
            continue
        seen.add(milestone)
        total, errors = validate_scorecard(root, path, milestone)
        display_path = path.as_posix()
        if errors:
            failed = True
            print(f"FAIL {milestone} {display_path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {milestone} {display_path} total={total:g}/100")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
