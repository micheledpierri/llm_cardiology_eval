# ------------------------------------------------------------
# LLMs Evaluation - Sensitivity Analysis
# Michele Danilo Pierri MD PhD
# 30/03/2024
# ------------------------------------------------------------

# Import libraries

import pandas as pd
from scipy.stats import kruskal


# Load the Excel file

df = pd.read_excel("1_DoctorAI_reorg.xlsx")


# Define criteria and reviewers

criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
reviewers = ['Reviewer1', 'Reviewer2', 'Reviewer3']

# Initialize results

sensitivity_results = []

for reviewer_out in reviewers:
    df_reduced = df[df['Reviewer'] != reviewer_out]

    # Mean of the two remaining reviewers for each prompt × model
    df_mean = df_reduced.groupby(['Request', 'Model'])[criteria].mean().reset_index()

    for crit in criteria:
        models = df_mean['Model'].unique()
        groups = [df_mean[df_mean['Model'] == model][crit] for model in models]
        stat, p = kruskal(*groups)
        sensitivity_results.append({
            'Excluded Reviewer': reviewer_out,
            'Criterion': crit,
            'Kruskal-Wallis H': round(stat, 3),
            'p-value': round(p, 4),
            'Significant (p < 0.05)': p < 0.05
        })

# Create the results table

df_sensitivity = pd.DataFrame(sensitivity_results)
print(df_sensitivity)
