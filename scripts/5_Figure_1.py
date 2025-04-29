# ------------------------------------------------------------
# LLMs Evaluation - Figure 1
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Create Figure 1 with error bars for each criterion
# ------------------------------------------------------------

# Import necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the Excel file
file_path = "2_Data.xlsx"
sheet_names = ["Accuracy", "Completeness", "Clarity", "Coherence"]

# Container for processed data
plot_data = []

# Loop over each sheet/criterion
for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    
    # Calculate mean and standard deviation across reviewers
    df['Mean'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].mean(axis=1)
    df['SD'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].std(axis=1)
    
    # Aggregate by model
    grouped = df.groupby('Model').agg({'Mean': 'mean', 'SD': 'mean'}).reset_index()
    grouped['Criterion'] = sheet
    plot_data.append(grouped)

# Combine all results into one DataFrame
df_plot = pd.concat(plot_data, ignore_index=True)

# Plot
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid", font_scale=1.2)
sns.barplot(data=df_plot, x='Criterion', y='Mean', hue='Model',
            ci=None, palette=['#000000', '#555555', '#AAAAAA'], edgecolor='black')

# Add error bars manually
criterion_order = ["Accuracy", "Completeness", "Clarity", "Coherence"]
model_offsets = {'ChatGPT': -0.25, 'Claude': 0.0, 'Gemini': 0.25}

for i, row in df_plot.iterrows():
    x_base = criterion_order.index(row['Criterion'])
    x = x_base + model_offsets[row['Model']]
    plt.errorbar(x, row['Mean'], yerr=row['SD'], fmt='none', 
                 ecolor='black', capsize=3, linewidth=1)

plt.ylim(0.5, 5.2)
plt.ylabel("Mean Score (± SD)")
plt.legend(title="Model")
plt.tight_layout()

# Save the figure in all required formats

plt.savefig("Figure1.png", dpi=600)
plt.savefig("Figure1.pdf", format='pdf')
plt.savefig("Figure1.tiff", format='tiff', dpi=600)
plt.show()
