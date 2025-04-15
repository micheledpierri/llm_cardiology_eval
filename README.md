# Evaluating Large Language Models in Cardiology

This repository contains all data, code, and figures related to the study:

**"Evaluating Large Language Models in Cardiology: A Comparative Study of ChatGPT, Claude, and Gemini"**

## Abstract

This study systematically compares the performance of three large language models (ChatGPT, Claude, and Gemini) in cardiology-related clinical scenarios. Using 70 simulated prompts representing both pre- and post-diagnostic phases and two user profiles (patient and doctor), responses were rated by three expert cardiologists on four quality criteria: scientific accuracy, completeness, clarity, and coherence. Statistical analyses confirmed ChatGPT’s superiority, though no model achieved maximal performance. Results support the need for domain-specific fine-tuning and human-in-the-loop oversight.

## Study Design

- Models Evaluated: ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google DeepMind)
- Prompts: 70 clinical questions stratified by diagnostic phase and user type
- Scoring: 5-point Likert scale, four criteria
- Reviewers: 3 blinded cardiologists
- Evaluation Period: September–December 2024

## Methods

- Non-parametric tests (Kruskal–Wallis, Dunn’s test, Mann–Whitney U)
- Inter-rater reliability (Kendall’s W, Weighted Kappa)
- Sensitivity analysis (leave-one-reviewer-out)
- All scripts written in Python 3.9

## Repository Structure
'''
llm-cardiology-eval/
├── data/
│   ├── 1_DoctorAI_reorg.xlsx
│   ├── 1_DoctorAI_words.xlsx
│   └── 1_DoctorAI_kendall.xlsx
├── scripts/
│   ├── analysis_main.py
│   ├── interrater_analysis.py
│   ├── sensitivity_analysis.py
│   └── plot_figures.py
├── figures/
│   ├── Figure1_scores_by_model.png
│   └── Figure2_dunn_heatmap.png
├── tables/
│   ├── Table1_KendallW.csv
│   ├── ...
├── LICENSE
├── CITATION.cff
└── README.md
'''
## Data Availability

All data used in this study are available in anonymized form under the `/data` directory. Original prompts, evaluation scores, and reliability statistics are included.

## Reproducing the Analysis

1. Clone the repository:
   git clone https://github.com/micheledpierri/llm-cardiology-eval.git
   cd llm-cardiology-eval

2. Create virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate  (on Windows: venv\Scripts\activate)
   pip install -r requirements.txt

3. Run main analysis:
   python scripts/analysis_main.py

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Citation

If you use this work, please cite it using the `CITATION.cff` file

## 🤝 Contact

For questions, please contact: micheled.pierri@ospedaliriuniti.marche.it
