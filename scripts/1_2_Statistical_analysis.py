# ------------------------------------------------------------
# DoctorAI - Statistical Analysis
# Michele Danilo Pierri
# 30/03/2024
# ------------------------------------------------------------

# Import libraries

import numpy as np
import pandas as pd
from scipy.stats import shapiro
from scipy.stats import kruskal
from scipy.stats import mannwhitneyu
import scikit_posthocs as sp
from itertools import combinations

# -------------------------------------------------------------
# 0 - Create bootstrap function for confidence intervals
# -------------------------------------------------------------

def bootstrap_ci(data1, data2, n_boot=10000, ci=95):
    """
    Calculate bootstrap confidence intervals for the difference between means
    
    Parameters:
    data1, data2: arrays of observations
    n_boot: number of bootstrap iterations
    ci: confidence interval level
    
    Returns:
    mean difference, lower CI bound, upper CI bound
    """
    diffs = []
    for _ in range(n_boot):
        s1 = np.random.choice(data1, size=len(data1), replace=True)
        s2 = np.random.choice(data2, size=len(data2), replace=True)
        diffs.append(np.mean(s1) - np.mean(s2))
    lower = np.percentile(diffs, (100 - ci) / 2)
    upper = np.percentile(diffs, 100 - (100 - ci) / 2)
    return np.mean(diffs), lower, upper


# ------------------------------------------------------------------
# 1 Loading data from Excel
# ------------------------------------------------------------------

file_path = "1_DoctorAI_reorg.xlsx"
df = pd.read_excel(file_path)

# examining the data
print("Data loaded from Excel")
print(df.info())
print(df.head())
print("\n\n")

# -----------------------------------------------------
# 2 Normality test
# -----------------------------------------------------


# Reshape needed to examine normality for each model and criterion

results = []

criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
models = df['Model'].unique()

# For every model and criterion, the Shapiro-Wilk test is applied

for crit in criteria:
    for model in models:
        scores = df[df['Model'] == model][crit]
        stat, p = shapiro(scores)
        results.append({
            'Model': model,
            'Criterion': crit,
            'W-statistic': stat,
            'p-value': p,
            'Normality': 'Non-normal (p < 0.05)' if p < 0.05 else 'Normal (p ≥ 0.05)'
        })

shapiro_df = pd.DataFrame(results)

print("\nShapiro-Wilk Normality Test Results\n")
print(shapiro_df)
print("\n\n")


# ------------------------------------------------------
# 3 Descriptive statistics
# ------------------------------------------------------

# Create empty list to store results
descriptive_stats = []

# Calculate statistics for each model and criterion
for crit in criteria:
    for model in models:
        scores = df[df['Model'] == model][crit]
        stats = {
            'Model': model,
            'Criterion': crit,
            'N': len(scores),
            'Mean': scores.mean(),
            'SD': scores.std(),
            'Median': scores.median(),
            'IQR': scores.quantile(0.75) - scores.quantile(0.25),
            '25th': scores.quantile(0.25),
            '75th': scores.quantile(0.75)
        }
        descriptive_stats.append(stats)

# Convert to DataFrame and round numeric columns
desc_df = pd.DataFrame(descriptive_stats)
numeric_columns = ['Mean', 'SD', 'Median', 'IQR', '25th', '75th']
desc_df[numeric_columns] = desc_df[numeric_columns].round(3)

# Display results using the custom display function
print("\nDescriptive Statistics by Model and Criterion")
print(desc_df)
print("\n\n")


# -------------------------------------------
# 4 Kruskal-Wallis test e Dunn-Bonferroni
# -------------------------------------------

# Kruskal-Wallis test
kw_results = []
for crit in criteria:
    groups = [df[df['Model'] == model][crit] for model in models]
    stat, p = kruskal(*groups)
    kw_results.append({
        'Criterion': crit,
        'H-statistic': f'{stat:.3f}',
        'p-value': f'{p:.4f}',
        'Significant': p < 0.05
    })

kw_df = pd.DataFrame(kw_results)
print("\nKruskal-Wallis Test Results:")
print(kw_df)
print("\n\n")

# Post-hoc Dunn test
for crit in criteria:
    print(f"\nPost-hoc Dunn test for {crit}")
    dunn = sp.posthoc_dunn(df, val_col=crit, group_col='Model', p_adjust='bonferroni')
    
    # formatting the Dunn matrix
    dunn = dunn.round(4)
    dunn = dunn.fillna('')  
    
    # printing the Dunn matrix
    print("\nP-value matrix:")
    print(dunn)
    print("\n")
    
    # calculating the mean differences and confidence intervals
    print("Pairwise comparisons:")
    for m1, m2 in combinations(models, 2):
        data1 = df[df['Model'] == m1][crit].values
        data2 = df[df['Model'] == m2][crit].values
        delta, ci_low, ci_high = bootstrap_ci(data1, data2)
        p_value = dunn.loc[m1, m2]
        print(f"{m1} vs {m2}: ")
        print(f"  p = {p_value:.4f}")
        print(f"  Δ = {delta:.3f} [95% CI: {ci_low:.3f} to {ci_high:.3f}]\n")


# ------------------------------------------------------
# 5 subgroup analysis (diagnostic phase and user type)
# ------------------------------------------------------


# Analysis for diagnostic phase (Pre vs Post)


diagnostic_results = []

for crit in criteria:
    pre_scores = df[df['Diagnosis'] == 'Pre'][crit].values
    post_scores = df[df['Diagnosis'] == 'Post'][crit].values
    stat, p = mannwhitneyu(post_scores, pre_scores, alternative='two-sided')
    delta, ci_low, ci_high = bootstrap_ci(post_scores, pre_scores)
    diagnostic_results.append({
        'Criterion': crit,
        'Comparison': 'Post vs Pre',
        'U-statistic': stat,
        'p-value': f'{p:.4f}',
        'Significant (p < 0.05)': p < 0.05,
        'Mean Pre': round(np.mean(pre_scores), 3),
        'Mean Post': round(np.mean(post_scores), 3),
        'Δ Mean': round(delta, 3),
        '95% CI': f"[{ci_low:.3f} to {ci_high:.3f}]"
    })

# Analysis for user type (Doctor vs Patient)
origin_results = []
for crit in criteria:
    doc_scores = df[df['Origin'] == 'Doctor'][crit].values
    pat_scores = df[df['Origin'] == 'Patient'][crit].values
    stat, p = mannwhitneyu(pat_scores, doc_scores, alternative='two-sided')
    delta, ci_low, ci_high = bootstrap_ci(pat_scores, doc_scores)
    origin_results.append({
        'Criterion': crit,
        'Comparison': 'Patient vs Doctor',
        'U-statistic': stat,
        'p-value': f'{p:.6f}',
        'Significant (p < 0.05)': p < 0.05,
        'Mean Doctor': round(np.mean(doc_scores), 3),
        'Mean Patient': round(np.mean(pat_scores), 3),
        'Δ Mean': round(delta, 3),
        '95% CI': f"[{ci_low:.3f} to {ci_high:.3f}]"
    })

# Combine results into a single DataFrame
diagnostic_df = pd.DataFrame(diagnostic_results)
origin_df = pd.DataFrame(origin_results)

print("\nSubgroup Analysis Results\n")
print("Diagnostic Phase (Pre vs Post):")
print(diagnostic_df)
print("\n\n")
print("User Type (Doctor vs Patient):")
print(origin_df)
print("\n\n")
