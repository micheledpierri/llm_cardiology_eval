# ------------------------------------------------------------
# LLMs Evaluation - Figure 3
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Create Figure 3 with differences in diagnostic phase
# ------------------------------------------------------------

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess
file_path = "2_Data.xlsx"
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
plot_data = pd.DataFrame()

for sheet in criteria:
    df = pd.read_excel(file_path, sheet_name=sheet)
    df['Mean'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].mean(axis=1)
    df['SD'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].std(axis=1)
    df['Criterion'] = sheet
    plot_data = pd.concat([plot_data, df], ignore_index=True)

# Compute means and SD per (Diagnosis, Criterion)
summary = plot_data.groupby(['Diagnosis', 'Criterion'])[['Mean']].agg(['mean', 'std']).reset_index()
summary.columns = ['Diagnosis', 'Criterion', 'Mean', 'SD']

# Plot
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid", font_scale=1.2)

ax = sns.barplot(
    data=summary,
    x='Criterion',
    y='Mean',
    hue='Diagnosis',
    palette='Greys',
    ci=None,
    edgecolor='black'
)

# Add error bars 
for bar, (_, row) in zip(ax.patches, summary.iterrows()):
    x = bar.get_x() + bar.get_width() / 2
    y = row['Mean']
    err = row['SD']
    if pd.notnull(err):
        plt.errorbar(x, y, yerr=err, fmt='none', ecolor='black', capsize=3, linewidth=1)

plt.ylim(0.5, 5.2)
plt.ylabel("Mean Score (± SD)")
plt.xlabel("Evaluation Criterion")
plt.legend(title="Diagnostic Phase")
plt.tight_layout()

# Save in all required formats
plt.savefig("Figure_DiagnosticPhase_wErrorBars.png", dpi=600)
plt.savefig("Figure_DiagnosticPhase_wErrorBars.pdf", format='pdf')
plt.savefig("Figure_DiagnosticPhase_wErrorBars.tiff", format='tiff', dpi=600)
plt.show()

