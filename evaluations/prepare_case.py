#!/usr/bin/env python3
"""Stage one blind input and the skill; never copy the rubric or other cases."""

import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id", choices=[f"{i:02d}" for i in range(1, 11)])
    parser.add_argument("destination", type=Path, help="New isolated directory")
    args = parser.parse_args()
    evaluation_root = Path(__file__).resolve().parent
    cases = json.loads((evaluation_root / "cases.json").read_text())
    case = next(item for item in cases if item["id"] == args.case_id)
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    source = evaluation_root.parent / "skills" / "bioinformatics-research-assistant"
    shutil.copytree(source, destination / "bioinformatics-research-assistant")
    for name, content in case["files"].items():
        (destination / name).write_text(content)
    (destination / "TASK.md").write_text(case["request"] + "\n")
    # Case 07's follow-up must be delivered only after the first result.
    print(destination)


if __name__ == "__main__":
    main()
