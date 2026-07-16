"""
Stage 3: Convert to Household-Level Data
- Converts person-level mortality data to household-level
- Calculates HH_Size, Males, Females, Deaths, Births
- Calculates Person-Time (HH_Size × 3 months)
"""
import pandas as pd
import numpy as np
from pathlib import Path

def convert_individual_to_household(input_file, output_file):
    """Convert individual mortality to household-level"""
    df = pd.read_csv(input_file)
    
    # Identify members (P1 to P20)
    member_cols = []
    for i in range(1, 21):
        if f'P{i}_sex' in df.columns:
            member_cols.append(i)
    
    if not member_cols:
        return False, "No member columns found"
    
    household_data = []
    
    for idx, row in df.iterrows():
        cluster = row.get('Cluster', '')
        team = row.get('Team', '')
        hh = row.get('HH', '')
        
        total_members = 0
        deaths = 0
        births = 0
        males = 0
        females = 0
        ages = []
        deaths_u5 = 0
        deaths_5plus = 0
        
        for p_num in member_cols:
            sex = row.get(f'P{p_num}_sex', '')
            age = row.get(f'P{p_num}_age', '')
            
            if pd.isna(sex) and (pd.isna(age) or age == ''):
                continue
            
            total_members += 1
            
            if str(sex).lower() == 'm':
                males += 1
            elif str(sex).lower() == 'f':
                females += 1
            
            if not pd.isna(age) and age != '':
                try:
                    ages.append(float(age))
                except:
                    pass
            
            # Count deaths
            died_val = row.get(f'P{p_num}_died', '')
            if not pd.isna(died_val) and str(died_val).lower() in ['1', 'y', 'yes']:
                deaths += 1
                if not pd.isna(age) and age != '':
                    try:
                        if float(age) < 5:
                            deaths_u5 += 1
                        else:
                            deaths_5plus += 1
                    except:
                        pass
            
            # Count births
            born_val = row.get(f'P{p_num}_born', '')
            if not pd.isna(born_val) and str(born_val).lower() in ['1', 'y', 'yes']:
                births += 1
        
        avg_age = np.mean(ages) if ages else 0
        
        household = {
            'CLUSTER': cluster,
            'Team': team,
            'HH': hh,
            'HH_Size': total_members,
            'Males': males,
            'Females': females,
            'Avg_Age': avg_age,
            'Deaths': deaths,
            'Deaths_u5': deaths_u5,
            'Deaths_5plus': deaths_5plus,
            'Births': births,
            'Person_Time': total_members * 3
        }
        household_data.append(household)
    
    household_df = pd.DataFrame(household_data)
    household_df.to_csv(output_file, index=False)
    
    return True, f"Converted {len(household_df)} households"

def convert_aggregate_to_household(input_file, output_file):
    """Convert aggregate person-level to household-level"""
    df = pd.read_csv(input_file)
    
    # Group by household
    household_groups = df.groupby(['CLUSTER', 'TEAM', 'HH'])
    
    household_data = []
    for (cluster, team, hh), group in household_groups:
        hh_size = len(group)
        males = group[group['COUNT_3'] == 1].shape[0]
        females = group[group['COUNT_3'] == 0].shape[0]
        deaths = group[group['COUNT_4'] == 1].shape[0]
        births = group[group['COUNT_5'] == 1].shape[0]
        
        household_data.append({
            'CLUSTER': cluster,
            'Team': team,
            'HH': hh,
            'HH_Size': hh_size,
            'Males': males,
            'Females': females,
            'Avg_Age': 0,
            'Deaths': deaths,
            'Deaths_u5': 0,
            'Deaths_5plus': 0,
            'Births': births,
            'Person_Time': hh_size * 3
        })
    
    household_df = pd.DataFrame(household_data)
    household_df.to_csv(output_file, index=False)
    
    return True, f"Converted {len(household_df)} households"

# ==============================================
# MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    mortality_folder = Path('mortality_extracted')
    output_folder = Path('household_level')
    output_folder.mkdir(exist_ok=True)
    
    files = list(mortality_folder.glob('*.csv'))
    
    print(f"Found {len(files)} mortality files")
    print("="*80)
    
    success = 0
    for f in files:
        output_file = output_folder / f.name.replace('_mortality', '_household')
        
        # Check if aggregate
        df_sample = pd.read_csv(f)
        is_aggregate = 'COUNT_1' in df_sample.columns
        
        if is_aggregate:
            success_flag, message = convert_aggregate_to_household(str(f), str(output_file))
        else:
            success_flag, message = convert_individual_to_household(str(f), str(output_file))
        
        if success_flag:
            print(f"   ✅ {f.name} → {message}")
            success += 1
        else:
            print(f"   ❌ {f.name} → {message}")
    
    print("\n" + "="*80)
    print(f"✅ Converted {success}/{len(files)} files")
    print(f"📁 Output: {output_folder}")