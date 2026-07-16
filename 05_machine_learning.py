"""
Machine Learning on Fixed Dataset with Proper Features
- Uses final_analysis_dataset_fixed.csv
- Features: HH_Size, Males, Females, YEAR, MONTH_SIN, MONTH_COS
- Removed Person_Time (redundant)
- Added cyclical month encoding
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, roc_curve
)
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MACHINE LEARNING ON FIXED DATASET")
print("="*80)

# Load the fixed dataset
df = pd.read_csv('final_analysis_dataset_fixed.csv')
print(f"\nTotal households: {len(df)}")
print(f"Death rate: {df['Deaths'].mean()*100:.2f}%")

# ==============================================
# PREPARE FEATURES
# ==============================================

print("\n" + "="*80)
print("PREPARING FEATURES")
print("="*80)

# Features: removed Person_Time, added cyclical month
features = ['HH_Size', 'Males', 'Females', 'YEAR', 'MONTH_SIN', 'MONTH_COS']

# Only keep features that exist
available_features = [f for f in features if f in df.columns]

print(f"Features used: {available_features}")

X = df[available_features].copy()
y = df['Deaths'].copy()

# Convert Deaths to binary (0 or 1)
y = y.apply(lambda x: 1 if x > 0 else 0)

# Fill missing values
X = X.fillna(X.mean())

print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
print(f"Death rate: {y.mean()*100:.2f}%")

# ==============================================
# TRAIN-TEST SPLIT
# ==============================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nTraining set: {len(X_train)} households")
print(f"Test set: {len(X_test)} households")
print(f"Training deaths: {y_train.sum()} ({y_train.mean()*100:.2f}%)")
print(f"Test deaths: {y_test.sum()} ({y_test.mean()*100:.2f}%)")

# ==============================================
# TRAIN MODELS
# ==============================================

print("\n" + "="*80)
print("TRAINING MODELS")
print("="*80)

class_weight_ratio = (len(y) - y.sum()) / y.sum()
print(f"Class weight ratio: {class_weight_ratio:.2f}")

models = {
    'Logistic Regression': LogisticRegression(
        class_weight='balanced', random_state=42, max_iter=1000
    ),
    'Decision Tree': DecisionTreeClassifier(
        class_weight='balanced', max_depth=10, random_state=42
    ),
    'Random Forest': RandomForestClassifier(
        class_weight='balanced', n_estimators=100, max_depth=10, random_state=42
    ),
    'XGBoost': XGBClassifier(
        scale_pos_weight=class_weight_ratio, n_estimators=100, 
        max_depth=6, random_state=42, eval_metric='logloss'
    )
}

results = {}

for name, model in models.items():
    print(f"\n📊 Training: {name}")
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    results[name] = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1-Score': f1_score(y_test, y_pred),
        'AUC': roc_auc_score(y_test, y_proba),
        'Confusion Matrix': confusion_matrix(y_test, y_pred)
    }
    
    print(f"   ✅ Accuracy: {results[name]['Accuracy']:.4f}")
    print(f"   ✅ Recall: {results[name]['Recall']:.4f}")
    print(f"   ✅ F1-Score: {results[name]['F1-Score']:.4f}")
    print(f"   ✅ AUC: {results[name]['AUC']:.4f}")
    print(f"   Confusion Matrix:\n{results[name]['Confusion Matrix']}")

# ==============================================
# COMPARISON TABLE
# ==============================================

print("\n" + "="*80)
print("MODEL COMPARISON TABLE")
print("="*80)

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': [r['Accuracy'] for r in results.values()],
    'Recall': [r['Recall'] for r in results.values()],
    'F1-Score': [r['F1-Score'] for r in results.values()],
    'AUC': [r['AUC'] for r in results.values()]
})

print(comparison_df.to_string(index=False))

best = comparison_df.loc[comparison_df['AUC'].idxmax()]
print(f"\n🏆 Best Model: {best['Model']} (AUC = {best['AUC']:.4f})")

# ==============================================
# FEATURE IMPORTANCE
# ==============================================

print("\n" + "="*80)
print("FEATURE IMPORTANCE")
print("="*80)

rf_model = models['Random Forest']
importance = pd.DataFrame({
    'Feature': available_features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

for _, row in importance.iterrows():
    print(f"   {row['Feature']}: {row['Importance']*100:.1f}%")

# ==============================================
# CONFUSION MATRICES PLOT
# ==============================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for idx, (name, result) in enumerate(results.items()):
    row, col = idx // 2, idx % 2
    ax = axes[row, col]
    cm = result['Confusion Matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Death', 'Death'],
                yticklabels=['No Death', 'Death'])
    ax.set_title(f'{name}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')

plt.tight_layout()
plt.savefig('confusion_matrices_fixed.png', dpi=300)
plt.show()
print("✅ Confusion matrices saved as: confusion_matrices_fixed.png")

# ==============================================
# ROC CURVES
# ==============================================

plt.figure(figsize=(10, 8))
for name, model in models.items():
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    plt.plot(fpr, tpr, label=f'{name} (AUC = {auc:.3f})')

plt.plot([0, 1], [0, 1], 'k--', label='Random (AUC = 0.5)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves - Fixed Dataset')
plt.legend(loc='lower right')
plt.grid(True)
plt.savefig('roc_curves_fixed.png', dpi=300)
plt.show()
print("✅ ROC curves saved as: roc_curves_fixed.png")

# ==============================================
# FINAL SUMMARY
# ==============================================

print("\n" + "="*80)
print("FINAL SUMMARY - FIXED DATASET")
print("="*80)

print(f"\n📊 Dataset: {len(df)} households")
print(f"📊 Death rate: {df['Deaths'].mean()*100:.2f}%")
print(f"📊 Features used: {len(available_features)} (removed Person_Time, added cyclical month)")

print("\n📊 Model Performance Summary:")
print(comparison_df.to_string(index=False))

print(f"\n🏆 Best Model: {best['Model']}")
print(f"   - Accuracy: {best['Accuracy']:.4f}")
print(f"   - Recall: {best['Recall']:.4f}")
print(f"   - F1-Score: {best['F1-Score']:.4f}")
print(f"   - AUC: {best['AUC']:.4f}")

print("\n📊 Most Important Features:")
for _, row in importance.head(5).iterrows():
    print(f"   {row['Feature']}: {row['Importance']*100:.1f}%")

print("\n" + "="*80)
print("✅ MACHINE LEARNING COMPLETE!")