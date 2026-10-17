"""Audit sample links, then estimate the treated-control contrast. No input edits."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter

import numpy as np
import scipy
import statsmodels
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def load_inputs():
    with (ROOT / "metadata.tsv").open() as handle:
        metadata = list(csv.DictReader(handle, delimiter="\t"))
    with (ROOT / "measurements.tsv").open() as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    sample_ids = rows[0][1:]
    features = [row[0] for row in rows[1:]]
    metadata_ids = [row["sample_id"] for row in metadata]
    assert len(set(sample_ids)) == len(sample_ids), "Duplicate measurement sample IDs"
    assert len(set(metadata_ids)) == len(metadata_ids), "Duplicate metadata sample IDs"
    assert len(set(features)) == len(features), "Duplicate feature IDs"
    assert set(sample_ids) == set(metadata_ids), "Unmatched sample IDs"
    assert all(len(row) == len(rows[0]) for row in rows[1:]), "Ragged measurement rows"
    lookup = {row["sample_id"]: row for row in metadata}
    aligned = [lookup[sample_id] for sample_id in sample_ids]
    values = np.array([[np.nan if value == "NA" else float(value)
                        for value in row[1:]] for row in rows[1:]])
    assert not np.isinf(values).any(), "Infinite values"
    return aligned, features, values, metadata_ids


def write_tsv(name, columns, rows):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(columns)
        writer.writerows(rows)


def audit():
    aligned, features, values, metadata_ids = load_inputs()
    sample_ids = [row["sample_id"] for row in aligned]
    counts = Counter((row["condition"], row["batch"]) for row in aligned)
    donor_counts = Counter(row["donor_id"] for row in aligned)
    summary = {
        "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                         for name in ["TASK.md", "context.md", "metadata.tsv", "measurements.tsv"]},
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__,
                        "statsmodels": statsmodels.__version__},
        "shape_features_samples": list(values.shape),
        "sample_id_sets_match": True,
        "metadata_order_matches_measurement_order": sample_ids == metadata_ids,
        "link_method": "exact sample_id; metadata reordered to measurement columns",
        "measurement_sample_order": sample_ids,
        "unique_donors": len(donor_counts),
        "samples_per_donor": dict(sorted(donor_counts.items())),
        "condition_batch_counts": {f"{condition}/{batch}": n for (condition, batch), n in sorted(counts.items())},
        "missing_values": int(np.isnan(values).sum()),
        "zero_values": int((values == 0).sum()),
        "minimum": float(np.nanmin(values)),
        "maximum": float(np.nanmax(values)),
        "excluded_samples": [],
        "excluded_features": [],
    }
    (OUT / "audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_tsv("sample_links.tsv", ["measurement_column", "sample_id", "donor_id", "condition", "batch"],
              [[i + 1, row["sample_id"], row["donor_id"], row["condition"], row["batch"]]
               for i, row in enumerate(aligned)])
    print(json.dumps(summary, indent=2))


def estimate():
    aligned, features, values, _ = load_inputs()
    assert not np.isnan(values).any(), "Missing data require an explicit analysis decision"
    assert len(set(row["donor_id"] for row in aligned)) == len(aligned), \
        "Repeated donors: this independent-donor model must be revised"
    assert set(row["condition"] for row in aligned) == {"control", "treated"}
    assert set(row["batch"] for row in aligned) == {"A", "B"}
    treated = np.array([row["condition"] == "treated" for row in aligned])
    batch_b = np.array([row["batch"] == "B" for row in aligned])
    design = np.column_stack([np.ones(len(aligned)), treated, batch_b])
    assert np.linalg.matrix_rank(design) == design.shape[1], "Nonidentifiable design"
    write_tsv("design_matrix.tsv", ["sample_id", "intercept", "treated", "batch_B"],
              [[row["sample_id"], *design[i]] for i, row in enumerate(aligned)])
    output = []
    for feature, y in zip(features, values):
        fitted = sm.OLS(y, design).fit()
        lo, hi = fitted.conf_int(alpha=0.05)[1]
        output.append([feature, int((~treated).sum()), int(treated.sum()),
                       y[~treated].mean(), y[treated].mean(),
                       y[~treated].std(ddof=1), y[treated].std(ddof=1),
                       fitted.params[1], fitted.bse[1], lo, hi,
                       fitted.params[2], int(fitted.df_resid)])
    columns = ["feature_id", "n_control_donors", "n_treated_donors", "control_mean_log2",
               "treated_mean_log2", "control_sd_log2", "treated_sd_log2",
               "treated_minus_control_log2", "standard_error", "ci95_lower", "ci95_upper",
               "batch_B_minus_A_log2", "residual_df"]
    write_tsv("contrasts.tsv", columns, output)
    print("Model: log2_intensity ~ intercept + treated + batch_B; independent donors")
    print(f"Design rank: {np.linalg.matrix_rank(design)}/{design.shape[1]}; residual df: {len(aligned)-design.shape[1]}")
    print("CI: per-marker 95% Student-t interval, additive batch model, independent normal equal-variance errors")
    print("No significance testing or multiple-testing claims; intervals are not simultaneous across markers.")
    print((OUT / "contrasts.tsv").read_text(), end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["audit", "estimate", "all"])
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.stage in {"audit", "all"}:
        audit()
    if args.stage in {"estimate", "all"}:
        estimate()
