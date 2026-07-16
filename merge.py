import pandas as pd
from pathlib import Path

# Load the final dataset
final_file = Path(r"C:\Users\abc\Downloads\dataset\final_merged\final_analysis_dataset.csv")
df = pd.read_csv(final_file)

print("="*80)
print("FINAL DATASET PREVIEW")
print("="*80)

print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print(f"\n📊 First 5 rows:")
print(df.head(5).to_string())

print(f"\n📊 Column names (first 20):")
print(df.columns[:20].tolist())

print(f"\n📊 Summary statistics:")
print(df[['HH_Size', 'Males', 'Females', 'Deaths', 'Births', 'Person_Time']].describe())