# Evaluating Large Language Models in Cardiology

This repository contains all data, code, and figures related to the study:

**"Evaluating Large Language Models in Cardiology: A Comparative Study of ChatGPT, Claude, and Gemini"**

[![Python](https://img.shields.io/badge/python-3.12.4-blue.svg)](https://www.python.org/downloads/release/python-3124/)
[![requirements](https://img.shields.io/badge/install-pip--requirements.txt-brightgreen)](./requirements.txt)


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
- All scripts written in Python 3.12

## Repository Structure

```text
llm-cardiology-eval/
requirements.txt
├── data/
│   ├── 1_DoctorAI_reorg.xlsx
│   ├── 1_DoctorAI_words.xlsx
├── scripts/
│   ├── 1_1_Power_Analysis.py
│   ├── 1_2_Statistical_Analysis.py
│   ├── 1_3_Sensitivity_Analysis.py
│   ├── 1_4_Figure_1.py
│   └── 1_5_Figure_2.py
├── figures/
│   ├── Figure1.png
│   └── Figure2.png
├── tables/
│   ├── 
│   ├── ...
├── LICENSE
├── CITATION.cff
└── README.md
```
## Reproducibility
To reproduce the figures and statistical analyses, make sure that the datasets and scripts are correctly located.
**Figure scripts assume that the corresponding Excel files are in the same directory.** If you keep datasets in a separate folder (e.g., `data/`), update the `file_path` variable at the beginning of each script accordingly.

## Data Availability

All data used in this study are available in anonymized form under the `/data` directory. Original prompts, evaluation scores, and reliability statistics are included.

## Reproducing the Analysis

1. Clone the repository:
   git clone https://github.com/micheledpierri/llm-cardiology-eval.git
   cd llm-cardiology-eval

2. Install required Python packages:
   pip install -r requirements.txt

3. Run main analysis:
   python scripts/analysis_main.py

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Citation

If you use this work, please cite it using the `CITATION.cff` file

## Contact

For questions, please contact: micheledanilo.pierri@ospedaliriuniti.marche.it
