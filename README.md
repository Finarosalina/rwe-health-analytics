# RWE Health Analytics Platform

> **Status:** work in progress. Implemented: synthetic EHR data generator, validated data loader with basic cohort logic, and an exploratory cohort EDA notebook. Planned: risk prediction, survival analysis and causal inference (see *Roadmap*).

A modular analytics framework for working with Real World Evidence (RWE) and electronic health records (EHR).  
The project is structured as a realistic healthcare data pipeline: from synthetic data generation to ingestion, cohort construction, exploratory analysis, and the foundation for downstream modeling (risk prediction, survival analysis, and causal inference).

---

Business / Clinical Objective

This project simulates a realistic Real-World Evidence (RWE) workflow using synthetic EHR data to demonstrate how patient-level healthcare data can be transformed into clinically meaningful insights and modelling-ready datasets.
It is designed to reflect use cases relevant to HEOR, clinical research, digital health, and observational analytics


Use Cases / Why it matters

Cohort construction for observational studies

Risk stratification and outcome prediction

Survival analysis for time-to-event endpoints

Treatment pattern and medication utilization analysis

Causal inference and comparative effectiveness research

Synthetic data prototyping for privacy-preserving healthcare analytics

---

Potential Digital Health Applications

The analytical workflows implemented in this project are relevant for several
digital health and precision medicine use cases, including:

• digital biomarker discovery
• remote patient monitoring
• clinical risk stratification
• early disease detection
• decision support systems

These approaches are particularly relevant for chronic disease management
contexts such as diabetes, cardiovascular disease and metabolic disorders.

---


## 1. Overview

This repository provides a reproducible environment for analysing longitudinal, patient-level healthcare data.  
It follows principles commonly used in pharmaceutical R&D, HEOR, and clinical analytics:

- Structured data ingestion and validation  
- Cohort definition logic  
- Domain-aware exploratory analysis  
- Modular organisation under `src/`  
- Reproducible workflows using notebooks  

The project currently uses synthetic EHR-style data aligned with realistic clinical patterns, but the architecture supports real datasets with minimal adaptation.

---

## 2. Tech Stack

### Core Languages & Tools
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)

### Visualization
![Matplotlib](https://img.shields.io/badge/Matplotlib-37474F?logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C8BBE?logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)

### Tooling
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)

**Planned for the modelling layer:** scikit-learn, XGBoost, lifelines / scikit-survival, DoWhy / EconML, Streamlit.

---

## 3. Project Structure

```text
rwe-health-analytics/
│
├── notebooks/
│   └── 01_exploratory_eda.ipynb      # Cohort EDA
│
├── src/
│   └── rwe_health_analytics/
│       ├── data/
│       │   └── data_loader.py        # Loading, validation, cohort logic
│       └── data_generation/
│           └── synthetic_data_generator.py
│
├── requirements.txt
├── setup.py
└── project_setup.sh
```

---

## 4. Data Flow

The system follows a structured, modular lifecycle:

### **1. Data Generation**
Synthetic patient-level data are created using clinically-inspired rules and realistic statistical distributions.

### **2. Data Ingestion**
`HealthcareDataLoader` reads and validates the raw tables, offering:

- loading by domain (patients, diagnoses, labs…)
- patient-level queries  
- data quality checks  
- basic cohort creation logic  

### **3. Exploratory Analysis**
Jupyter notebooks provide:

- demographic summaries  
- comorbidity patterns  
- laboratory distributions  
- medication behaviour  
- longitudinal event timelines  

### **4. Modelling Layer (future)**
The architecture is prepared for:

- survival analysis  
- risk prediction  
- clustering  
- causal inference pipelines  

Maintaining separation between **data → logic → analysis**.

---

## 5. Installation

```bash
git clone https://github.com/Finarosalina/rwe-health-analytics.git
cd rwe-health-analytics
```

Create environment:

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

---

## 6. Synthetic Data Generation

Run:

```bash
python src/rwe_health_analytics/data_generation/synthetic_data_generator.py
```

This generates:

```
data/raw/
    demographics.csv
    diagnoses.csv
    lab_results.csv
    medications.csv
    outcomes.csv
```

### Dataset Description

| Dataset | Description |
|---------|-------------|
| **Demographics** | Age, sex, race, BMI, smoking, insurance |
| **Diagnoses** | ICD-like codes, visit types, chronicity |
| **Laboratories** | Lab measures with normal/abnormal ranges |
| **Medications** | Prescriptions, dose, duration, specialty |
| **Outcomes** | Hospitalizations, ER visits, mortality |

Data are generated using:

- normal, log-normal, Poisson, and multinomial distributions  
- disease-driven physiological changes  
- comorbidity-based risk modeling  
- temporal sequencing for visits, prescriptions, labs and outcomes  

This enables EDA, ML, causal inference and survival analysis without PHI/PII.

---

## 7. Exploratory Analysis

Launch notebooks:

```bash
jupyter notebook
```

Notebook included:

```
notebooks/01_exploratory_eda.ipynb
```

The analysis covers:

- demographic distributions  
- comorbidity burden  
- diagnosis patterns  
- medication dynamics  
- laboratory value distributions  
- outcome timelines  

---

## 8. Roadmap

The project is structured as a Python package to support clean expansion.

Future modules may include:

- Cox PH models  
- Random Survival Forests  
- Gradient-boosted risk models  
- Propensity score pipelines  
- Streamlit dashboard  
- Docker deployment  

---

## 9. Testing

Automated tests are planned (pytest).

---

## 10. License
MIT License.

---

## 11. Author

**Maria Pais Fajín**  
GitHub: https://github.com/Finarosalina  
LinkedIn: https://linkedin.com/in/maria-pais-fajin


