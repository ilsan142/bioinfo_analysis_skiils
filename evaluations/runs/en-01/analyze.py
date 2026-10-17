#!/usr/bin/env python3
"""Small, staged analysis of the supplied synthetic log2 marker panel."""
from pathlib import Path
import argparse
import csv
import hashlib
import platform

import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent


def load_inputs():
    # Read literal headers first: pandas can silently rename duplicate columns.
    with (ROOT / "measurements.tsv").open() as handle:
        header = next(csv.reader(handle, delimiter="\t"))
    assert header[0] == "feature_id"
    assert len(header) == len(set(header)), "Duplicate measurement columns"
    metadata = pd.read_csv(ROOT / "metadata.tsv", sep="\t", dtype=str)
    values = pd.read_csv(ROOT / "measurements.tsv", sep="\t", index_col=0, na_values=["NA"])
    assert list(metadata.columns) == ["sample_id", "donor_id", "condition", "batch"]
    assert not metadata.isna().any().any(), "Missing metadata"
    assert not metadata["sample_id"].duplicated().any(), "Duplicate sample IDs"
    assert not metadata["donor_id"].duplicated().any(), "Repeated donor: reconsider model"
    assert not values.index.has_duplicates, "Duplicate features"
    assert not values.index.isna().any(), "Missing feature IDs"
    assert set(values.columns) == set(metadata["sample_id"]), "Sample sets differ"
    assert set(metadata["condition"]) == {"control", "treated"}
    assert set(metadata["batch"]) == {"A", "B"}
    metadata = metadata.set_index("sample_id")
    original_order = list(values.columns)
    values = values.loc[:, metadata.index].apply(pd.to_numeric, errors="raise")
    assert np.isfinite(values.to_numpy()).all(), "Missing/nonfinite values: inspect first"
    design = pd.DataFrame({"intercept": 1.0,
                           "treated": (metadata["condition"] == "treated").astype(float),
                           "batch_B": (metadata["batch"] == "B").astype(float)},
                          index=metadata.index)
    assert np.linalg.matrix_rank(design) == design.shape[1], "Nonidentifiable additive model"
    return metadata, values, design, original_order


def qc(metadata, values, design, original_order):
    print("QUESTION 1: sample linkage, independent units, design, distributions")
    print("Input measurement column order:", ", ".join(original_order))
    print("ID-aligned order:", ", ".join(values.columns))
    print(f"Samples={len(metadata)}; independent donors={metadata.donor_id.nunique()}; markers={len(values)}")
    print("Missing measurements=0; duplicate sample/donor/feature IDs=0; unmatched IDs=0")
    print("Condition x batch (independent donors):")
    print(pd.crosstab(metadata.condition, metadata.batch).to_string())
    print(f"Additive model rank={np.linalg.matrix_rank(design)}/{design.shape[1]}")
    print("Per-sample distributions across three different markers (descriptive only):")
    samples = values.agg(["min", "median", "max"]).T.join(metadata)
    print(samples.to_string())
    print("Marker-by-condition distributions on supplied log2 intensity scale:")
    long = values.T.rename_axis("sample_id").reset_index().melt(
        id_vars="sample_id", var_name="feature_id", value_name="log2_intensity")
    long = long.join(metadata, on="sample_id")
    print(long.groupby(["feature_id", "condition"]).log2_intensity.agg(
        ["count", "mean", "std", "min", "median", "max"]).to_string())
    print("No normalization, transformation, imputation, aggregation, filtering, or exclusions applied.")


def fit_effects(metadata, values, design):
    print("QUESTION 2: treated minus control, adjusted for batch")
    print("OLS: log2_intensity ~ intercept + treated + batch_B; control and batch A are references.")
    print("Classical 95% t intervals; independent, homoskedastic approximately normal errors assumed.")
    print("BH testing family: all 3 supplied markers, one two-sided treated-control contrast each.")
    rows = []
    fits = {}
    for feature, y in values.iterrows():
        fit = sm.OLS(y, design).fit()
        fits[feature] = fit
        interval = fit.conf_int(alpha=0.05).loc["treated"]
        rows.append({"feature_id": feature,
                     "n_control_donors": int((metadata.condition == "control").sum()),
                     "n_treated_donors": int((metadata.condition == "treated").sum()),
                     "control_mean": y[metadata.condition == "control"].mean(),
                     "treated_mean": y[metadata.condition == "treated"].mean(),
                     "difference_log2": fit.params["treated"],
                     "ci95_low": interval.iloc[0], "ci95_high": interval.iloc[1],
                     "batch_B_minus_A": fit.params["batch_B"],
                     "residual_df": fit.df_resid, "residual_sd": np.sqrt(fit.mse_resid),
                     "p_value": fit.pvalues["treated"]})
    result = pd.DataFrame(rows).set_index("feature_id")
    result["q_BH_3_markers"] = multipletests(result.p_value, method="fdr_bh")[1]
    print(result.to_string(float_format=lambda x: f"{x:.6g}"))
    result.to_csv(ROOT / "results.tsv", sep="\t", float_format="%.10g")
    return result, fits


def sensitivity(metadata, values, design, result, fits):
    print("QUESTION 3 (post hoc): batch consistency, residuals, and single-donor dependence")
    print("Leave-one-donor-out fits assess influence only; no donor is excluded from the primary results.")
    for feature, y in values.iterrows():
        within_batch = {}
        for batch in ["A", "B"]:
            in_batch = metadata.batch == batch
            within_batch[batch] = (y[in_batch & (metadata.condition == "treated")].mean()
                                   - y[in_batch & (metadata.condition == "control")].mean())
            result.loc[feature, f"difference_within_batch_{batch}"] = within_batch[batch]
        result.loc[feature, "batch_difference_of_differences"] = within_batch["B"] - within_batch["A"]
        leave_one_out = {}
        for sample in metadata.index:
            keep = metadata.index != sample
            assert np.linalg.matrix_rank(design.loc[keep]) == design.shape[1]
            leave_one_out[sample] = sm.OLS(y.loc[keep], design.loc[keep]).fit().params["treated"]
        result.loc[feature, "leave_one_out_min"] = min(leave_one_out.values())
        result.loc[feature, "leave_one_out_max"] = max(leave_one_out.values())
        influence = fits[feature].get_influence()
        result.loc[feature, "max_abs_internal_studentized_residual"] = np.max(np.abs(influence.resid_studentized_internal))
        result.loc[feature, "max_cooks_distance"] = np.max(influence.cooks_distance[0])
        print(feature, "within-batch differences:", {k: round(float(v), 6) for k, v in within_batch.items()})
        print("  Residuals:", {k: round(v, 6) for k, v in fits[feature].resid.items()})
        print("  Effect after omitting each donor:", {k: round(float(v), 6) for k, v in leave_one_out.items()})
    print(result[["difference_within_batch_A", "difference_within_batch_B",
                  "batch_difference_of_differences", "leave_one_out_min", "leave_one_out_max",
                  "max_abs_internal_studentized_residual", "max_cooks_distance"]]
          .to_string(float_format=lambda x: f"{x:.6g}"))
    print("No normality/interaction significance test: 8 donors provide weak assumption diagnostics.")
    print("No randomization/permutation claim: treatment randomization/exchangeability is undocumented.")
    print("Intervals and p values remain model-based exploratory summaries of synthetic data.")
    result.to_csv(ROOT / "results.tsv", sep="\t", float_format="%.10g")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["qc", "fit", "all"], nargs="?", default="all")
    args = parser.parse_args()
    print("Command: python analyze.py", args.stage)
    print("Versions:", {"python": platform.python_version(), "numpy": np.__version__,
                        "pandas": pd.__version__, "scipy": scipy.__version__,
                        "statsmodels": statsmodels.__version__})
    for name in ["TASK.md", "context.md", "metadata.tsv", "measurements.tsv"]:
        print("SHA256", name, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())
    metadata, values, design, original_order = load_inputs()
    qc(metadata, values, design, original_order)
    if args.stage in {"fit", "all"}:
        result, fits = fit_effects(metadata, values, design)
        if args.stage == "all":
            sensitivity(metadata, values, design, result, fits)


if __name__ == "__main__":
    main()
