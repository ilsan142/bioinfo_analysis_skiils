"""Execute the exploratory notebook from a fresh Python kernel without changing inputs."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parent
notebook_path = root / 'marker_exploration.ipynb'
input_names = ['context.md', 'metadata.tsv', 'measurements.tsv']
input_before = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in input_names}
nb = nbformat.read(notebook_path, as_version=4)
for cell in nb.cells:
    if cell.cell_type == 'code':
        cell.outputs = []
        cell.execution_count = None
nbformat.validate(nb)
client = NotebookClient(nb, timeout=120, kernel_name='python3', allow_errors=False, resources={'metadata': {'path': str(root)}})
try:
    client.execute()
except Exception:
    nbformat.write(nb, root / 'results/marker_exploration.failed.ipynb')
    raise
nbformat.validate(nb)
nbformat.write(nb, notebook_path)
code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
error_count = sum(output.output_type == 'error' for cell in code_cells for output in cell.outputs)
input_after = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in input_names}
assert input_before == input_after, 'Original input contents changed.'
assert error_count == 0 and all(cell.execution_count is not None for cell in code_cells)
status = {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'notebook': notebook_path.name,
    'fresh_kernel': True,
    'execution_order': [cell.execution_count for cell in code_cells],
    'executed_code_cells': len(code_cells),
    'error_outputs': error_count,
    'schema_validated': True,
    'input_files_unchanged': input_before == input_after,
    'figure_review': 'requires separate human or assistant viewing; not certified by this script',
    'biological_validation': False,
}
(root / 'results/execution.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
print('새 커널 전체 실행 완료:', len(code_cells), '개 코드 셀, 오류', error_count, '개; 원본 입력 보존 확인.')
