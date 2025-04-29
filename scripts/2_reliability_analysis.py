# ------------------------------------------------------------
# LLMs Evaluation - Reliability Analysis
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Assess inter-rater agreement using classical Kendall's W,
#          Friedman-based Kendall's W (via Pingouin), and Quadratic Weighted Kappa.
# ------------------------------------------------------------

import pandas as pd
from itertools import combinations
from sklearn.metrics import cohen_kappa_score
import pingouin as pg

# defining the path and the criteria

file_path = "2_Data.xlsx"
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
reviewers = ['Reviewer1', 'Reviewer2', 'Reviewer3']

# initialize results lists
kappa_results = []
friedman_results = []
kendall_classic_results = []

# defining matrix for kendall W calculation
# Note: This function assumes that the input matrix is complete (no NaNs).

def kendalls_w(matrix):
    m, n = matrix.shape
    ranks = matrix.rank(axis=0)
    R = ranks.sum(axis=1)
    S = ((R - R.mean())**2).sum()
    W = 12 * S / (n**2 * (m**3 - m))
    return W

for crit in criteria:
    df = pd.read_excel(file_path, sheet_name=crit)
    df['Criterion'] = crit

    # Long format per reviewer
    long_df = df.melt(
        id_vars=["Request", "Model", "Origin", "Diagnosis", "Criterion"],
        value_vars=reviewers,
        var_name="Reviewer", value_name="Score"
    )
    long_df['Score'] = pd.to_numeric(long_df['Score'], errors='coerce')
    long_df['Subject'] = long_df['Request'].astype(str) + "_" + long_df['Model']

    # Pivot to wide format for pairwise comparison
    pivot_df = long_df.pivot_table(index="Subject", columns="Reviewer", values="Score")
    pivot_df = pivot_df.dropna()

    # --- Classical Kendall's W ---
    W = kendalls_w(pivot_df)
    kendall_classic_results.append({
        "Criterion": crit,
        "Kendall's W (classical)": round(W, 3)
    })

    # --- Pingouin Friedman-based Kendall's W ---
    friedman = pg.friedman(data=long_df, dv='Score', within='Reviewer', subject='Subject')
    friedman_results.append({
        'Criterion': crit,
        "Kendall's W (friedman)": round(friedman['W'].values[0], 3),
        "p-value": round(friedman['p-unc'].values[0], 4)
        })

    # --- Pairwise Quadratic Weighted Kappa ---
    for r1, r2 in combinations(pivot_df.columns, 2):
        kappa = cohen_kappa_score(pivot_df[r1], pivot_df[r2], weights='quadratic')
        kappa_results.append({
            'Criterion': crit,
            'Reviewer Pair': f'{r1} vs {r2}',
            'Weighted Kappa': round(kappa, 3),
            'Interpretation': (
                'Poor (<0.20)' if kappa < 0.2 else
                'Fair (0.21–0.40)' if kappa < 0.41 else
                'Moderate (0.41–0.60)' if kappa < 0.61 else
                'Substantial (0.61–0.80)' if kappa < 0.81 else
                'Almost Perfect (>0.80)'
            )
        })

# Export results
pd.DataFrame(kappa_results).to_csv("reliability_kappa.csv", index=False)
pd.DataFrame(kendall_classic_results).to_csv("reliability_kendall.csv", index=False)
pd.DataFrame(friedman_results).to_csv("reliability_kendall_friedman.csv", index=False)

print("Reliability analysis completed and saved to CSV.")
