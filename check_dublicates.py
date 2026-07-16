"""
Check if duplicate removal in Stage 4 was done correctly
Run this on your final dataset
"""
import pandas as pd
from pathlib import Path

print("="*80)
print("CHECKING DUPLICATE REMOVAL IN FINAL DATASET")
print("="*80)

# Load the final dataset
df = pd.read_csv('final_analysis_dataset.csv')
print(f"\n📊 Total households: {len(df)}")
print(f"📊 Death rate: {df['Deaths'].mean()*100:.2f}%")

# ==============================================
# Check 1: Duplicates on ALL columns
# ==============================================

print("\n" + "="*80)
print("CHECK 1: Full row duplicates (all columns)")
print("="*80)

full_duplicates = df.duplicated().sum()
print(f"Duplicate rows (full row): {full_duplicates}")

if full_duplicates > 0:
    print(f"⚠️ Found {full_duplicates} exact duplicate rows")
    # Check if any death cases are in duplicates
    death_duplicates = df[df.duplicated(keep=False) & (df['Deaths'] == 1)].shape[0]
    print(f"Death cases in duplicates: {death_duplicates}")
    if death_duplicates > 0:
        print("⚠️ Some death cases are in duplicate rows!")
    else:
        print("✅ No death cases lost in duplicates")
else:
    print("✅ No exact duplicate rows found")

# ==============================================
# Check 2: Duplicates on features only (modeling columns)
# ==============================================

print("\n" + "="*80)
print("CHECK 2: Duplicates on feature columns only")
print("="*80)

feature_cols = ['HH_Size', 'Males', 'Females', 'Person_Time', 'YEAR', 'MONTH']
available_features = [col for col in feature_cols if col in df.columns]

feature_duplicates = df.duplicated(subset=available_features).sum()
print(f"Duplicate rows (features only): {feature_duplicates}")

if feature_duplicates > 0:
    # Check if duplicates have different Death values
    dup_mask = df.duplicated(subset=available_features, keep=False)
    dup_df = df[dup_mask]
    
    # Group by feature values and check Death values
    grouped = dup_df.groupby(available_features)['Deaths'].agg(['nunique', 'sum'])
    conflicting = grouped[grouped['nunique'] > 1]
    
    if len(conflicting) > 0:
        print(f"⚠️ Found {len(conflicting)} groups of duplicates with conflicting Death values!")
        print("   This means identical feature values but different outcomes")
        print("   These would need to be handled carefully")
    else:
        print("✅ All duplicates have consistent Death values")
        
        # Show summary
        print(f"\n📊 Duplicate groups summary:")
        print(dup_df.groupby(available_features).size().value_counts().sort_index())
else:
    print("✅ No duplicate rows on features")

# ==============================================
# Check 3: Potential data leakage from duplicates
# ==============================================

print("\n" + "="*80)
print("CHECK 3: Potential issues from duplicates")
print("="*80)

# Check if any survey has too many duplicates
if 'Source_File' in df.columns:
    print("\nDuplicate distribution by survey:")
    dup_by_survey = df.duplicated(keep=False).groupby(df['Source_File']).sum()
    if dup_by_survey.sum() > 0:
        print(dup_by_survey[dup_by_survey > 0].sort_values(ascending=False).head(10))
    else:
        print("   No duplicates found across surveys")

# ==============================================
# Summary
# ==============================================

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

if full_duplicates == 0 and feature_duplicates == 0:
    print("✅ No duplicates found. Your deduplication is clean!")
elif full_duplicates > 0:
    print(f"⚠️ Found {full_duplicates} exact duplicate rows.")
    print("   You can safely remove them with: df.drop_duplicates(inplace=True)")
elif feature_duplicates > 0 and conflicting == 0:
    print("✅ Duplicates found on features but they have consistent Death values.")
    print("   You can either keep them or remove them.")
elif feature_duplicates > 0 and conflicting > 0:
    print("❌ Critical issue: Duplicates with conflicting Death values found!")
    print("   These need manual review before deduplication.")