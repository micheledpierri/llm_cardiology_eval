[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Requirements](https://img.shields.io/badge/dependencies-requirements.txt-green.svg)](./requirements.txt)


# Evaluating Large Language Models in Cardiology

This repository contains all data, code, and figures related to the study:

**"Evaluating Large Language Models in Cardiology: A Comparative Study of ChatGPT, Claude, and Gemini"**

## 📄 Abstract

This study systematically compares the performance of three large language models (ChatGPT, Claude, and Gemini) in cardiology-related clinical scenarios. Using 70 simulated prompts representing both pre- and post-diagnostic phases and two user profiles (patient and doctor), responses were rated by three board-certified cardiologists on four quality criteria: scientific accuracy, completeness, clarity, and coherence. Statistical analyses confirmed ChatGPT’s superiority, though no model achieved maximal performance. Results support the need for domain-specific fine-tuning and human-in-the-loop oversight.

## 🧪 Study Design

- Models Evaluated: ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google DeepMind)
- Prompts: 70 clinical questions stratified by diagnostic phase and user type
- Scoring: 5-point Likert scale, four criteria
- Reviewers: 3 blinded cardiologists
- Evaluation Period: September–December 2024

## 📊 Methods

- Non-parametric tests (Kruskal–Wallis, Dunn’s test, Mann–Whitney U)
- Inter-rater reliability (Kendall’s W, Weighted Kappa)
- Sensitivity analysis (leave-one-reviewer-out)
- All scripts written in Python 

## 📁 Repository Structure

```text
llm-cardiology-eval/
├── data/
│   ├── 1_Pilot.xlsx
│   └── 2_Data.xlslx
├── scripts/
│   ├── 1_Power_analysis.py
│   ├── 2_reliability_analysis.py
│   ├── 3_Statistical_Analysis.py
│   ├── 4_Sensitivity_analysis.py
│   ├── 5_Figure_1.py
│   ├── 6_Figure_2.py
│   ├── 7_Figure_3.py
│   └── 8_Figure_4.py
├── figures/
│   ├── Figure1.pdf
│   ├── Figure2.pdf
│   ├── Figure_DiagnosticPhase_wErrorBars.pdf
│   └── Figure_UserType.pdf
├── tables/
│   ├── reliability_kappa.csv
│   ├── reliability_kendall.csv
│   ├── reliability_kendall_friedman.csv
│   ├── sensitivity_analysis.csv
│   ├── stat_analysis_descriptive.csv
│   ├── stat_analysis_diagnostic_phase.csv
│   ├── stat_analysis_kruskal.csv
│   ├── stat_analysis_posthoc_dunn.csv
│   ├── stat_analysis_power.csv
│   ├── stat_analysis_shapiro.csv
│   └── stat_analysis_user_type.csv
├── LICENSE
├── requirements.txt
└── README.md
```

## 🗃️ Data Availability

All data used in this study are available in anonymized form under the `/data` directory. Original prompts, evaluation scores, and reliability statistics are included.

## ▶️ Reproducing the Analysis

1. Clone the repository:
   git clone https://github.com/micheledpierri/llm-cardiology-eval.git
   cd llm-cardiology-eval

2. Create virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate  (on Windows: venv\Scripts\activate)
   pip install -r requirements.txt

3. Run main analysis:
   python scripts/analysis_main.py

⚠️ Scripts expect data files to be in the same folder. Copy `.csv`/`.xlsx` files into the script directory before running.


## 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.


## 🤝 Contact

For questions, please contact: micheledanilo.pierri@ospedaliriuniti.marche.it
