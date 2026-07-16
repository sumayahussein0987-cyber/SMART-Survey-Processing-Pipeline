import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('final_analysis_dataset_fixed.csv')

print("="*80)
print("VERIFYING CYCLICAL ENCODING")
print("="*80)

# Check if new columns exist
print(f"\n📊 Columns in dataset:")
print(df.columns.tolist())

# Check if MONTH_SIN and MONTH_COs exist
if 'MONTH_SIN' in df.columns and 'MONTH_COS' in df.columns:
    print("\n✅ MONTH_SIN and MONTH_COS columns found!")
    
    # Show the values
    print("\n📊 Month values and their encodings:")
    month_data = df[['MONTH', 'MONTH_SIN', 'MONTH_COS']].drop_duplicates().sort_values('MONTH')
    print(month_data.to_string(index=False))
    
    # Verify the math
    print("\n📊 Verification (should be close to 1):")
    print(f"   sin² + cos² = {(df['MONTH_SIN']**2 + df['MONTH_COS']**2).mean():.4f} (should be ~1.0)")
    
else:
    print("\n❌ MONTH_SIN and/or MONTH_COS columns not found!")
    print("   Running the encoding again...")
    
    # Add cyclical encoding
    df['MONTH_SIN'] = np.sin(2 * np.pi * df['MONTH'] / 12)
    df['MONTH_COS'] = np.cos(2 * np.pi * df['MONTH'] / 12)
    
    # Save
    df.to_csv('final_analysis_dataset_fixed.csv', index=False)
    print("✅ Added MONTH_SIN and MONTH_COS columns")