"""
OmX-to-Cursor Porting Validation Script
Validates converted Cursor rules/skills against original OmX prompts/skills.
Scoring rubric: 100 points per file across 8 dimensions.
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from difflib import SequenceMatcher

# ── Tool mapping dictionary ──────────────────────────────────────────────────
TOOL_MAP = {
    "ask_codex": "Task tool (subagent)",
    "AskUserQuestion": "AskQuestion tool",
    "lsp_diagnostics": "ReadLints tool",
    "ast_grep_search": "Grep tool",
    "Bash": "Shell tool",
    "bash": "Shell tool",
    "shell": "Shell tool",
    "Edit": "StrReplace tool",
    "file_edit": "StrReplace tool",
    ".omx/": ".cursor/",
    "omx explore": "Task tool with explore subagent",
    "omx team": "Task tool with parallel subagents",
}

# OmX section tags (HTML-like) used in prompt files
OMX_SECTION_TAGS = [
    "role", "hard-rules", "workflow", "output-format", "quality-criteria",
    "effort-calibration", "tool-strategy", "examples", "self-check",
    "anti-pattern", "continuation-handling", "scope-boundary",
    "default-behavior", "escalation-rules", "format-rules",
]

# Cursor equivalent section headers expected in .mdc / SKILL.md
CURSOR_SECTION_HEADERS = {
    "role": ["Role", "Identity", "Purpose"],
    "hard-rules": ["Rules", "Hard Rules", "Constraints", "Guidelines"],
    "workflow": ["Workflow", "Procedure", "Steps", "Process"],
    "output-format": ["Output Format", "Output", "Response Format"],
    "quality-criteria": ["Quality Criteria", "Quality", "Standards"],
    "effort-calibration": ["Effort", "Calibration", "Effort Calibration"],
    "tool-strategy": ["Tools", "Tool Strategy", "Tool Usage"],
    "examples": ["Examples", "Scenario Examples", "Good/Bad Examples"],
    "self-check": ["Self-Check", "Checklist", "Verification"],
    "anti-pattern": ["Anti-Patterns", "Common Mistakes", "What Not To Do"],
    "continuation-handling": ["Continuation", "Continuation Handling"],
    "scope-boundary": ["Scope", "Boundaries"],
    "default-behavior": ["Defaults", "Default Behavior"],
    "escalation-rules": ["Escalation", "Escalation Rules"],
    "format-rules": ["Format Rules", "Formatting"],
}

# Skill-specific OmX tags
OMX_SKILL_TAGS = [
    "purpose", "when-to-use", "when-not-to-use", "why-this-matters",
    "rules", "workflow", "tools", "examples", "edge-cases",
    "completion-criteria", "checklist", "appendix",
]

CURSOR_SKILL_HEADERS = {
    "purpose": ["Purpose"],
    "when-to-use": ["When to Use"],
    "when-not-to-use": ["When Not to Use"],
    "why-this-matters": ["Why This Matters", "Rationale"],
    "rules": ["Rules", "Guidelines", "Constraints"],
    "workflow": ["Workflow", "Procedure", "Steps"],
    "tools": ["Tools", "Tool Usage", "Tool Strategy"],
    "examples": ["Examples", "Scenario Examples"],
    "edge-cases": ["Edge Cases"],
    "completion-criteria": ["Completion Criteria", "Done When"],
    "checklist": ["Checklist", "Self-Check"],
    "appendix": ["Appendix", "Reference"],
}


def parse_yaml_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def extract_omx_sections(text: str) -> dict:
    """Extract content from OmX HTML-like tags."""
    sections = {}
    all_tags = OMX_SECTION_TAGS + OMX_SKILL_TAGS
    for tag in all_tags:
        pattern = rf"<{tag}>(.*?)</{tag}>"
        m = re.search(pattern, text, re.DOTALL)
        if m:
            sections[tag] = m.group(1).strip()
    return sections


def extract_cursor_sections(text: str) -> dict:
    """Extract content from Cursor markdown headers (## Section)."""
    sections = {}
    header_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(header_pattern.finditer(text))
    for i, match in enumerate(matches):
        header = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections[header] = content
    return sections


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    a_clean = re.sub(r"\s+", " ", a.lower().strip())
    b_clean = re.sub(r"\s+", " ", b.lower().strip())
    return SequenceMatcher(None, a_clean, b_clean).ratio()


def find_matching_section(omx_tag: str, cursor_sections: dict, header_map: dict) -> tuple:
    """Find the best matching Cursor section for an OmX tag."""
    expected_headers = header_map.get(omx_tag, [])
    for hdr in expected_headers:
        for cursor_hdr, content in cursor_sections.items():
            if hdr.lower() in cursor_hdr.lower():
                return cursor_hdr, content
    return None, None


def check_tool_mapping(original: str, converted: str) -> tuple:
    """Check that Codex-specific tool references are mapped to Cursor equivalents."""
    found = 0
    mapped = 0
    unmapped = []
    for codex_tool, cursor_tool in TOOL_MAP.items():
        if codex_tool in original:
            found += 1
            cursor_term = cursor_tool.split("(")[0].strip().split(" ")[0]
            if cursor_term.lower() in converted.lower() or codex_tool not in converted:
                mapped += 1
            else:
                unmapped.append(codex_tool)
    if found == 0:
        return 1.0, unmapped
    return mapped / found, unmapped


def validate_prompt(original_path: str, converted_path: str) -> dict:
    """Validate a converted prompt (.mdc) against the original OmX prompt."""
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()
    with open(converted_path, "r", encoding="utf-8") as f:
        converted = f.read()

    result = {"file": os.path.basename(converted_path), "scores": {}, "feedback": []}
    total = 0

    # 1. Frontmatter (10 pts)
    orig_fm = parse_yaml_frontmatter(original)
    conv_fm = parse_yaml_frontmatter(converted)
    fm_score = 0
    if conv_fm.get("description"):
        fm_score += 5
        if similarity(orig_fm.get("description", ""), conv_fm.get("description", "")) > 0.3:
            fm_score += 5
        else:
            result["feedback"].append("Frontmatter description doesn't closely match original intent")
    else:
        result["feedback"].append("Missing frontmatter description")
    result["scores"]["frontmatter"] = fm_score
    total += fm_score

    # 2-8: Section-based scoring
    omx_sections = extract_omx_sections(original)
    cursor_sections = extract_cursor_sections(converted)

    section_scores = {
        "role": {"max": 15, "tag": "role"},
        "hard_rules": {"max": 15, "tag": "hard-rules"},
        "workflow": {"max": 20, "tag": "workflow"},
        "output_format": {"max": 10, "tag": "output-format"},
        "examples": {"max": 10, "tag": "examples"},
    }

    for key, cfg in section_scores.items():
        tag = cfg["tag"]
        max_pts = cfg["max"]
        omx_content = omx_sections.get(tag, "")
        if not omx_content:
            result["scores"][key] = max_pts
            total += max_pts
            continue

        cursor_hdr, cursor_content = find_matching_section(tag, cursor_sections, CURSOR_SECTION_HEADERS)
        if cursor_hdr and cursor_content:
            sim = similarity(omx_content, cursor_content)
            pts = round(max_pts * min(1.0, sim + 0.3))
            pts = min(pts, max_pts)
            result["scores"][key] = pts
            if pts < max_pts * 0.8:
                result["feedback"].append(
                    f"Section '{tag}' content similarity low ({sim:.0%}). "
                    f"Original has {len(omx_content)} chars, converted has {len(cursor_content)} chars."
                )
        else:
            result["scores"][key] = 0
            result["feedback"].append(f"Missing section for OmX tag <{tag}>")
        total += result["scores"][key]

    # Tool mapping (15 pts)
    tool_ratio, unmapped = check_tool_mapping(original, converted)
    tool_pts = round(15 * tool_ratio)
    result["scores"]["tool_mapping"] = tool_pts
    total += tool_pts
    if unmapped:
        result["feedback"].append(f"Unmapped Codex tools still present: {unmapped}")

    # Completeness (5 pts)
    present_omx = len(omx_sections)
    if present_omx == 0:
        result["scores"]["completeness"] = 5
    else:
        matched = 0
        for tag in omx_sections:
            hdr, _ = find_matching_section(tag, cursor_sections, CURSOR_SECTION_HEADERS)
            if hdr:
                matched += 1
        completeness_ratio = matched / present_omx
        result["scores"]["completeness"] = round(5 * completeness_ratio)
    total += result["scores"]["completeness"]

    result["total"] = total
    result["pass"] = total >= 90
    return result


def validate_skill(original_path: str, converted_path: str) -> dict:
    """Validate a converted skill (SKILL.md) against the original OmX skill."""
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()
    with open(converted_path, "r", encoding="utf-8") as f:
        converted = f.read()

    result = {"file": os.path.basename(os.path.dirname(converted_path)), "scores": {}, "feedback": []}
    total = 0

    # 1. Frontmatter (10 pts)
    orig_fm = parse_yaml_frontmatter(original)
    conv_fm = parse_yaml_frontmatter(converted)
    fm_score = 0
    if conv_fm.get("description"):
        fm_score += 5
        if conv_fm.get("name"):
            fm_score += 5
        else:
            result["feedback"].append("Missing skill name in frontmatter")
    else:
        result["feedback"].append("Missing frontmatter description")
    result["scores"]["frontmatter"] = fm_score
    total += fm_score

    # Section scoring for skills
    omx_sections = extract_omx_sections(original)
    cursor_sections = extract_cursor_sections(converted)

    section_scores = {
        "purpose": {"max": 10, "tag": "purpose"},
        "rules": {"max": 15, "tag": "rules"},
        "workflow": {"max": 25, "tag": "workflow"},
        "examples": {"max": 10, "tag": "examples"},
    }

    for key, cfg in section_scores.items():
        tag = cfg["tag"]
        max_pts = cfg["max"]
        omx_content = omx_sections.get(tag, "")
        if not omx_content:
            result["scores"][key] = max_pts
            total += max_pts
            continue

        cursor_hdr, cursor_content = find_matching_section(tag, cursor_sections, CURSOR_SKILL_HEADERS)
        if cursor_hdr and cursor_content:
            sim = similarity(omx_content, cursor_content)
            pts = round(max_pts * min(1.0, sim + 0.3))
            pts = min(pts, max_pts)
            result["scores"][key] = pts
            if pts < max_pts * 0.8:
                result["feedback"].append(
                    f"Section '{tag}' content similarity low ({sim:.0%}). "
                    f"Original has {len(omx_content)} chars, converted has {len(cursor_content)} chars."
                )
        else:
            result["scores"][key] = 0
            result["feedback"].append(f"Missing section for OmX tag <{tag}>")
        total += result["scores"][key]

    # Tool mapping (15 pts)
    tool_ratio, unmapped = check_tool_mapping(original, converted)
    tool_pts = round(15 * tool_ratio)
    result["scores"]["tool_mapping"] = tool_pts
    total += tool_pts
    if unmapped:
        result["feedback"].append(f"Unmapped Codex tools still present: {unmapped}")

    # When to use / When not to use (10 pts)
    when_score = 0
    for tag in ["when-to-use", "when-not-to-use"]:
        if tag in omx_sections:
            hdr, content = find_matching_section(tag, cursor_sections, CURSOR_SKILL_HEADERS)
            if hdr:
                when_score += 5
            else:
                result["feedback"].append(f"Missing section for <{tag}>")
    if "when-to-use" not in omx_sections and "when-not-to-use" not in omx_sections:
        when_score = 10
    result["scores"]["when_to_use"] = when_score
    total += when_score

    # Completeness (5 pts)
    present_omx = len(omx_sections)
    if present_omx == 0:
        result["scores"]["completeness"] = 5
    else:
        matched = 0
        for tag in omx_sections:
            mapping = {**CURSOR_SECTION_HEADERS, **CURSOR_SKILL_HEADERS}
            hdr, _ = find_matching_section(tag, cursor_sections, mapping)
            if hdr:
                matched += 1
        completeness_ratio = matched / present_omx
        result["scores"]["completeness"] = round(5 * completeness_ratio)
    total += result["scores"]["completeness"]

    result["total"] = total
    result["pass"] = total >= 90
    return result


def run_validation(mode: str, source_dir: str, target_dir: str) -> dict:
    """Run validation for all files of a given mode (prompts or skills)."""
    results = []

    if mode == "prompts":
        source_path = Path(source_dir) / "prompts"
        for md_file in sorted(source_path.glob("*.md")):
            name = md_file.stem
            converted = Path(target_dir) / f"omx-{name}.mdc"
            if not converted.exists():
                results.append({
                    "file": f"omx-{name}.mdc",
                    "total": 0,
                    "pass": False,
                    "feedback": [f"Converted file not found: {converted}"],
                    "scores": {},
                })
                continue
            results.append(validate_prompt(str(md_file), str(converted)))

    elif mode == "skills":
        source_path = Path(source_dir) / "skills"
        skills_to_convert = [
            "ai-slop-cleaner", "analyze", "autopilot", "build-fix",
            "code-review", "deep-interview", "deepsearch", "frontend-ui-ux",
            "git-master", "pipeline", "plan", "ralph", "ralph-init",
            "ralplan", "review", "security-review", "tdd", "ultraqa",
            "ultrawork", "visual-verdict", "web-clone",
        ]
        for skill_name in sorted(skills_to_convert):
            orig_skill = source_path / skill_name / "SKILL.md"
            if not orig_skill.exists():
                continue
            converted = Path(target_dir) / f"omx-{skill_name}" / "SKILL.md"
            if not converted.exists():
                results.append({
                    "file": f"omx-{skill_name}",
                    "total": 0,
                    "pass": False,
                    "feedback": [f"Converted file not found: {converted}"],
                    "scores": {},
                })
                continue
            results.append(validate_skill(str(orig_skill), str(converted)))

    summary = {
        "mode": mode,
        "total_files": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "average_score": round(sum(r["total"] for r in results) / max(len(results), 1), 1),
        "results": results,
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description="Validate OmX-to-Cursor conversions")
    parser.add_argument("mode", choices=["prompts", "skills"], help="What to validate")
    default_source = str(Path(__file__).resolve().parents[2] / "_omx_source")
    parser.add_argument("--source", default=default_source, help="OmX source dir")
    parser.add_argument("--target-rules", default=r"C:\Users\khala\.cursor\rules", help="Cursor rules dir")
    parser.add_argument("--target-skills", default=r"C:\Users\khala\.cursor\skills-cursor", help="Cursor skills dir")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    target = args.target_rules if args.mode == "prompts" else args.target_skills
    summary = run_validation(args.mode, args.source, target)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {args.mode.upper()}")
        print(f"{'='*60}")
        print(f"Total: {summary['total_files']} | Passed: {summary['passed']} | Failed: {summary['failed']}")
        print(f"Average Score: {summary['average_score']}/100")
        print(f"{'='*60}\n")

        for r in summary["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            print(f"[{status}] {r['file']}: {r['total']}/100")
            if r.get("scores"):
                for k, v in r["scores"].items():
                    print(f"       {k}: {v}")
            if r.get("feedback"):
                for fb in r["feedback"]:
                    print(f"       >> {fb}")
            print()

        # Output failing files as a comma-separated list for iteration
        failing = [r["file"] for r in summary["results"] if not r["pass"]]
        if failing:
            print(f"\nFAILING FILES ({len(failing)}):")
            for f in failing:
                print(f"  - {f}")


if __name__ == "__main__":
    main()
