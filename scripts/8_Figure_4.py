# ------------------------------------------------------------
# LLMs Evaluation - Figure 4
# Michele Danilo Pierri MD PhD
# 30/03/2024
# Purpose: Create Figure 3 with differences in user profile
# ------------------------------------------------------------

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel and process each criterion
file_path = "2_Data.xlsx"
criteria = ['Accuracy', 'Completeness', 'Clarity', 'Coherence']
plot_data = pd.DataFrame()

for sheet in criteria:
    df = pd.read_excel(file_path, sheet_name=sheet)
    df['Mean'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].mean(axis=1)
    df['SD'] = df[['Reviewer1', 'Reviewer2', 'Reviewer3']].std(axis=1)
    df['Criterion'] = sheet
    plot_data = pd.concat([plot_data, df], ignore_index=True)

# Group by User Type
summary = plot_data.groupby(['Origin', 'Criterion'])['Mean'].agg(['mean', 'std']).reset_index()
summary.columns = ['Origin', 'Criterion', 'Mean', 'SD']

# Plot
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid", font_scale=1.2)

ax = sns.barplot(data=summary, x='Criterion', y='Mean', hue='Origin',
                 palette='Greys', ci=None, edgecolor='black')

# Add error bars
for i, row in summary.iterrows():
    x = i % 4 + (-0.2 if row['Origin'] == 'Patient' else 0.2)
    plt.errorbar(x, row['Mean'], yerr=row['SD'], fmt='none',
                 ecolor='black', capsize=3, linewidth=1)

plt.ylim(0.5, 5.2)
plt.ylabel("Mean Score (± SD)")
plt.xlabel("Evaluation Criterion")
plt.legend(title="User Type")
plt.tight_layout()

# Save
plt.savefig("Figure_UserType.png", dpi=600)
plt.savefig("Figure_UserType.pdf", format='pdf')
plt.savefig("Figure_UserType.tiff", format='tiff', dpi=600)
plt.show()
