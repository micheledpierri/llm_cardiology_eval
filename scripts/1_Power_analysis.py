# ------------------------------------------------------------
# LLMs Evaluation - Pilot Study and power analysis
# Michele Danilo Pierri MD PhD
# 30/03/2024
# ------------------------------------------------------------

# import necessary libraries

import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare
import statsmodels.stats.power as smp

# Data loading and preparation

file_path = "1_Pilot.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")


# Mean ratings for each row
df['Rating_Mean'] = df[['Accuracy', 'Completeness', 'Clarity', 'Coherence']].mean(axis=1)

# Mean by model and question
mean_scores = df.groupby(['Model', 'Question'])['Rating_Mean'].mean().reset_index()


# Wide table for Friedman
wide_df = mean_scores.pivot(index='Question', columns='Model', values='Rating_Mean')


# Friedman test
friedman_stat, p_value = friedmanchisquare(
    wide_df['ChatGPT'], wide_df['Claude'], wide_df['Gemini']
)

# Calculate Kendall's W
k = 3  # models
n = wide_df.shape[0]  # questions
kendalls_w = friedman_stat / (n * (k - 1))
# old formulation kendalls_w = (12 * friedman_stat) / (k**2 * n * (k + 1))



# Cohen's f from W (approximation)
f_effect_size = np.sqrt(kendalls_w / (1 - kendalls_w))

# Power analysis for observed effect
analysis = smp.FTestAnovaPower()
sample_size_needed = analysis.solve_power(effect_size=f_effect_size, alpha=0.05, power=0.8, k_groups=3)
sample_size_needed = int(np.ceil(sample_size_needed))

# Calculate theoretical f for delta = 0.5
std_within = wide_df.std(axis=1).mean()
delta = 0.5
sigma_effect = delta / np.sqrt(2)
f_from_delta = sigma_effect / std_within

# Output results
results = {
    "friedman_stat": friedman_stat,
    "p_value": p_value,
    "kendalls_w": kendalls_w,
    "f_effect_size_observed": f_effect_size,
    "sample_size_needed_for_observed_effect": sample_size_needed,
    "std_within_models": std_within,
    "cohens_f_for_delta_0.5": f_from_delta
}

pd.DataFrame(results, index=[0]).to_csv("stat_analysis_power.csv", index=False)

for result in results:
    print(f"{result}: {results[result]:4g} \n")