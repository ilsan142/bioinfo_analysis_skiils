"""Current paired-donor analysis after design_correction.txt. No original input edits."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from decimal import Decimal

import numpy as np
import scipy
import statsmodels
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def load_inputs():
    with (ROOT / "metadata_corrected.tsv").open() as handle:
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
    return aligned, features, values, metadata_ids, [row[1:] for row in rows[1:]]


def write_tsv(name, columns, rows):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(columns)
        writer.writerows(rows)


def audit():
    aligned, features, values, metadata_ids, raw_values = load_inputs()
    with (ROOT / "metadata.tsv").open() as handle:
        original = {row["sample_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    assert set(original) == set(metadata_ids)
    assert all(original[row["sample_id"]][field] == row[field]
               for row in aligned for field in ["sample_id", "condition", "batch"]), \
        "Correction unexpectedly changed sample, condition, or batch"
    sample_ids = [row["sample_id"] for row in aligned]
    counts = Counter((row["condition"], row["batch"]) for row in aligned)
    donor_counts = Counter(row["donor_id"] for row in aligned)
    summary = {
        "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                         for name in ["TASK.md", "context.md", "metadata.tsv", "metadata_corrected.tsv",
                                      "design_correction.txt", "measurements.tsv"]},
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__,
                        "statsmodels": statsmodels.__version__},
        "shape_features_samples": list(values.shape),
        "sample_id_sets_match": True,
        "metadata_order_matches_measurement_order": sample_ids == metadata_ids,
        "link_method": "exact sample_id; metadata reordered to measurement columns",
        "measurement_sample_order": sample_ids,
        "unique_donors": len(donor_counts),
        "independent_unit": "paired donor, based on user correction in design_correction.txt",
        "correction_preserves_sample_condition_batch": True,
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
    pair_rows, _ = paired_differences(aligned, features, raw_values)
    write_tsv("paired_differences.tsv", ["feature_id", "donor_id", "control_sample_id", "treated_sample_id",
              "batch", "control_log2", "treated_log2", "treated_minus_control_log2"], pair_rows)
    print(json.dumps(summary, indent=2))
    print((OUT / "paired_differences.tsv").read_text(), end="")


def paired_differences(aligned, features, raw_values):
    donors = sorted(set(row["donor_id"] for row in aligned))
    pairs = []
    for donor in donors:
        members = [i for i, row in enumerate(aligned) if row["donor_id"] == donor]
        assert len(members) == 2, f"Incomplete or duplicated pair for {donor}"
        by_condition = {aligned[i]["condition"]: i for i in members}
        assert set(by_condition) == {"control", "treated"}, f"Invalid pair for {donor}"
        c, t = by_condition["control"], by_condition["treated"]
        assert aligned[c]["batch"] == aligned[t]["batch"], "Batch differs within donor"
        pairs.append((donor, c, t))
    rows, differences = [], []
    for feature, raw_y in zip(features, raw_values):
        feature_differences = []
        for donor, c, t in pairs:
            assert raw_y[t] != "NA" and raw_y[c] != "NA", "Missing pair requires a separate decision"
            # Use supplied decimal values exactly; binary subtraction must not invent pair variance.
            difference = Decimal(raw_y[t]) - Decimal(raw_y[c])
            feature_differences.append(difference)
            rows.append([feature, donor, aligned[c]["sample_id"], aligned[t]["sample_id"],
                         aligned[c]["batch"], raw_y[c], raw_y[t], str(difference)])
        differences.append(feature_differences)
    return rows, differences


def estimate():
    aligned, features, values, _, raw_values = load_inputs()
    assert not np.isnan(values).any(), "Missing data require an explicit analysis decision"
    assert set(row["condition"] for row in aligned) == {"control", "treated"}
    assert set(row["batch"] for row in aligned) == {"A", "B"}
    _, differences = paired_differences(aligned, features, raw_values)
    donors = sorted(set(row["donor_id"] for row in aligned))
    treated = np.array([row["condition"] == "treated" for row in aligned])
    batch_b = np.array([row["batch"] == "B" for row in aligned])
    donor_indicators = [np.array([row["donor_id"] == donor for row in aligned]) for donor in donors[1:]]
    design = np.column_stack([np.ones(len(aligned)), treated, *donor_indicators])
    assert np.linalg.matrix_rank(design) == design.shape[1], "Nonidentifiable design"
    # Batch is constant within donor and lies in the span of the donor indicators.
    rank_with_batch = np.linalg.matrix_rank(np.column_stack([design, batch_b]))
    assert rank_with_batch == design.shape[1], "Review unexpected batch structure"
    write_tsv("design_matrix.tsv", ["sample_id", "intercept", "treated", *[f"donor_{d}" for d in donors[1:]]],
              [[row["sample_id"], *design[i]] for i, row in enumerate(aligned)])
    output = []
    for feature, y, exact_differences in zip(features, values, differences):
        n = len(exact_differences)
        pair_values = np.array([float(d) for d in exact_differences])
        mean_difference = float(sum(exact_differences) / Decimal(n))
        constant = len(set(exact_differences)) == 1
        sd = 0.0 if constant else float(np.std(pair_values, ddof=1))
        se = 0.0 if constant else float(stats.sem(pair_values))
        if constant:
            # The arithmetic t interval collapses. Do not label it an informative 95% CI.
            lo, hi = "NA", "NA"
            formal_lo = formal_hi = mean_difference
            status = "zero_pair_variance_degenerate; ordinary_95pct_CI_not_reported"
        else:
            lo, hi = stats.t.interval(0.95, df=n-1, loc=mean_difference, scale=se)
            formal_lo, formal_hi = lo, hi
            status = "paired_t_CI; independent_normal_differences_assumed"
        # Algebraic cross-check: donor fixed-effect model equals the paired analysis.
        fitted = sm.OLS(y, design).fit()
        assert np.isclose(fitted.params[1], mean_difference)
        assert int(fitted.df_resid) == n - 1
        if not constant:
            assert np.allclose(fitted.conf_int(alpha=0.05)[1], [lo, hi])
            assert np.isclose(fitted.bse[1], se)
        output.append([feature, n, 2*n,
                       y[~treated].mean(), y[treated].mean(),
                       mean_difference, sd, se, lo, hi, n-1, status, formal_lo, formal_hi])
    columns = ["feature_id", "n_independent_donor_pairs", "n_observations", "control_mean_log2",
               "treated_mean_log2", "treated_minus_control_log2", "paired_difference_sd",
               "standard_error", "ci95_lower", "ci95_upper", "residual_df", "uncertainty_status",
               "formal_t_formula_lower", "formal_t_formula_upper"]
    write_tsv("contrasts.tsv", columns, output)
    print("Current model: within-donor treated-control differences; 4 independent donor pairs")
    print("Equivalent cross-check: log2_intensity ~ intercept + treated + donor indicators")
    print(f"Design rank: {np.linalg.matrix_rank(design)}/{design.shape[1]}; residual df: {len(aligned)-design.shape[1]}")
    print(f"Adding batch gives rank {rank_with_batch}/{design.shape[1]+1}; separate batch coefficient is not estimable alongside donor.")
    print("CI: per-marker paired 95% Student-t interval; independent normally distributed donor differences")
    print("Zero observed pair variance: report empirical SD/SE=0 and formal collapsed bounds only; ordinary 95% CI withheld.")
    print("WARNING: zero pair variance at supplied decimal precision is not evidence of zero population or measurement uncertainty.")
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
