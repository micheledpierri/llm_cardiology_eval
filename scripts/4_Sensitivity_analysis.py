# ------------------------------------------------------------
# LLMs Evaluation - Sensitivity Analysis
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Perform leave-one-reviewer-out sensitivity analysis
# ------------------------------------------------------------

# Import necessary libraries

import pandas as pd
from scipy.stats import kruskal

# setting di file path and lists for criteria and reviewers

file_path = "2_Data.xlsx"
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
reviewers = ['Reviewer1', 'Reviewer2', 'Reviewer3']

# Concatenate all sheets into a single long dataframe

dfs = []
for crit in criteria:
    df = pd.read_excel(file_path, sheet_name=crit)
    df['Criterion'] = crit
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)

# Melt to long format for scoring fields

df_long = df_all.melt(
    id_vars=["Request", "Model", "Origin", "Diagnosis", "Criterion"],
    value_vars=reviewers,
    var_name="Reviewer", value_name="Score"
)
df_long['Score'] = pd.to_numeric(df_long['Score'], errors='coerce')

# Perform sensitivity analysis by removing one reviewer at a time

sensitivity_results = []

for reviewer_out in reviewers:
    df_reduced = df_long[df_long['Reviewer'] != reviewer_out]
    df_mean = df_reduced.groupby(['Request', 'Model', 'Criterion'])['Score'].mean().reset_index()

    for crit in criteria:
        subset = df_mean[df_mean['Criterion'] == crit]
        groups = [subset[subset['Model'] == model]['Score'] for model in subset['Model'].unique()]
        stat, p = kruskal(*groups)
        sensitivity_results.append({
            'Excluded Reviewer': reviewer_out,
            'Criterion': crit,
            'Kruskal-Wallis H': round(stat, 3),
            'p-value': round(p, 4),
            'Significant (p < 0.05)': p < 0.05
        })

# Export the results to CSV
pd.DataFrame(sensitivity_results).to_csv("sensitivity_analysis.csv", index=False)
print("Sensitivity analysis completed and saved to 'sensitivity_analysis.csv'")
