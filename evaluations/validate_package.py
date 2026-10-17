#!/usr/bin/env python3
"""Validate packaging and evaluation inputs, not scientific or agent behavior."""

import json
import re
from pathlib import Path

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "bioinformatics-research-assistant"
    content = (skill / "SKILL.md").read_text()
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    assert match, "Missing YAML frontmatter"
    fields = yaml.safe_load(match.group(1))
    assert set(fields) == {"name", "description"}, "Unexpected shared metadata"
    assert fields["name"] == skill.name
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"])
    assert 1 <= len(fields["name"]) <= 64
    assert isinstance(fields["description"], str)
    assert 1 <= len(fields["description"]) <= 1024
    print("PASS: name, description, directory and shared metadata")

    skill_documents = list(skill.rglob("*.md"))
    for path in skill_documents:
        assert not re.search(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3]", path.read_text()), f"Untranslated Korean in distributed skill: {path}"
    print("PASS: distributed skill documents contain no untranslated Korean text")

    documents = skill_documents + [root / "README.md", root / "README.ko.md", root / "evaluations" / "rubric.md"]
    for report_name in ("REPORT.md", "ENGLISH_EDITION.md", "NOTEBOOK_WORKFLOW.md"):
        report = root / "evaluations" / report_name
        if report.exists():
            documents.append(report)
    link_count = 0
    for path in documents:
        body = path.read_text()
        assert "[TODO:" not in body, f"Unfinished scaffold: {path}"
        assert not any(line.rstrip() != line for line in body.splitlines()), f"Trailing spaces: {path}"
        fence = None
        for line in body.splitlines():
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if marker:
                if fence is None:
                    fence = marker.group(1)
                elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
                    fence = None
        assert fence is None, f"Unclosed Markdown fence: {path}"
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
            if re.match(r"https?://|#", target):
                continue
            local = target.split("#", 1)[0]
            assert (path.parent / local).exists(), f"Broken local link: {path}: {target}"
            link_count += 1
    print(f"PASS: {len(documents)} documents, {link_count} local links, fences and whitespace")

    cases = json.loads((root / "evaluations" / "cases.json").read_text())
    assert [case["id"] for case in cases] == [f"{i:02d}" for i in range(1, 11)]
    for case in cases:
        assert isinstance(case["request"], str) and case["request"]
        assert isinstance(case["files"], dict)
        for name, value in case["files"].items():
            assert Path(name).name == name and name not in {".", ".."}
            assert isinstance(value, str)
    assert cases[6]["followup"]
    print("PASS: 10 distinct task inputs; case 07 has a staged correction")
    print("NOT TESTED HERE: agent behavior, statistical validity, product discovery")


if __name__ == "__main__":
    main()
