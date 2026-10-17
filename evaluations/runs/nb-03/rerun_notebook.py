"""Execute the analysis from a fresh kernel; retain actual outputs in the notebook."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import os
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parent
for variable, folder in [('IPYTHONDIR', 'ipython'), ('JUPYTER_RUNTIME_DIR', 'jupyter')]:
    runtime_path = root / '.runtime' / folder
    runtime_path.mkdir(parents=True, exist_ok=True)
    os.environ[variable] = str(runtime_path)
notebook_path = root / 'treated_control_batch_analysis.ipynb'
source_paths = [root / name for name in ['TASK.md', 'context.md', 'metadata.tsv', 'measurements.tsv']]
before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
notebook = nbformat.read(notebook_path, as_version=4)
for cell in notebook.cells:
    if cell.cell_type == 'code':
        cell.outputs = []
        cell.execution_count = None
nbformat.validate(notebook)
client = NotebookClient(notebook, timeout=120, kernel_name='python3', resources={'metadata': {'path': str(root)}})
client.execute()
after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
assert before == after, 'Original inputs changed during rerun'
code_cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
assert [cell.execution_count for cell in code_cells] == list(range(1, len(code_cells) + 1))
assert all(output.output_type != 'error' for cell in code_cells for output in cell.outputs)
stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
for cell in notebook.cells:
    if cell.cell_type == 'markdown' and '<!-- rerun_status -->' in cell.source:
        cell.source = (
            '<!-- rerun_status -->\n'
            f'**전체 재실행 확인:** {stamp}에 새 Python 커널에서 코드 셀 {len(code_cells)}개를 '
            '순서대로 실행했고 오류 없이 실제 출력을 저장했다. 원래 입력 4개 파일의 실행 전후 SHA-256은 동일했다. '
            '노트북 스키마 검사도 통과했다. 최초 탐색은 실제 노트북 커널에서 단계별로 실행했고, 각 단계 출력을 '
            '확인한 뒤 다음 단계와 해석을 추가했다. 이 재실행은 코드와 저장 출력의 일치를 확인하며 생물학적 검증은 아니다. '
            '그림을 생성하지 않아 그림 시각 검토는 해당 없음.'
        )
notebook.metadata['analysis_rerun'] = {'finished_utc': stamp, 'fresh_kernel': True, 'code_cells': len(code_cells), 'inputs_unchanged': True}
nbformat.validate(notebook)
nbformat.write(notebook, notebook_path)
print(f'Fresh-kernel rerun complete: {len(code_cells)} code cells, no errors; inputs unchanged.')
print(notebook_path)
for index, cell in enumerate(code_cells, start=1):
    print(f'CODE CELL {index}')
    for output in cell.outputs:
        if output.output_type == 'stream':
            print(output.text)
        elif output.output_type in {'display_data', 'execute_result'}:
            print(output.data.get('text/plain', '[non-text output]'))
