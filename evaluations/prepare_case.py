#!/usr/bin/env python3
"""Stage one blind input and the skill; never copy the rubric or other cases."""

import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id")
    parser.add_argument("destination", type=Path, help="New isolated directory")
    parser.add_argument("--suite", choices=["analysis", "planner"], default="analysis")
    args = parser.parse_args()
    evaluation_root = Path(__file__).resolve().parent
    case_root = evaluation_root if args.suite == "analysis" else evaluation_root / "planner"
    cases = json.loads((case_root / "cases.json").read_text())
    if args.case_id not in {item["id"] for item in cases}:
        parser.error(f"Unknown case {args.case_id} for {args.suite}")
    case = next(item for item in cases if item["id"] == args.case_id)
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    skill_name = "bioinformatics-research-assistant" if args.suite == "analysis" else "bioinformatics-analysis-planner"
    source = evaluation_root.parent / "skills" / skill_name
    shutil.copytree(source, destination / skill_name)
    for name, content in case["files"].items():
        (destination / name).write_text(content)
    (destination / "TASK.md").write_text(case["request"] + "\n")
    # Case 07's follow-up must be delivered only after the first result.
    print(destination)


if __name__ == "__main__":
    main()
