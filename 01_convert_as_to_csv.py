"""
Stage 1: Convert .as files to CSV
- Reads raw .as files with encoding detection
- Finds the correct header row containing SURVDATE
- Extracts data rows and saves as CSV
"""
import os
import pandas as pd
from pathlib import Path
import chardet

def detect_encoding(file_path):
    """Detect file encoding"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding'] or 'latin1'

def convert_as_to_csv(input_file, output_file):
    """Convert .as file to CSV"""
    print(f"  Processing: {Path(input_file).name}")
    
    # Detect encoding
    encoding = detect_encoding(input_file)
    
    # Read file
    with open(input_file, 'r', encoding=encoding, errors='ignore') as f:
        lines = f.readlines()
    
    # Find header row
    header_row_index = None
    for i, line in enumerate(lines):
        if 'SURVDATE' in line and 'CLUSTER' in line and 'TEAM' in line:
            header_row_index = i
            break
    
    if header_row_index is None:
        print(f"    ⚠️ Could not find header in {Path(input_file).name}")
        return False
    
    # Get headers
    headers = [h.strip() for h in lines[header_row_index].strip().split('\t') if h.strip()]
    
    # Extract data rows
    data_rows = []
    for line in lines[header_row_index + 1:]:
        line = line.strip()
        if line:
            row = line.split('\t')
            data_rows.append(row)
    
    if not data_rows:
        print(f"    ⚠️ No data found in {Path(input_file).name}")
        return False
    
    # Create DataFrame
    max_cols = max(len(row) for row in data_rows)
    for row in data_rows:
        while len(row) < max_cols:
            row.append('')
    
    df = pd.DataFrame(data_rows, columns=headers[:max_cols])
    df.to_csv(output_file, index=False)
    
    print(f"    ✅ Converted: {len(df)} rows")
    return True

# ==============================================
# MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    # Find all .as files
    as_files = list(Path('.').glob('*.as'))
    as_files.extend(Path('.').glob('*.AS'))
    
    if not as_files:
        print("❌ No .as files found in current directory")
        exit()
    
    print(f"Found {len(as_files)} .as files")
    print("="*80)
    
    success = 0
    for f in as_files:
        output = f.with_suffix('.csv')
        if convert_as_to_csv(str(f), str(output)):
            success += 1
    
    print("\n" + "="*80)
    print(f"✅ Converted {success}/{len(as_files)} files to CSV")