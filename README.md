# SMART Survey Processing Pipeline & Machine Learning-Based Mortality Prediction

## Project Overview

This project processes raw SMART survey data (.as files) from Somalia through a complete data pipeline and builds machine learning models to predict household-level mortality. A total of 80 raw survey files were processed through four stages, resulting in a clean dataset of 41,679 households.

**Best Model:** Logistic Regression
- **AUC:** 0.7260
- **Accuracy:** 72.94%
- **Recall:** 68.25%

---

## Pipeline Stages

### Stage 1: Organize and Classify
- Read all .as files
- Identify survey type (LHZ, Admin2, Admin1)
- Identify format (individual, aggregate)
- Rename files: `country_year_month_place_level_format`
- Sort files into folders

### Stage 2: Convert to CSV & Extract Mortality
- Convert .as files to CSV
- Extract mortality sections (individual and aggregate formats)
- Handle two mortality structures:
  - **Individual**: P1_sex, P1_age, P1_died, etc.
  - **Aggregate**: COUNT_1 (HH_Size), COUNT_4 (Deaths), COUNT_5 (Births)

### Stage 3: Clean and Compute Household Information
- Convert person-level data to household-level (one row per household)
- Calculate: HH_Size, Males, Females, Avg_Age
- Calculate: Deaths, Deaths_u5, Deaths_5plus, Births
- Calculate Person-Time: `Person_Time = HH_Size × 3 months`

### Stage 4: Final Analysis Dataset
- Standardize all household files
- Merge 80 surveys into one dataset
- Final dataset: **41,679 households**

---

## Machine Learning

### Algorithms Used
| Model | Accuracy | Recall | F1-Score | AUC |
|-------|----------|--------|----------|-----|
| **Logistic Regression** | **0.7294** | **0.6825** | **0.0708** | **0.7260** |
| Decision Tree | 0.6388 | 0.6508 | 0.0517 | 0.6875 |
| Random Forest | 0.6606 | 0.6032 | 0.0510 | 0.7240 |
| XGBoost | 0.6742 | 0.5000 | 0.0443 | 0.6636 |

### Features Used
- **HH_Size** — Household size (30.9% importance)
- **Males** — Number of male members (17.4%)
- **MONTH_COS** — Seasonal pattern (14.6%)
- **Females** — Number of female members (14.6%)
- **MONTH_SIN** — Seasonal pattern (11.9%)
- **YEAR** — Survey year (10.5%)

### Target Variable
- **Deaths** (Binary: 0 = No Death, 1 = Death)

---

## Key Findings

1. **Death Rate:** 1.46% of households experienced deaths
2. **Best Model:** Logistic Regression (AUC = 0.7260)
3. **Most Important Predictor:** HH_Size (30.9%)
4. **Seasonal Patterns:** Month features combined = 26.5% importance
5. **Critical Metric:** Recall is most important for humanitarian applications

---

## Installation

```bash
# Clone the repository
git clone https://github.com/sumayahussein0987-cyber/SMART-Survey-Processing-Pipeline.git

# Navigate to the folder
cd SMART-Survey-Processing-Pipeline

# Install dependencies
pip install -r requirements.txt


Usage
bash
# Place raw .as files in the project folder

# Run pipeline stages in order
python 01_convert_as_to_csv.py
python 02_extract_mortality.py
python 03_convert_to_household.py
python 04_merge_datasets.py
python 05_machine_learning.py
## Outputs
File	Description
final_analysis_dataset_fixed.csv	Clean dataset (41,679 households)
confusion_matrices_fixed.png	Confusion matrix plots
roc_curves_fixed.png	ROC curves comparison
feature_importance_fixed.png	Feature importance plot
Folder Structure
text
📁 SMART-Survey-Processing-Pipeline/
├── 📄 README.md
├── 📄 .gitignore
├── 📄 requirements.txt
├── 📄 01_convert_as_to_csv.py
├── 📄 02_extract_mortality.py
├── 📄 03_convert_to_household.py
├── 📄 04_merge_datasets.py
├── 📄 05_machine_learning.py
├── 📄 apply_fixes.py
├── 📄 rename_files.py
├── 🖼️ confusion_matrices_fixed.png
├── 🖼️ roc_curves_fixed.png
└── 🖼️ feature_importance_fixed.png
Author
Sumaya Hussein

Date
July 2026

License
This project is for educational purposes.

