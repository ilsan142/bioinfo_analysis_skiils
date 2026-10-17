#!/usr/bin/env python3
"""Synthetic log2 marker exploration. Run: python analysis.py"""
import csv
import hashlib
import json
import math
import platform
import statistics
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
import statsmodels
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def read_tsv(name):
    with (ROOT / name).open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = reader.fieldnames
        assert fields and len(fields) == len(set(fields)), "Duplicate header"
        rows = list(reader)
    assert all(None not in row and None not in row.values() for row in rows)
    return fields, rows


def write_tsv(name, rows):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def audit():
    _, metadata = read_tsv("metadata.tsv")
    fields, measurements = read_tsv("measurements.tsv")
    assert fields[0] == "feature_id"
    assert all(all(row[key] for key in ["sample_id", "donor_id", "condition", "batch"]) for row in metadata)
    ids = [row["sample_id"] for row in metadata]
    donors = [row["donor_id"] for row in metadata]
    features = [row["feature_id"] for row in measurements]
    assert len(ids) == len(set(ids)), "Duplicate sample ID"
    assert len(donors) == len(set(donors)), "Repeated donor: revise design"
    assert len(features) == len(set(features)), "Duplicate feature ID"
    assert set(ids) == set(fields[1:]), "Unmatched sample IDs"
    assert {row["condition"] for row in metadata} == {"control", "treated"}
    assert {row["batch"] for row in metadata} == {"A", "B"}
    values = {row["feature_id"]: {
        sid: (None if row[sid] == "NA" else float(row[sid])) for sid in ids
    } for row in measurements}
    numbers = [v for feature in values.values() for v in feature.values() if v is not None]
    assert all(math.isfinite(v) for v in numbers), "Non-finite intensity"
    missing = len(ids) * len(features) - len(numbers)
    qc = {
        "samples": len(ids), "independent_donors": len(set(donors)),
        "features": len(features), "missing": missing, "zeros": numbers.count(0),
        "unmatched_ids": [], "measurement_order_matches_metadata": fields[1:] == ids,
        "join": "sample_id", "excluded_samples": [], "excluded_features": [],
        "condition_batch": dict(Counter(row["condition"] + "/" + row["batch"] for row in metadata)),
        "input_scale": "background-corrected, normalized log2 intensity; no transform",
        "python": platform.python_version(),
        "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                   for name in ["context.md", "metadata.tsv", "measurements.tsv"]},
    }
    (OUT / "qc.json").write_text(json.dumps(qc, indent=2) + "\n")
    print("AUDIT", json.dumps(qc, sort_keys=True))
    assert missing == 0, "Missing data require an explicit analysis decision"
    distribution = []
    for feature, by_id in values.items():
        for condition in ["control", "treated"]:
            obs = sorted(by_id[row["sample_id"]] for row in metadata if row["condition"] == condition)
            n = len(obs)
            mean = sum(obs) / n
            sd = math.sqrt(sum((v - mean) ** 2 for v in obs) / (n - 1))
            distribution.append({"feature_id": feature, "condition": condition, "n_donors": n,
                                 "mean": mean, "sd": sd, "min": obs[0],
                                 "median": statistics.median(obs), "max": obs[-1],
                                 "sorted_values": ", ".join(str(v) for v in obs)})
    write_tsv("distribution.tsv", distribution)
    for row in distribution:
        print("DISTRIBUTION", json.dumps(row, sort_keys=True))
    return metadata, values


def compare(metadata, values):
    # Independent donors; reference levels are control and batch A.
    # The estimand is the adjusted treated-minus-control mean log2 intensity.
    design = np.array([[1, row["condition"] == "treated", row["batch"] == "B"]
                       for row in metadata], dtype=float)
    rank = int(np.linalg.matrix_rank(design))
    assert rank == design.shape[1], "Condition and batch are not separately identifiable"
    print("MODEL", json.dumps({"formula": "log2_intensity ~ 1 + treated + batch_B",
                               "rank": rank, "columns": 3, "residual_df": len(metadata)-rank,
                               "numpy": np.__version__, "scipy": scipy.__version__,
                               "statsmodels": statsmodels.__version__}))
    results, within_batch, residuals = [], [], []
    for feature, by_id in values.items():
        y = np.array([by_id[row["sample_id"]] for row in metadata])
        model = sm.OLS(y, design).fit()
        ci = model.conf_int(alpha=0.05)[1]
        raw_delta = float(y[design[:, 1] == 1].mean() - y[design[:, 1] == 0].mean())
        results.append({"feature_id": feature, "n_control_donors": int(sum(design[:, 1] == 0)),
                        "n_treated_donors": int(sum(design[:, 1] == 1)),
                        "raw_treated_minus_control": raw_delta,
                        "batch_adjusted_difference": float(model.params[1]),
                        "ci95_low": float(ci[0]), "ci95_high": float(ci[1]),
                        "batch_B_minus_A": float(model.params[2]),
                        "residual_sd": float(np.sqrt(model.mse_resid)),
                        "residual_df": int(model.df_resid)})
        for batch in ["A", "B"]:
            groups = {condition: [by_id[row["sample_id"]] for row in metadata
                                  if row["batch"] == batch and row["condition"] == condition]
                      for condition in ["control", "treated"]}
            within_batch.append({"feature_id": feature, "batch": batch,
                                 "n_control_donors": len(groups["control"]),
                                 "n_treated_donors": len(groups["treated"]),
                                 "control_mean": float(np.mean(groups["control"])),
                                 "treated_mean": float(np.mean(groups["treated"])),
                                 "treated_minus_control": float(np.mean(groups["treated"]) - np.mean(groups["control"]))})
        for index, row in enumerate(metadata):
            residuals.append({"feature_id": feature, **row,
                              "log2_intensity": float(y[index]),
                              "fitted": float(model.fittedvalues[index]),
                              "residual": float(model.resid[index])})
        print("COMPARISON", json.dumps(results[-1], sort_keys=True))
        print("WITHIN_BATCH", json.dumps(within_batch[-2:], sort_keys=True))
        print("RESIDUAL_RANGE", feature, float(model.resid.min()), float(model.resid.max()))
    write_tsv("effects.tsv", results)
    write_tsv("within_batch.tsv", within_batch)
    write_tsv("aligned_observations_residuals.tsv", residuals)


def check_single_donor_influence(metadata, values):
    # Added after observing the full-model differences. This is sensitivity
    # analysis, not a new exclusion rule or independent validation.
    results = []
    for feature, by_id in values.items():
        feature_results = []
        for omitted in metadata:
            retained = [row for row in metadata if row["donor_id"] != omitted["donor_id"]]
            design = np.array([[1, row["condition"] == "treated", row["batch"] == "B"]
                               for row in retained], dtype=float)
            assert np.linalg.matrix_rank(design) == 3
            y = [by_id[row["sample_id"]] for row in retained]
            fit = sm.OLS(y, design).fit()
            row = {"feature_id": feature, "omitted_donor_id": omitted["donor_id"],
                   "omitted_sample_id": omitted["sample_id"], "n_remaining": len(retained),
                   "batch_adjusted_difference": float(fit.params[1])}
            feature_results.append(row)
        results.extend(feature_results)
        effects = [row["batch_adjusted_difference"] for row in feature_results]
        print("LEAVE_ONE_DONOR_OUT", json.dumps({"feature_id": feature,
              "min_difference": min(effects), "max_difference": max(effects)}))
    write_tsv("leave_one_donor_out.tsv", results)


if __name__ == "__main__":
    metadata, values = audit()
    compare(metadata, values)
    check_single_donor_influence(metadata, values)
