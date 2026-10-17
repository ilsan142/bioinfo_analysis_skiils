"""Audit the supplied split and source only; do not fit or score a model."""
import ast
import csv
import hashlib
import json
import platform
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT / "pipeline.py").read_text(encoding="utf-8")
tree = ast.parse(source)
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "evaluate")
calls = sorted((n for n in ast.walk(function) if isinstance(n, ast.Call)), key=lambda n: n.lineno)
selection = next(n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == "fit_transform")
split = next(n for n in calls if isinstance(n.func, ast.Name) and n.func.id == "train_test_split")

with (ROOT / "split.tsv").open(encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    if reader.fieldnames != ["row_id", "patient_id", "split"]:
        raise ValueError("Unexpected manifest columns")
    rows = list(reader)
if not rows or any(not row[key] for row in rows for key in ("row_id", "patient_id", "split")):
    raise ValueError("Empty manifest or missing required identifier")
if any(row["split"] not in {"train", "test"} for row in rows):
    raise ValueError("Unexpected split label")
duplicates = sorted(key for key, count in Counter(row["row_id"] for row in rows).items() if count > 1)
if duplicates:
    raise ValueError(f"Duplicate row IDs: {duplicates}")

patients_by_split = {
    group: {row["patient_id"] for row in rows if row["split"] == group}
    for group in ("train", "test")
}
patient_rows = defaultdict(lambda: {"train": [], "test": []})
for row in rows:
    patient_rows[row["patient_id"]][row["split"]].append(row["row_id"])
overlap = patients_by_split["train"] & patients_by_split["test"]
test_rows = [row for row in rows if row["split"] == "test"]
report = {
    "audit_type": "Executed manifest audit and static source inspection; no model training or scoring",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "python_version": platform.python_version(),
    "command": "python3 audit.py",
    "inputs_sha256": {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ("TASK.md", "context.md", "pipeline.py", "split.tsv")
    },
    "manifest": {
        "rows": len(rows),
        "unique_patients": len(patient_rows),
        "duplicate_row_ids": duplicates,
        "rows_per_split": dict(Counter(row["split"] for row in rows)),
        "patients_per_split": {key: len(value) for key, value in patients_by_split.items()},
        "overlapping_patient_ids": sorted(overlap),
        "overlapping_patient_count": len(overlap),
        "unseen_test_patient_ids": sorted(patients_by_split["test"] - patients_by_split["train"]),
        "test_rows_with_patient_seen_in_train": sum(row["patient_id"] in overlap for row in test_rows),
        "patient_row_membership": dict(patient_rows),
    },
    "source": {
        "feature_selection_line": selection.lineno,
        "feature_selection_expression": ast.get_source_segment(source, selection),
        "split_line": split.lineno,
        "split_expression": ast.get_source_segment(source, split),
        "selection_precedes_split": selection.lineno < split.lineno,
        "patient_id_read_in_function_body": any(
            isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id == "patient_id"
            for n in ast.walk(function)
        ),
        "manifest_referenced_in_source": "split.tsv" in source,
    },
    "limitations": [
        "No X or y provided; cannot execute evaluate, verify class balance, or estimate performance/bias/uncertainty.",
        "Manifest overlap is observed; its correspondence to an actual random split execution is unverified.",
        "Audit execution is not independent biological or predictive validation.",
    ],
}
output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
(ROOT / "audit_results.json").write_text(output, encoding="utf-8")
print(output, end="")
