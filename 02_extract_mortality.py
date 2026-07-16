"""
Stage 2: Extract Mortality Sections
- Extracts mortality data from CSV files
- Handles both individual and aggregate structures
- Preserves all markers and metadata
"""
import pandas as pd
from pathlib import Path

def extract_individual_mortality(input_file, output_file):
    """Extract individual mortality data (has P1_sex, P1_age columns)"""
    df = pd.read_csv(input_file)
    
    # Find mortality start
    mortality_start = None
    for idx in range(len(df)):
        for col in df.columns[:5]:
            val = str(df.iloc[idx][col]) if pd.notna(df.iloc[idx][col]) else ''
            if '¥Mortality_new' in val or '¥Mor_individual' in val:
                mortality_start = idx
                break
        if mortality_start:
            break
    
    if mortality_start is None:
        return False, "No mortality section found"
    
    # Find header row (first column contains 'Date')
    header_row = None
    for idx in range(mortality_start, min(len(df), mortality_start + 30)):
        first_val = str(df.iloc[idx][df.columns[0]]) if pd.notna(df.iloc[idx][df.columns[0]]) else ''
        if first_val == 'Date':
            header_row = idx
            break
    
    if header_row is None:
        return False, "No header row found"
    
    # Get headers
    new_headers = []
    for col in df.columns:
        val = df.iloc[header_row][col] if pd.notna(df.iloc[header_row][col]) else ''
        new_headers.append(str(val).strip())
    
    # Find end of mortality data (before metadata)
    end_row = len(df)
    metadata_keywords = ['¥Mor_individual_options', '¥Results', '¥Options', '¥Variables']
    for idx in range(header_row + 1, len(df)):
        first_val = str(df.iloc[idx][df.columns[0]]) if pd.notna(df.iloc[idx][df.columns[0]]) else ''
        if any(keyword in first_val for keyword in metadata_keywords):
            end_row = idx
            break
    
    # Extract data rows
    data_rows = []
    for idx in range(header_row + 1, end_row):
        row = []
        for col in df.columns:
            val = df.iloc[idx][col] if pd.notna(df.iloc[idx][col]) else ''
            row.append(str(val).strip())
        data_rows.append(row)
    
    mortality_df = pd.DataFrame(data_rows, columns=new_headers)
    mortality_df.to_csv(output_file, index=False)
    
    return True, f"Extracted {len(mortality_df)} rows"

def extract_aggregate_mortality(input_file, output_file):
    """Extract aggregate mortality data (has ¥Mortality_new marker)"""
    df = pd.read_csv(input_file)
    
    # Find mortality start
    mortality_start = None
    for idx in range(len(df)):
        for col in df.columns[:5]:
            val = str(df.iloc[idx][col]) if pd.notna(df.iloc[idx][col]) else ''
            if '¥Mortality_new' in val or 'Mortality_new' in val:
                mortality_start = idx
                break
        if mortality_start:
            break
    
    if mortality_start is None:
        return False, "No mortality section found"
    
    # Find end of mortality data (before next section)
    end_row = len(df)
    for idx in range(mortality_start + 1, len(df)):
        first_val = str(df.iloc[idx][df.columns[0]]) if pd.notna(df.iloc[idx][df.columns[0]]) else ''
        if '¥Mor_individual' in first_val or '¥Results' in first_val:
            end_row = idx
            break
    
    # Extract data rows
    data_rows = []
    for idx in range(mortality_start + 1, end_row):
        row = []
        for col in df.columns:
            val = df.iloc[idx][col] if pd.notna(df.iloc[idx][col]) else ''
            row.append(str(val).strip())
        data_rows.append(row)
    
    mortality_df = pd.DataFrame(data_rows)
    mortality_df.to_csv(output_file, index=False)
    
    return True, f"Extracted {len(mortality_df)} rows"

def process_mortality_file(input_file, output_file):
    """Auto-detect and extract mortality"""
    df = pd.read_csv(input_file)
    
    # Check if individual or aggregate
    is_individual = any('P1_sex' in col for col in df.columns[:20])
    is_aggregate = any('COUNT_' in col for col in df.columns[:10])
    
    if is_individual:
        return extract_individual_mortality(input_file, output_file)
    else:
        return extract_aggregate_mortality(input_file, output_file)

# ==============================================
# MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    # Find all CSV files (excluding already extracted ones)
    csv_files = [f for f in Path('.').glob('*.csv') if '_mortality' not in f.name]
    
    if not csv_files:
        print("❌ No CSV files found")
        exit()
    
    print(f"Found {len(csv_files)} CSV files")
    print("="*80)
    
    # Create output folder
    output_folder = Path('mortality_extracted')
    output_folder.mkdir(exist_ok=True)
    
    success = 0
    for f in csv_files:
        print(f"\n📄 {f.name}")
        output_file = output_folder / f"{f.stem}_mortality.csv"
        
        if output_file.exists():
            print(f"   ⏭️ Already exists")
            continue
        
        success_flag, message = process_mortality_file(str(f), str(output_file))
        if success_flag:
            print(f"   ✅ {message}")
            success += 1
        else:
            print(f"   ❌ {message}")
    
    print("\n" + "="*80)
    print(f"✅ Extracted mortality from {success}/{len(csv_files)} files")
    print(f"📁 Output: {output_folder}")