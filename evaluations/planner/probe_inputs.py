#!/usr/bin/env python3
"""Inspect one prepared synthetic planner case; do not estimate effects or grade an agent."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_directory", type=Path)
    args = parser.parse_args()
    root = args.case_directory
    with (root / "metadata.tsv").open() as handle:
        metadata = list(csv.DictReader(handle, delimiter="\t"))
    matrix_path = root / "measurements.tsv"
    if not matrix_path.exists():
        matrix_path = root / "expression.tsv"
    with matrix_path.open() as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    sample_columns = rows[0][1:]
    sample_ids = [row["sample_id"] for row in metadata]
    assert all(len(row) == len(rows[0]) for row in rows[1:]), "Ragged measurement rows"
    conditions = Counter(row["condition"] for row in metadata)
    by_batch = defaultdict(Counter)
    donor_conditions = defaultdict(set)
    for row in metadata:
        if row.get("batch"):
            by_batch[row["batch"]][row["condition"]] += 1
        if row.get("donor_id"):
            donor_conditions[row["donor_id"]].add(row["condition"])
    inputs = [root / "metadata.tsv", matrix_path, root / "context.md"]
    result = {
        "scope": "Complete schema and identifier inspection of synthetic inputs; no outcome estimates or hypothesis tests",
        "features": len(rows) - 1,
        "matrix_columns": len(sample_columns),
        "metadata_rows": len(metadata),
        "matched_unique_sample_ids": len(set(sample_columns) & set(sample_ids)),
        "matrix_only_sample_ids": sorted(set(sample_columns) - set(sample_ids)),
        "metadata_only_sample_ids": sorted(set(sample_ids) - set(sample_columns)),
        "duplicate_matrix_sample_ids": [key for key, n in Counter(sample_columns).items() if n > 1],
        "duplicate_metadata_sample_ids": [key for key, n in Counter(sample_ids).items() if n > 1],
        "observations_by_condition": dict(conditions),
        "observations_by_batch_condition": {key: dict(value) for key, value in by_batch.items()},
        "unique_donor_ids": len(donor_conditions) if donor_conditions else None,
        "donors_observed_in_all_conditions": sum(set(conditions) <= values for values in donor_conditions.values()) if donor_conditions else None,
        "input_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
    }
    print("Check purpose: establish sample linkage, observed donor structure, and condition/batch coverage before choosing a comparison.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
