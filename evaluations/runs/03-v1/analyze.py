"""Audit the supplied synthetic log2 intensities; do not fit a confounded effect."""
import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

def read_tsv(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.reader(handle, delimiter="\t"))

metadata_rows = read_tsv("metadata.tsv")
assert metadata_rows[0] == ["sample_id", "donor_id", "condition", "batch"]
assert all(len(row) == 4 and all(row) for row in metadata_rows[1:])
metadata = [dict(zip(metadata_rows[0], row)) for row in metadata_rows[1:]]
sample_ids = [row["sample_id"] for row in metadata]
donor_ids = [row["donor_id"] for row in metadata]
assert len(sample_ids) == len(set(sample_ids)), "Duplicate sample IDs"
assert len(donor_ids) == len(set(donor_ids)), "Repeated donors need a different design"

measurements = read_tsv("measurements.tsv")
header = measurements[0]
assert header[0] == "feature_id"
assert len(header[1:]) == len(set(header[1:])), "Duplicate measurement columns"
assert set(header[1:]) == set(sample_ids), "Metadata/measurement IDs differ"
assert all(len(row) == len(header) for row in measurements[1:])
features = [row[0] for row in measurements[1:]]
assert all(features) and len(features) == len(set(features)), "Invalid feature IDs"
# Match by sample ID, never by metadata/measurement row position.
values = np.array([[float(row[header.index(sid)]) for sid in sample_ids]
                   for row in measurements[1:]])
assert np.isfinite(values).all(), "Missing/nonfinite measurement"
assert set(row["condition"] for row in metadata) == {"control", "treated"}
assert set(row["batch"] for row in metadata) == {"A", "B"}

treated = np.array([row["condition"] == "treated" for row in metadata])
batch_b = np.array([row["batch"] == "B" for row in metadata])
design = np.column_stack([np.ones(len(metadata)), treated, batch_b])
rank = int(np.linalg.matrix_rank(design))
null_direction = np.array([0.0, 1.0, -1.0])
audit = {
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
               for name in ["TASK.md", "context.md", "metadata.tsv", "measurements.tsv"]},
    "n_samples": len(sample_ids), "n_unique_donors": len(set(donor_ids)),
    "n_features": len(features), "n_values": int(values.size),
    "n_missing_or_nonfinite": int((~np.isfinite(values)).sum()),
    "sample_id_sets_match": True, "duplicate_sample_or_feature_ids": False,
    "n_samples_excluded": 0, "n_features_excluded": 0,
    "range_log2_intensity": [float(values.min()), float(values.max())],
    "condition_by_batch": {condition: {
        batch: sum(row["condition"] == condition and row["batch"] == batch
                   for row in metadata) for batch in ["A", "B"]}
        for condition in ["control", "treated"]},
    "design_columns": ["intercept", "treated_vs_control", "batch_B_vs_A"],
    "design_rank": rank, "design_n_columns": design.shape[1],
    "condition_column_equals_batch_column": bool(np.array_equal(treated, batch_b)),
    "null_direction": null_direction.tolist(),
    "max_abs_X_times_null_direction": float(np.abs(design @ null_direction).max()),
    "treatment_adjusted_for_batch_estimable": rank == design.shape[1],
}
(OUT / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
with (OUT / "design_matrix.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["sample_id"] + audit["design_columns"])
    writer.writerows([sid] + list(map(int, row)) for sid, row in zip(sample_ids, design))
print(json.dumps(audit, indent=2))

# This is a descriptive difference between condition/batch groups, not an
# adjusted treatment coefficient. SD describes donors within each group.
summary_rows = []
for feature, row in zip(features, values):
    control_values, treated_values = row[~treated], row[treated]
    summary_rows.append({
        "feature_id": feature,
        "n_control_donors": len(control_values),
        "n_treated_donors": len(treated_values),
        "control_mean_log2_intensity": float(control_values.mean()),
        "control_sd_log2_intensity": float(control_values.std(ddof=1)),
        "control_min_log2_intensity": float(control_values.min()),
        "control_max_log2_intensity": float(control_values.max()),
        "treated_mean_log2_intensity": float(treated_values.mean()),
        "treated_sd_log2_intensity": float(treated_values.std(ddof=1)),
        "treated_min_log2_intensity": float(treated_values.min()),
        "treated_max_log2_intensity": float(treated_values.max()),
        "observed_treatedB_minus_controlA_log2_intensity":
            float(treated_values.mean() - control_values.mean()),
        "interpretation": "descriptive_condition_batch_group_difference",
    })
with (OUT / "descriptive_summary.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(summary_rows[0]))
    writer.writeheader()
    writer.writerows(summary_rows)
print("\nObserved group differences (log2 intensity; not adjusted treatment effects):")
for row in summary_rows:
    print(f"{row['feature_id']}: control/A "
          f"{row['control_mean_log2_intensity']:.3f} +/- "
          f"{row['control_sd_log2_intensity']:.3f} SD; treated/B "
          f"{row['treated_mean_log2_intensity']:.3f} +/- "
          f"{row['treated_sd_log2_intensity']:.3f} SD; difference "
          f"{row['observed_treatedB_minus_controlA_log2_intensity']:+.3f}")
if rank < design.shape[1]:
    print("NOT ESTIMABLE: batch-adjusted treatment coefficient; no treatment p values, "
          "confidence intervals, or multiple-testing adjustment computed.")
print("No filtering, exclusion, imputation, renormalization, or batch correction performed.")
print("Completed: input audit, design estimability assessment, descriptive summaries.")
