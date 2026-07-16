import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('final_analysis_dataset_fixed.csv')

# Prepare features
features = ['HH_Size', 'Males', 'Females', 'YEAR', 'MONTH_SIN', 'MONTH_COS']
X = df[features].fillna(df[features].mean())
y = df['Deaths'].apply(lambda x: 1 if x > 0 else 0)

# Train Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(class_weight='balanced', n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# ==============================================
# PLOT FEATURE IMPORTANCE
# ==============================================

importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=True)

plt.figure(figsize=(10, 6))
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(importance)))
plt.barh(importance['Feature'], importance['Importance'], color=colors)
plt.xlabel('Importance')
plt.title('Feature Importance - Random Forest')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('feature_importance_fixed.png', dpi=300, bbox_inches='tight')
plt.show()

print("="*80)
print("FEATURE IMPORTANCE")
print("="*80)
for _, row in importance.sort_values('Importance', ascending=False).iterrows():
    print(f"   {row['Feature']}: {row['Importance']*100:.1f}%")

print("\n✅ Feature importance saved as: feature_importance_fixed.png")

# ==============================================
# VERIFY ALL FILES
# ==============================================

from pathlib import Path
files = ['confusion_matrices_fixed.png', 'roc_curves_fixed.png', 'feature_importance_fixed.png']

print("\n" + "="*80)
print("📁 ALL PNG FILES IN YOUR FOLDER")
print("="*80)

for f in files:
    if Path(f).exists():
        size = Path(f).stat().st_size / 1024
        print(f"   ✅ {f} ({size:.1f} KB)")
    else:
        print(f"   ❌ {f} - NOT FOUND")