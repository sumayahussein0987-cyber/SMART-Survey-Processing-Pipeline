import pandas as pd

# Load your dataset
df = pd.read_csv('final_analysis_dataset.csv')

# Check before removal
print(f"Before: {len(df)} rows")

# Remove exact duplicates
df = df.drop_duplicates()

print(f"After: {len(df)} rows")
print(f"Removed: {7} duplicate rows")

# Save
df.to_csv('final_analysis_dataset_clean.csv', index=False)