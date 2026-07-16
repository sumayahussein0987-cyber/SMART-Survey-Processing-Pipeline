"""
Rename Files: Standardize file names to country_year_month_place_level_format
"""
import os
import re
from pathlib import Path

def rename_files_in_folder(folder_path):
    """Rename files in a folder to standardized format"""
    files = list(Path(folder_path).glob('*.csv'))
    files.extend(Path(folder_path).glob('*.CSV'))
    
    if not files:
        print(f"No files found in {folder_path}")
        return
    
    print(f"Found {len(files)} files in {folder_path}")
    
    for f in files:
        old_name = f.stem
        old_name_lower = old_name.lower()
        
        # Extract country
        country = "SOM"
        
        # Extract year and month
        year = None
        month = "00"
        
        # Pattern: YYYYMM
        yyyymm_match = re.search(r'(20\d{2})(\d{2})', old_name)
        if yyyymm_match:
            year = yyyymm_match.group(1)
            month = yyyymm_match.group(2)
        else:
            # Pattern: YYYY_MM
            year_month_match = re.search(r'(20\d{2})_(\d{2})', old_name)
            if year_month_match:
                year = year_month_match.group(1)
                month = year_month_match.group(2)
            else:
                # Pattern: YYYY
                year_match = re.search(r'(20\d{2})', old_name)
                if year_match:
                    year = year_match.group(1)
        
        # Extract place
        place = old_name_lower
        place = re.sub(r'som[_\s]*', '', place)
        place = re.sub(r'20\d{2}[_\s]*', '', place)
        place = re.sub(r'\d{2}[_\s]*', '', place)
        place = re.sub(r'lhz[_\s]*', '', place)
        place = re.sub(r'admin[0-9][_\s]*', '', place)
        place = re.sub(r'[_\s]+', '_', place)
        place = place.strip('_')
        
        # Capitalize
        place = place.title()
        
        # Determine level
        level = 'unknown'
        if 'lhZ' in old_name or 'lhz' in old_name_lower:
            level = 'lhz'
        elif 'admin2' in old_name_lower:
            level = 'admin2'
        elif 'admin1' in old_name_lower:
            level = 'admin1'
        
        # Determine format
        fmt = 'individual'
        if 'aggregate' in old_name_lower:
            fmt = 'aggregate'
        
        # Create new name
        if year:
            new_name = f"{country}_{year}_{month}_{place}_{level}_{fmt}.csv"
        else:
            new_name = f"{country}_unknown_{place}_{level}_{fmt}.csv"
        
        new_name = re.sub(r'_+', '_', new_name)
        
        old_path = f
        new_path = f.parent / new_name
        
        try:
            old_path.rename(new_path)
            print(f"   ✅ {old_name} → {new_name}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")

# ==============================================
# MAIN EXECUTION
# ==============================================

if __name__ == "__main__":
    # Process each folder
    folders = [
        'lhz_surveys/individual',
        'admin2_surveys/individual',
        'admin2_surveys/aggregate',
        'issue_surveys'
    ]
    
    for folder in folders:
        if Path(folder).exists():
            print("\n" + "="*80)
            print(f"📁 Processing: {folder}")
            print("="*80)
            rename_files_in_folder(folder)