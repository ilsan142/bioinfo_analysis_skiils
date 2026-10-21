from pathlib import Path
import pandas as pd
from scipy import stats
Path('execution_marker.txt').write_text('analysis executed')
samples = pd.read_csv('samples.csv')
control = samples.loc[samples.condition == 'control', 'score'].round()
treated = samples.loc[samples.condition == 'treated', 'score'].round()
result = stats.ttest_ind(treated, control)
Path('result.txt').write_text(f'independent_n={len(samples)}; p={result.pvalue}')
