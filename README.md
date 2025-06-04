# Multimodal EHR Mining of CABG Patients (MIMIC-IV)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Requirements](https://img.shields.io/badge/dependencies-requirements.txt-green.svg)](./requirements.txt)

This repository contains the complete workflow and codebase for the study:  
**"Multimodal EHR Analysis of CABG Patients: Integrating Structured and Unstructured Data for Anemia-Outcome Studies in MIMIC-IV"**

---

## 🧠 Project Overview

This project proposes a methodological case study using the MIMIC-IV database to:
- Identify patients undergoing **coronary artery bypass grafting (CABG)**;
- Extract **preoperative hemoglobin** values and classify **anemia severity**;
- Parse **free-text discharge summaries** to detect **postoperative complications**;
- Evaluate the feasibility, limitations, and reproducibility of EHR mining workflows.

We focus on structured tables (e.g., `procedures_icd`, `labevents`, `admissions`) and unstructured clinical notes (`noteevents`).

---

## 🗂 Repository Structure

```bash
mimic-cabg-anemia/
├── data/                 # (empty, local use only)
├── notebooks/            # Jupyter notebooks per workflow step
├── scripts/              # Reusable Python scripts
├── docs/                 # Figures, diagrams, explanations
├── README.md             # Project description
├── requirements.txt      # Required packages
├── LICENSE               # Open license (MIT)
└── .gitignore
```

---

## ⚙️ Requirements

Install the required packages with:

```bash
pip install -r requirements.txt
```

Main packages include:
- `pandas`
- `numpy`
- `scipy`
- `regex`
- `jupyter`
- `matplotlib`
- `statsmodels`

---

## 📊 Notebooks Included

| Notebook                                | Description                                |
|----------------------------------------|--------------------------------------------|
| `01_cohort_selection.ipynb`            | CABG patient identification via ICD-9      |
| `02_lab_extraction.ipynb`              | Hemoglobin value extraction and filtering  |
| `03_anemia_classification.ipynb`       | WHO-based anemia stratification            |
| `04_note_parsing.ipynb`                | NLP processing of discharge summaries      |
| `05_stats_analysis.ipynb`              | Statistical testing and visualization      |

---

## 📎 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

## 🤝 Acknowledgements

This research uses the publicly available [MIMIC-IV](https://physionet.org/content/mimiciv/2.2/) and [MIMIC-IV-Note](https://physionet.org/content/mimic-iv-note/2.2/) databases.  
Access was granted upon completion of the required credentialing and data use agreement via PhysioNet.

---

## 📬 Contact

For questions or collaboration proposals, please contact: **Michele Pierri**
