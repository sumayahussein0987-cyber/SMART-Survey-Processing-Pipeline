# SMART Survey Processing Pipeline & Mortality Prediction

## Project Overview

This project processes raw SMART survey data (.as files) from Somalia through a complete data pipeline and builds machine learning models to predict household mortality.

## Pipeline Stages

### Stage 1: Organize and Classify
- Read all .as files
- Identify survey type (LHZ, Admin2, Admin1)
- Identify format (individual, aggregate)
- Rename files with standardized format: `country_year_month_place_level_format`
- Sort files into folders

### Stage 2: Convert to CSV & Extract Mortality
- Convert .as files to CSV
- Extract mortality sections (individual and aggregate formats)
- Handle two mortality structures:
  - **Individual**: P1_sex, P1_age, P1_died, etc.
  - **Aggregate**: COUNT_1 (HH_Size), COUNT_4 (Deaths), COUNT_5 (Births)

### Stage 3: Clean and Compute Household Information
- Convert person-level data to household-level (one row per household)
- Calculate household counts (HH_Size, Males, Females)
- Calculate person-time (HH_Size × 3 months)
- Research and apply person-time methodology

### Stage 4: Final Analysis Dataset
- Standardize all household files
- Merge 80 surveys into one dataset
- Clean district names and dates
- Final dataset: 38,199 households

## Machine Learning

### Algorithms Used
- Logistic Regression (Best: AUC = 0.6766)
- Decision Tree
- Random Forest
- XGBoost

### Features
- HH_Size
- Males
- Females
- Person_Time
- YEAR
- MONTH

### Target
- Deaths (Binary: 0 = No Death, 1 = Death)

### Evaluation Metrics
- Accuracy
- Recall
- F1-Score
- AUC
- Confusion Matrix

## Results

### Best Model: Logistic Regression
- Accuracy: 69.98%
- Recall: 51.22%
- F1-Score: 0.0598
- AUC: 0.6766

### Most Important Features
| Feature | Importance |
|---------|------------|
| MONTH | 30.5% |
| HH_Size | 17.8% |
| Person_Time | 16.2% |
| YEAR | 12.7% |
| Males | 11.5% |
| Females | 10.3% |

## Folder Structure
