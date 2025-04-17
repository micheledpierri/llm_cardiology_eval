# ------------------------------------------------------------
# Figure 2 - Dunn's Post Hoc Comparisons
# Michele Danilo Pierri MD PhD
# 30/03/2024
# ------------------------------------------------------------

# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file

file_path = "1_DoctorAI_reorg.xlsx"
df = pd.read_excel(file_path)

# set plotting style and parameters

sns.set(style="whitegrid", font_scale=1.2)
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "axes.titlesize": "large",
    "axes.labelsize": "medium",
    "xtick.labelsize": "small",
    "ytick.labelsize": "small",
    "legend.fontsize": "small",
    "figure.figsize": (8, 6),
    "axes.prop_cycle": plt.cycler(color=["#000000", "#555555", "#AAAAAA"])
})

# define criteria and models

criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']


# create a DataFrame for Dunn's post hoc comparisons

dunn_data = {
    'Accuracy': {'ChatGPT vs Claude': 0.5141, 'ChatGPT vs Gemini': 0.0001, 'Claude vs Gemini': 0.0207},
    'Completeness': {'ChatGPT vs Claude': 0.0185, 'ChatGPT vs Gemini': 0.0000, 'Claude vs Gemini': 0.0002},
    'Clarity': {'ChatGPT vs Claude': 0.2119, 'ChatGPT vs Gemini': 0.0000, 'Claude vs Gemini': 0.0124},
    'Coherence': {'ChatGPT vs Claude': 0.0586, 'ChatGPT vs Gemini': 0.0000, 'Claude vs Gemini': 0.0039}
}

# Restructure the data for heatmap

comparisons = ['ChatGPT vs Claude', 'ChatGPT vs Gemini', 'Claude vs Gemini']
heatmap_data = pd.DataFrame(index=criteria, columns=comparisons)

for crit in criteria:
    for cmp in comparisons:
        heatmap_data.loc[crit, cmp] = dunn_data[crit][cmp]

heatmap_data = heatmap_data.astype(float)

# plot the heatmap

plt.figure(figsize=(8, 4))
sns.heatmap(heatmap_data, annot=True, fmt=".4f", cmap="Greys", cbar_kws={'label': 'p-value'},
            linewidths=0.5, linecolor='black')

#plt.title("Figure 2. Dunn’s Post Hoc Comparisons (Bonferroni-corrected p-values)")
plt.xlabel("Model Pair")
plt.ylabel("Evaluation Criterion")
plt.tight_layout()


plt.savefig("Figure2.png", dpi=600)
plt.show()