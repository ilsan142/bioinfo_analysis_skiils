#!/usr/bin/env python3
"""Audit supplied values; preserve their unknown measurement scale."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

def read_tsv(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    assert rows and len(rows) > 1, f"Empty table: {name}"
    assert all(len(row) == len(rows[0]) for row in rows), f"Ragged table: {name}"
    return rows[0], rows[1:]

header, records = read_tsv("expression.tsv")
meta_header, meta_rows = read_tsv("metadata.tsv")
assert header[0] == "feature_id", "Unexpected feature ID column"
assert meta_header == ["sample_id", "condition"], "Unexpected metadata columns"
samples = header[1:]
features = [row[0] for row in records]
metadata_ids = [row[0] for row in meta_rows]
assert all(samples + features + metadata_ids), "Empty identifier"
assert len(set(samples)) == len(samples), "Duplicate matrix sample IDs"
assert len(set(features)) == len(features), "Duplicate feature IDs"
assert len(set(metadata_ids)) == len(metadata_ids), "Duplicate metadata sample IDs"
assert set(samples) == set(metadata_ids), "Matrix/metadata sample mismatch"
conditions = dict(meta_rows)
assert set(conditions.values()) == {"control", "treated"}, "Unexpected conditions"
matrix = [[float(value) for value in row[1:]] for row in records]
values = [value for row in matrix for value in row]
assert all(math.isfinite(value) for value in values), "Nonfinite value"

sample_summary = []
for index, sample in enumerate(samples):
    column = [row[index] for row in matrix]
    sample_summary.append({
        "sample_id": sample, "condition": conditions[sample],
        "min": min(column), "median": statistics.median(column),
        "max": max(column), "zero_values": sum(value == 0 for value in column),
    })
qc = {
    "python": sys.version.split()[0],
    "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                     for name in ("TASK.md", "context.md", "expression.tsv", "metadata.tsv")},
    "n_features": len(features), "n_sample_columns": len(samples),
    "sample_ids": samples, "metadata_ids": metadata_ids,
    "sample_id_join": "exact set match; metadata joined by sample_id",
    "duplicate_feature_ids": 0, "duplicate_sample_ids": 0,
    "n_missing_or_nonfinite": 0, "n_values": len(values),
    "n_negative": sum(value < 0 for value in values),
    "n_zero": sum(value == 0 for value in values),
    "n_noninteger": sum(not value.is_integer() for value in values),
    "min": min(values), "max": max(values),
    "sample_columns_per_condition": {
        group: sum(conditions[sample] == group for sample in samples)
        for group in ("control", "treated")},
    "sample_summary": sample_summary,
    "measurement_units": "unknown", "independent_biological_units": "unknown",
    "normalization_or_transform": "not applied",
    "n_features_excluded": 0, "n_samples_excluded": 0,
}
(OUT / "qc.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Command: python3 analyze.py")
print("Code SHA256:", hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
print(json.dumps(qc, ensure_ascii=False, indent=2))

# Descriptive comparisons follow the audited labels, with no paired-unit assumption.
# The difference is on the supplied numeric scale; its biological unit is unknown.
group_indices = {group: [i for i, sample in enumerate(samples)
                         if conditions[sample] == group]
                 for group in ("control", "treated")}
columns = ["feature_id", "control_n_columns", "treated_n_columns",
           "control_mean", "control_min", "control_max",
           "treated_mean", "treated_min", "treated_max",
           "treated_minus_control_mean"]
comparisons = []
for feature, row in zip(features, matrix):
    control = [row[i] for i in group_indices["control"]]
    treated = [row[i] for i in group_indices["treated"]]
    comparisons.append({
        "feature_id": feature,
        "control_n_columns": len(control), "treated_n_columns": len(treated),
        "control_mean": statistics.mean(control),
        "control_min": min(control), "control_max": max(control),
        "treated_mean": statistics.mean(treated),
        "treated_min": min(treated), "treated_max": max(treated),
        "treated_minus_control_mean": statistics.mean(treated) - statistics.mean(control),
    })
with (OUT / "group_comparison.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for record in comparisons:
        # Formatting only: the input matrix is never rounded or altered.
        writer.writerow({key: f"{value:.12g}" if isinstance(value, float) else value
                         for key, value in record.items()})
print("Descriptive comparison (unknown input units):")
print((OUT / "group_comparison.tsv").read_text(encoding="utf-8"), end="")
print("No filtering, imputation, rounding of inputs, normalization, or transformation.")
print("No hypothesis tests, p-values, FDR, confidence intervals, or fold changes calculated.")
