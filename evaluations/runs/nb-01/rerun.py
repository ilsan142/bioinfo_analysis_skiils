"""Execute analysis.ipynb from a new Python kernel and preserve real outputs.

Run: python rerun.py
Dependencies and versions used are printed in the notebook's first code cell.
Original inputs are only read; result table and figures are regenerated.
"""
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    base = Path(__file__).resolve().parent
    path = base / "analysis.ipynb"
    notebook = nbformat.read(path, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    client = NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(base)}},
    )
    client.execute()
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert all(cell.execution_count is not None for cell in code_cells)
    print(f"Fresh-kernel rerun completed: {len(code_cells)} code cells; {path}")
    for artifact in ["marker_results.tsv", "marker_A.png", "marker_A.svg"]:
        assert (base / artifact).is_file(), artifact
        print(artifact)


if __name__ == "__main__":
    main()
