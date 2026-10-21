# Supplied excerpt of the executed comparison; not a complete upstream pipeline.
import pandas as pd
from scipy import stats
means = pd.read_csv('donor_means.csv').set_index('donor')
difference = means['treated_mean'] - means['control_mean']
interval = stats.t.interval(0.95, df=len(difference)-1, loc=difference.mean(), scale=stats.sem(difference))
paired_test = stats.ttest_rel(means['treated_mean'], means['control_mean'])
