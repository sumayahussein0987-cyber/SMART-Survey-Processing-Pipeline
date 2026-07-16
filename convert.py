from pathlib import Path
import shutil

mortality_folder = Path(r"C:\Users\abc\Downloads\dataset\mortality_extracted")
household_folder = Path(r"C:\Users\abc\Downloads\dataset\household_level")

# List of aggregate files that need to be copied
aggregate_files = [
    "SOM_2013_00_Bakool_Pastoral_lhz_individual_mortality_aggregate.csv",
    "SOM_2013_01_BeletWeyne_2_admin2_aggregate_mortality.csv",
    "SOM_2013_02_BeletWeyne_admin2_aggregate_mortality.csv",
    "SOM_2013_11_Baydhaba_admin2_aggregate_mortality.csv",
    "SOM_2013_12_Mogadishu_IDP_admin2_aggregate_mortality.csv",
    "SOM_2014_05_Burco_IDP_admin2_aggregate_mortality.csv",
    "SOM_2014_06_Hargeysa_IDP_admin2_aggregate_mortality.csv",
]

print("="*80)
print("COPYING MISSING AGGREGATE FILES TO HOUSEHOLD LEVEL")
print("="*80)

copied = 0
for fname in aggregate_files:
    src = mortality_folder / fname
    if src.exists():
        # Create new name (replace _mortality_aggregate with _household)
        new_name = fname.replace('_mortality_aggregate', '_household')
        dst = household_folder / new_name
        shutil.copy2(src, dst)
        print(f"   ✅ {fname} → {new_name}")
        copied += 1
    else:
        print(f"   ⚠️ {fname} - not found")

print("\n" + "="*80)
print(f"✅ Copied {copied} files to household_level folder")

# Final count
final_files = list(household_folder.glob("*.csv"))
print(f"\n📁 Total files in household_level folder: {len(final_files)}")