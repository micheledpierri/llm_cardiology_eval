# ------------------------------------------------------------
# LLMs Evaluation - Statistical Analysis
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Perform descriptive statistics, normality evaluazion with Shapiro test,
#          Analyze data with Kruskall-Wallis and Dunn test with bootstrap for confidence-limits,
#          Subgroups analysis for diagnostic phase and user type
# ------------------------------------------------------------


# Import necessary libraries

from itertools import combinations
from scipy.stats import kruskal, mannwhitneyu, shapiro
import numpy as np
import pandas as pd
import scikit_posthocs as sp


# Initial configuration

file_path = "2_Data.xlsx"
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
models = ['ChatGPT', 'Claude', 'Gemini']

# Loading data
# Read all sheets and concatenate into a single DataFrame

df_all = []
for crit in criteria:
    df = pd.read_excel(file_path, sheet_name=crit)
    df['Criterion'] = crit
    df_all.append(df)
df_all = pd.concat(df_all, ignore_index=True)

df_long = df_all.melt(
    id_vars=["Request", "Model", "Origin", "Diagnosis", "Criterion"],
    value_vars=["Reviewer1", "Reviewer2", "Reviewer3"],
    var_name="Reviewer", value_name="Score"
)
df_long['Score'] = pd.to_numeric(df_long['Score'], errors='coerce')

# defining the bootstrap function

def bootstrap_ci(data1, data2, n_boot=10000, ci=95):
    diffs = []
    for _ in range(n_boot):
        s1 = np.random.choice(data1, size=len(data1), replace=True)
        s2 = np.random.choice(data2, size=len(data2), replace=True)
        diffs.append(np.mean(s1) - np.mean(s2))
    lower = np.percentile(diffs, (100 - ci) / 2)
    upper = np.percentile(diffs, 100 - (100 - ci) / 2)
    return np.mean(diffs), lower, upper

# ------------------------------
# Descriptive Statistics
# ------------------------------

desc_stats = []
for crit in criteria:
    for model in models:
        scores = df_long[(df_long["Criterion"] == crit) & (df_long["Model"] == model)]["Score"]
        desc_stats.append({
            "Model": model,
            "Criterion": crit,
            "N": scores.count(),
            "Mean": round(scores.mean(), 3),
            "Median": round(scores.median(), 3),
            "SD": round(scores.std(), 3),
            "IQR": round(scores.quantile(0.75) - scores.quantile(0.25), 3)
        })
desc_df = pd.DataFrame(desc_stats)
desc_df.to_csv("stat_analysis_descriptive.csv", index=False)

# ------------------------------
# Shapiro test for normality
# ------------------------------

norm_results = []
for crit in criteria:
    for model in models:
        scores = df_long[(df_long["Criterion"] == crit) & (df_long["Model"] == model)]["Score"]
        stat, p = shapiro(scores)
        norm_results.append({
            "Model": model,
            "Criterion": crit,
            "W-statistic": round(stat, 3),
            "p-value": round(p, 4),
            "Normality": 'Non-normal (p < 0.05)' if p < 0.05 else 'Normal (p ≥ 0.05)'
        })
norm_df = pd.DataFrame(norm_results)
norm_df.to_csv("stat_analysis_shapiro.csv", index=False)


# ------------------------------
# Kruskal-Wallis + Dunn + Bootstrap CI
# (Post-hoc analysis)   
# ------------------------------

kw_results = []
dunn_results = []

for crit in criteria:
    data = df_long[df_long['Criterion'] == crit]
    groups = [data[data['Model'] == model]['Score'] for model in models]
    stat, p = kruskal(*groups)
    kw_results.append({
        "Criterion": crit,
        "H-statistic": round(stat, 3),
        "p-value": round(p, 4),
        "Significant": p < 0.05
    })
    dunn = sp.posthoc_dunn(data, val_col='Score', group_col='Model', p_adjust='bonferroni').round(4)
    for m1, m2 in combinations(models, 2):
        data1 = data[data["Model"] == m1]["Score"].values
        data2 = data[data["Model"] == m2]["Score"].values
        delta, ci_low, ci_high = bootstrap_ci(data1, data2)
        dunn_results.append({
            "Criterion": crit,
            "Model A": m1,
            "Model B": m2,
            "Δ Mean": round(delta, 3),
            "95% CI": f"[{ci_low:.3f} to {ci_high:.3f}]",
            "p-value": dunn.loc[m1, m2]
        })
pd.DataFrame(kw_results).to_csv("stat_analysis_kruskal.csv", index=False)
pd.DataFrame(dunn_results).to_csv("stat_analysis_posthoc_dunn.csv", index=False)

# ------------------------------
# Diagnostic Phase Analysis
# ------------------------------

diag_results = []
for crit in criteria:
    subset = df_long[df_long['Criterion'] == crit]
    pre = subset[subset["Diagnosis"] == "Pre"]["Score"].values
    post = subset[subset["Diagnosis"] == "Post"]["Score"].values
    stat, p = mannwhitneyu(post, pre, alternative='two-sided')
    delta, ci_low, ci_high = bootstrap_ci(post, pre)
    diag_results.append({
        "Criterion": crit,
        "Mean Pre": round(np.mean(pre), 3),
        "Mean Post": round(np.mean(post), 3),
        "Δ Post - Pre": round(delta, 3),
        "95% CI": f"[{ci_low:.3f} to {ci_high:.3f}]",
        "U statistic": stat,
        "p-value": round(p, 4),
        "Significant": p < 0.05
    })
pd.DataFrame(diag_results).to_csv("stat_analysis_diagnostic_phase.csv", index=False)

# ------------------------------
# User Type Analysis
# ------------------------------

user_results = []
for crit in criteria:
    subset = df_long[df_long['Criterion'] == crit]
    pat = subset[subset["Origin"] == "Patient"]["Score"].values
    doc = subset[subset["Origin"] == "Doctor"]["Score"].values
    stat, p = mannwhitneyu(pat, doc, alternative='two-sided')
    delta, ci_low, ci_high = bootstrap_ci(pat, doc)
    user_results.append({
        "Criterion": crit,
        "Mean Patient": round(np.mean(pat), 3),
        "Mean Doctor": round(np.mean(doc), 3),
        "Δ Patient - Doctor": round(delta, 3),
        "95% CI": f"[{ci_low:.3f} to {ci_high:.3f}]",
        "U statistic": stat,
        "p-value": round(p, 4),
        "Significant": p < 0.05
    })
pd.DataFrame(user_results).to_csv("stat_analysis_user_type.csv", index=False)

print("All results exported to CSV.")
