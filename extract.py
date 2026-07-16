import pandas as pd
from pathlib import Path

def rename_columns(input_file):
    """Rename first three columns to Date, YEAR, MONTH"""
    df = pd.read_csv(input_file)
    
    # Check if already renamed
    if df.columns[0] == 'Date' and df.columns[1] == 'YEAR' and df.columns[2] == 'MONTH':
        return False  # Already renamed
    
    # Rename first three columns
    new_columns = list(df.columns)
    new_columns[0] = 'Date'
    new_columns[1] = 'YEAR'
    new_columns[2] = 'MONTH'
    df.columns = new_columns
    
    # Save (overwrite)
    df.to_csv(input_file, index=False)
    return True

# ==============================================
# Process all mortality files
# ==============================================

mortality_folder = Path(r"C:\Users\abc\Downloads\dataset\mortality_extracted")

# Get all CSV files (exclude the test file)
files = [f for f in mortality_folder.glob("*.csv") if f.name != "test_renamed.csv"]

print(f"Found {len(files)} files to process")
print("="*80)

renamed_count = 0
skipped_count = 0

for f in files:
    try:
        if rename_columns(f):
            print(f"   ✅ {f.name}")
            renamed_count += 1
        else:
            print(f"   ⏭️ {f.name} - already has correct column names")
            skipped_count += 1
    except Exception as e:
        print(f"   ❌ Error processing {f.name}: {e}")

print("\n" + "="*80)
print(f"✅ Renamed: {renamed_count} files")
print(f"⏭️ Already correct: {skipped_count} files")
print(f"\n📁 All files in: {mortality_folder}")

# Delete the test file
test_file = mortality_folder / "test_renamed.csv"
if test_file.exists():
    test_file.unlink()
    print(f"\n🗑️ Removed test file: test_renamed.csv")