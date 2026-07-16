import pandas as pd
import os
from pathlib import Path

def split_dates_preserve_all(input_file, output_file):
    print(f"  Reading file...")
    
    df = pd.read_csv(input_file)
    
    # -----------------------------
    # FIND MORTALITY START
    # -----------------------------
    mortality_start_idx = None
    
    for idx, row in df.iterrows():
        for col in df.columns[:5]:
            val = str(row[col]) if pd.notna(row[col]) else ''
            if '¥Mortality_new' in val or '¥Mor_individual' in val:
                mortality_start_idx = idx
                break
        if mortality_start_idx is not None:
            break
    
    print(f"  Mortality section starts at row: {mortality_start_idx}")
    
    # -----------------------------
    # CREATE YEAR / MONTH
    # -----------------------------
    df['YEAR'] = pd.NA
    df['MONTH'] = pd.NA
    
    # -----------------------------
    # SPLIT SECTIONS
    # -----------------------------
    if mortality_start_idx is not None:
        anthro_rows = df.iloc[:mortality_start_idx].copy()
        mortality_rows = df.iloc[mortality_start_idx:].copy()
    else:
        anthro_rows = df.copy()
        mortality_rows = pd.DataFrame()
    
    # -----------------------------
    # PROCESS ANTHRO (SURVDATE)
    # -----------------------------
    if 'SURVDATE' in anthro_rows.columns:
        dates = pd.to_datetime(anthro_rows['SURVDATE'], errors='coerce')
        anthro_rows['YEAR'] = dates.dt.year
        anthro_rows['MONTH'] = dates.dt.month_name()
    
    # -----------------------------
    # PROCESS MORTALITY (DATE OR FIRST COLUMN)
    # -----------------------------
    if len(mortality_rows) > 0:
        # try DATE first, else first column
        date_col = 'DATE' if 'DATE' in mortality_rows.columns else mortality_rows.columns[0]
        
        dates = pd.to_datetime(mortality_rows[date_col], errors='coerce')
        mortality_rows['YEAR'] = dates.dt.year
        mortality_rows['MONTH'] = dates.dt.month_name()
    
    # -----------------------------
    # COMBINE BACK
    # -----------------------------
    df_final = pd.concat([anthro_rows, mortality_rows], ignore_index=True, sort=False)
    
    # -----------------------------
    # DROP ONLY DATE COLUMNS (SAFE)
    # -----------------------------
    cols_to_drop = [c for c in ['SURVDATE', 'DATE'] if c in df_final.columns]
    df_final.drop(columns=cols_to_drop, inplace=True)
    
    # -----------------------------
    # ENSURE Mor columns are preserved (safety)
    # -----------------------------
    protected_cols = ['Mor_new', 'Mor_individual']
    for col in protected_cols:
        if col not in df_final.columns:
            print(f"  ⚠️ Warning: {col} missing after processing!")
    
    # -----------------------------
    # REORDER COLUMNS SAFELY
    # -----------------------------
    cols = df_final.columns.tolist()
    
    # move YEAR / MONTH to front
    for c in ['YEAR', 'MONTH']:
        if c in cols:
            cols.remove(c)
    
    cols = ['YEAR', 'MONTH'] + cols
    df_final = df_final[cols]
    
    # -----------------------------
    # SAVE
    # -----------------------------
    df_final.to_csv(output_file, index=False)
    
    print(f"  Valid dates converted: {df_final['YEAR'].notna().sum()}")
    return True


# ==============================================
# PROCESS ALL FILES
# ==============================================

input_folder = r"C:\Users\abc\Downloads\dataset\raw_surveys"
output_folder = os.path.join(input_folder, "dates_split_last_last")
os.makedirs(output_folder, exist_ok=True)

csv_files = list(Path(input_folder).glob("*.csv"))

print(f"Found {len(csv_files)} files to process")
print("="*70)

success = 0

for csv_file in csv_files:
    print(f"\n📁 Processing: {csv_file.name}")
    
    output_file = os.path.join(output_folder, csv_file.name)
    
    try:
        split_dates_preserve_all(str(csv_file), output_file)
        print(f"  ✅ Success!")
        success += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

print("\n" + "="*70)
print(f"✅ Complete! {success}/{len(csv_files)} files processed")
print(f"📁 Output folder: {output_folder}")