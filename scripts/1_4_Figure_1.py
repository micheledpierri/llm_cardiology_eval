# ------------------------------------------------------------
# Figure 1 - Barplot of Mean Scores by AI Model and Criterion
# Michele Danilo Pierri MD PhD
# 30/03/2024
# ------------------------------------------------------------

# Import libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Load the Excel file
file_path = "1_DoctorAI_reorg.xlsx"
df = pd.read_excel(file_path)

# Calculate mean and SD for each model and criterion

summary_stats = df.groupby(['Model'])[['Accuracy', 'Completeness', 'Clarity', 'Coherence']].agg(['mean', 'std'])
summary_stats.columns = ['_'.join(col) for col in summary_stats.columns]
summary_stats.reset_index(inplace=True)

# Restructure data for the barplot

plot_data = []

for crit in ['Accuracy', 'Completeness', 'Clarity', 'Coherence']:
    for _, row in summary_stats.iterrows():
        plot_data.append({
            'Criterion': crit,
            'Model': row['Model'],
            'Mean': row[f'{crit}_mean'],
            'SD': row[f'{crit}_std']
        })

df_plot = pd.DataFrame(plot_data)

# Plotting

plt.figure(figsize=(8, 6))
sns.set(style="whitegrid", font_scale=1.2)
sns.barplot(data=df_plot, x='Criterion', y='Mean', hue='Model', ci=None,
            palette=['#000000', '#555555', '#AAAAAA'], edgecolor='black')

# Add error bars
for i, row in df_plot.iterrows():
    x_offset = {'ChatGPT': -0.25, 'Claude': 0.0, 'Gemini': 0.25}[row['Model']]
    x = ['Accuracy', 'Completeness', 'Clarity', 'Coherence'].index(row['Criterion']) + x_offset
    plt.errorbar(x, row['Mean'], yerr=row['SD'], fmt='none', ecolor='black', capsize=3, linewidth=1)

plt.ylim(0.5, 5.2)
plt.ylabel("Mean Score (± SD)")
#plt.title("Figure 1. Mean Evaluation Scores by AI Model and Criterion")
plt.legend(title="Model")
plt.tight_layout()

# Save the figure

plt.savefig("Figure1.png", dpi=600)

plt.show()

