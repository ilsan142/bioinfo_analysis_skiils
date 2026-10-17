#!/usr/bin/env python3
"""Rerun the two synthetic notebook cases without reusing their saved outputs.

Requires nbformat, nbclient, the recorded kernel, and each notebook's packages.
Prints a JSON check record; does not modify archived notebooks or prove biology.
"""

import csv
import hashlib
import json
import math
import shutil
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def output_evidence(notebook, working_directory):
    """Compare real outputs while ignoring counters and runtime metadata."""
    evidence = []
    for cell in notebook.cells:
        if cell.cell_type != "code" or not cell.source.strip():
            continue
        outputs = []
        for output in cell.outputs:
            item = {key: output[key] for key in ("output_type", "name", "text", "data", "ename", "evalue", "traceback") if key in output}
            # A changed execution directory is not a changed analysis result.
            normalized = json.dumps(item, sort_keys=True, ensure_ascii=False).replace(str(working_directory), "<working_directory>")
            outputs.append(hashlib.sha256(normalized.encode()).hexdigest())
        evidence.append(outputs)
    return evidence


def main():
    evaluation_root = Path(__file__).resolve().parent
    cases = {case["id"]: case for case in json.loads((evaluation_root / "cases.json").read_text())}
    records = []
    for case_id in ("01", "03"):
        source = evaluation_root / "runs" / f"nb-{case_id}"
        notebooks = list(source.glob("*.ipynb"))
        assert len(notebooks) == 1, f"Expected one notebook in {source}"
        notebook = nbformat.read(notebooks[0], as_version=4)
        nbformat.validate(notebook)
        code_cells = [cell for cell in notebook.cells if cell.cell_type == "code" and cell.source.strip()]
        assert code_cells and all(cell.execution_count is not None for cell in code_cells), "Archived analysis has unexecuted code cells"
        assert not any(output.output_type == "error" for cell in code_cells for output in cell.outputs), "Archived notebook has execution errors"
        input_identity = all((source / name).read_bytes() == value.encode() for name, value in cases[case_id]["files"].items())
        assert input_identity, "Archived raw input differs from the original fixture"
        original_directory = Path(f"/tmp/bio-notebook-{case_id}-20261017")
        expected = output_evidence(notebook, original_directory)

        with tempfile.TemporaryDirectory(prefix=f"bio-notebook-replay-{case_id}-") as directory:
            work = Path(directory)
            for name in [*cases[case_id]["files"], "TASK.md"]:
                shutil.copy2(source / name, work / name)
            # Saved outputs and execution state must not supply the new evidence.
            for cell in code_cells:
                cell.outputs = []
                cell.execution_count = None
            NotebookClient(notebook, timeout=120, kernel_name=notebook.metadata.kernelspec.name,
                           resources={"metadata": {"path": str(work)}}).execute()
            nbformat.validate(notebook)
            actual = output_evidence(notebook, work)
            equal = actual == expected
            assert all((work / name).read_bytes() == value.encode() for name, value in cases[case_id]["files"].items()), "Rerun modified raw input"
            table_checks = {path.name: (work / path.name).read_bytes() == path.read_bytes()
                            for path in source.glob("*.tsv") if path.name not in cases[case_id]["files"]}
            if case_id == "01":
                with (work / "marker_results.tsv").open() as stream:
                    results = {row["marker"]: row for row in csv.DictReader(stream, delimiter="\t")}
                for marker, expected_effect in {"marker_A": 1.025, "marker_B": 0.1, "marker_C": -0.1}.items():
                    assert math.isclose(float(results[marker]["adjusted_difference_log2"]), expected_effect, abs_tol=1e-9)
                    assert int(results[marker]["n_control_donors"]) == int(results[marker]["n_treated_donors"]) == 4
                assert math.isclose(float(results["marker_A"]["loo_min_log2"]), 0.98, abs_tol=1e-9)
                assert math.isclose(float(results["marker_A"]["loo_max_log2"]), 1.06, abs_tol=1e-9)
            else:
                with (work / "descriptive_group_differences.tsv").open() as stream:
                    results = {row["feature_id"]: row for row in csv.DictReader(stream, delimiter="\t")}
                for marker, expected_effect in {"marker_A": 2.0, "marker_B": 0.5}.items():
                    assert math.isclose(float(results[marker]["observed_treated_B_minus_control_A"]), expected_effect, abs_tol=1e-9)
                    assert results[marker]["batch_adjusted_treatment_effect"] == "not_identifiable"
                    assert int(results[marker]["n_control_donors"]) == int(results[marker]["n_treated_donors"]) == 3
            records.append({
                "case": case_id, "notebook": str(notebooks[0].relative_to(evaluation_root)),
                "schema_valid": True, "fresh_kernel": True, "fresh_directory": True,
                "code_cells_executed": len(code_cells), "original_inputs_unchanged": input_identity,
                "stored_and_rerun_output_evidence_equal": equal,
                "exported_tables_byte_identical": table_checks,
                "bounded_fixture_value_checks": "pass",
                "differing_code_cell_indices": [i for i, (old, new) in enumerate(zip(expected, actual)) if old != new],
            })
    print(json.dumps({"edition": "English notebook v1", "checks": records,
                      "comparison": "All stream and display data, including embedded images; directory paths normalized, output counters and metadata excluded.",
                      "scope": "Schema and synthetic execution checks only; behavioral timing, scientific interpretation, and visual review require separate inspection."}, indent=2))
    assert all(record["stored_and_rerun_output_evidence_equal"] and all(record["exported_tables_byte_identical"].values()) for record in records), "Inspect changed outputs before claiming reproduction"


if __name__ == "__main__":
    main()
