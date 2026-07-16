import pandas as pd
import os
from pathlib import Path

def clean_file(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Month names
    months = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
              7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    # Split SURVDATE if it exists
    if 'SURVDATE' in df.columns:
        dates = pd.to_datetime(df['SURVDATE'], errors='coerce')
        df['YEAR'] = dates.dt.year
        df['MONTH'] = dates.dt.month.map(months)
        df = df.drop('SURVDATE', axis=1)
        print(f"    Converted SURVDATE")
    
    # Find and remove Date column in mortality section
    # Look for a row where first column contains 'Date'
    date_col_idx = None
    for i in range(len(df)):
        first_val = str(df.iloc[i,0]) if pd.notna(df.iloc[i,0]) else ''
        if first_val == 'Date':
            date_col_idx = 0
            break
    
    if date_col_idx is not None:
        # Extract dates from that column for rows below the header
        for i in range(date_col_idx + 1, len(df)):
            val = df.iloc[i, date_col_idx]
            if pd.notna(val) and '/' in str(val):
                try:
                    dt = pd.to_datetime(val, errors='coerce')
                    if pd.notna(dt):
                        df.loc[i, 'YEAR'] = dt.year
                        df.loc[i, 'MONTH'] = months.get(dt.month, '')
                except:
                    pass
        
        # Drop the Date column
        df = df.drop(df.columns[date_col_idx], axis=1)
        print(f"    Removed Date column")
    
    # Reorder columns
    cols = ['YEAR', 'MONTH'] + [c for c in df.columns if c not in ['YEAR', 'MONTH']]
    df = df[cols]
    
    df.to_csv(output_file, index=False)
    return True

# Process all files
input_folder = r"C:\Users\abc\Downloads\dataset\raw_surveys"
output_folder = r"C:\Users\abc\Downloads\dataset\raw_surveys\my_last_braincell"
os.makedirs(output_folder, exist_ok=True)

csv_files = list(Path(input_folder).glob("*.csv"))
print(f"Found {len(csv_files)} files\n")

for f in csv_files:
    print(f"📁 {f.name}")
    out = os.path.join(output_folder, f.name)
    try:
        clean_file(str(f), out)
        print(f"   ✅ OK\n")
    except Exception as e:
        print(f"   ❌ {e}\n")

print(f"Output: {output_folder}")