# ------------------------------------------------------------
# LLMs Evaluation - Figure 2
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Create Figure 2 with Dunn's test p-values (hardcoded) heatmap
# ------------------------------------------------------------

# import necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style
sns.set(style="whitegrid", font_scale=1.2)
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "axes.titlesize": "large",
    "axes.labelsize": "medium",
    "xtick.labelsize": "small",
    "ytick.labelsize": "small",
    "legend.fontsize": "small",
    "figure.figsize": (8, 4),
    "axes.prop_cycle": plt.cycler(color=["#000000", "#555555", "#AAAAAA"])
})

# Define criteria and pairwise comparisons
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
comparisons = ['ChatGPT vs Claude', 'ChatGPT vs Gemini', 'Claude vs Gemini']

# Hardcoded p-values from updated Dunn’s test
dunn_data = {
    'Accuracy': {
        'ChatGPT vs Claude': 0.5121,
        'ChatGPT vs Gemini': 0.0001,
        'Claude vs Gemini': 0.0177
    },
    'Completeness': {
        'ChatGPT vs Claude': 0.0190,
        'ChatGPT vs Gemini': 0.0000,
        'Claude vs Gemini': 0.0001
    },
    'Clarity': {
        'ChatGPT vs Claude': 0.2417,
        'ChatGPT vs Gemini': 0.0000,
        'Claude vs Gemini': 0.0022
    },
    'Coherence': {
        'ChatGPT vs Claude': 0.066,
        'ChatGPT vs Gemini': 0.0000,
        'Claude vs Gemini': 0.0029
    }
}

# Convert to DataFrame for heatmap
heatmap_data = pd.DataFrame(index=criteria, columns=comparisons)
for crit in criteria:
    for cmp in comparisons:
        heatmap_data.loc[crit, cmp] = dunn_data[crit][cmp]
heatmap_data = heatmap_data.astype(float)

# Plot heatmap
plt.figure(figsize=(8, 4))
sns.heatmap(heatmap_data, annot=True, fmt=".4f", cmap="Greys", cbar_kws={'label': 'p-value'},
            linewidths=0.5, linecolor='black')

plt.xlabel("Model Pair")
plt.ylabel("Evaluation Criterion")
plt.tight_layout()

# Save figure in multiple formats
plt.savefig("Figure2.png", dpi=600)
plt.savefig("Figure2.pdf", format='pdf')
plt.savefig("Figure2.tiff", format='tiff', dpi=600)
plt.show()