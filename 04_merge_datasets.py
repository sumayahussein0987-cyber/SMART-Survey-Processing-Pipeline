"""
Stage 4: Final Analysis Dataset
- Standardizes all household files
- Merges all surveys into one dataset
- Cleans and prepares final dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path

def standardize_household_file(file_path):
    """Standardize household file to consistent format"""
    df = pd.read_csv(file_path)
    
    # Check if aggregate (has COUNT columns)
    if 'COUNT_1' in df.columns:
        # Convert aggregate to household
        household_groups = df.groupby(['CLUSTER', 'TEAM', 'HH'])
        household_data = []
        for (cluster, team, hh), group in household_groups:
            household_data.append({
                'CLUSTER': cluster,
                'Team': team,
                'HH': hh,
                'HH_Size': len(group),
                'Males': group[group['COUNT_3'] == 1].shape[0],
                'Females': group[group['COUNT_3'] == 0].shape[0],
                'Avg_Age': 0,
                'Deaths': group[group['COUNT_4'] == 1].shape[0],
                'Deaths_u5': 0,
                'Deaths_5plus': 0,
                'Births': group[group['COUNT_5'] == 1].shape[0],
                'Person_Time': len(group) * 3,
                'Source_Type': 'aggregate'
            })
        df = pd.DataFrame(household_data)
    else:
        df['Source_Type'] = 'individual'
    
    # Add source file
    df['Source_File'] = file_path.stem
    
    # Keep standard columns
    standard_cols = [
        'CLUSTER', 'Team', 'HH', 'HH_Size', 'Males', 'Females',
        'Avg_Age', 'Deaths', 'Deaths_u5', 'Deaths_5plus',
        'Births', 'Person_Time', 'Source_Type', 'Source_File'
    ]
    
    existing_cols = [col for col in standard_cols if col in df.columns]
    return df[existing_cols]

# ==============================================
# MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    household_folder = Path('household_level')
    output_file = Path('final_analysis_dataset.csv')
    
    files = list(household_folder.glob('*.csv'))
    
    print(f"Found {len(files)} household files")
    print("="*80)
    
    all_dfs = []
    for f in files:
        df = standardize_household_file(f)
        all_dfs.append(df)
        print(f"   ✅ {f.name}: {len(df)} households")
    
    # Merge all
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    # Clean: Remove rows with missing target
    final_df = final_df.dropna(subset=['Deaths'])
    
    # Convert Deaths to binary (0 or 1)
    final_df['Deaths'] = final_df['Deaths'].apply(lambda x: 1 if x > 0 else 0)
    
    # Save
    final_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print(f"✅ FINAL DATASET CREATED!")
    print(f"   Total households: {len(final_df)}")
    print(f"   Total columns: {len(final_df.columns)}")
    print(f"   Death rate: {final_df['Deaths'].mean()*100:.2f}%")
    print(f"   📁 {output_file}")