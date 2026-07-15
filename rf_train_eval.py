# Random Forest classifier training and evaluation.

import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    matthews_corrcoef,
    roc_auc_score,
    cohen_kappa_score,
)

# Config
TRAIN_CSV = "train_reduced.csv"
TEST_CSV = "test_reduced.csv"
TARGET_COLUMN = "label"
RANDOM_STATE = 8
MODEL_NAME = "RandomForest"

# Load the already-split, already-feature-filtered data
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

X_train_reduced = train_df.drop(columns=[TARGET_COLUMN])
y_train = train_df[TARGET_COLUMN]
X_test_reduced = test_df.drop(columns=[TARGET_COLUMN])
y_test = test_df[TARGET_COLUMN]

print(f"Train shape: {X_train_reduced.shape}, Test shape: {X_test_reduced.shape}")

# Train Random Forest
default_params = {
    "n_estimators": 300,
    "max_depth": 20,
    "min_samples_split": 10,
    "min_samples_leaf": 2,
    "max_features": "sqrt",
}

rf_params = default_params.copy()
try:
    with open("best_rf_params.json") as f:
        tuned_params = json.load(f)
    rf_params.update(tuned_params)
    print(f"\nLoaded tuned hyperparameters from 'best_rf_params.json': {tuned_params}")
except FileNotFoundError:
    print("\nNo 'best_rf_params.json' found — using default hyperparameters. "
          "Run rf_hyperparameter_tuning.py first to tune them.")

rf = RandomForestClassifier(
    random_state=RANDOM_STATE,
    n_jobs=-1,
    **rf_params,
)

train_start = time.perf_counter()
rf.fit(X_train_reduced, y_train)
train_time = time.perf_counter() - train_start
print(f"\nTraining time: {train_time:.4f} seconds")

inference_start = time.perf_counter()
y_pred = rf.predict(X_test_reduced)
inference_time = time.perf_counter() - inference_start
inference_time_per_sample_ms = (inference_time / len(X_test_reduced)) * 1000
print(f"Inference time (full test set, {len(X_test_reduced)} samples): {inference_time:.4f} seconds")
print(f"Inference time (per sample): {inference_time_per_sample_ms:.4f} ms")

y_proba = rf.predict_proba(X_test_reduced)

classes = rf.classes_

# Performance metrics
accuracy = accuracy_score(y_test, y_pred)
balanced_acc = balanced_accuracy_score(y_test, y_pred)
mcc = matthews_corrcoef(y_test, y_pred)
kappa = cohen_kappa_score(y_test, y_pred)

precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
    y_test, y_pred, average="macro", zero_division=0
)
precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
    y_test, y_pred, average="weighted", zero_division=0
)

y_test_bin = label_binarize(y_test, classes=classes)
try:
    roc_auc_macro = roc_auc_score(y_test_bin, y_proba, average="macro", multi_class="ovr")
    roc_auc_weighted = roc_auc_score(y_test_bin, y_proba, average="weighted", multi_class="ovr")
except ValueError as e:
    roc_auc_macro = roc_auc_weighted = float("nan")
    print(f"ROC-AUC could not be computed: {e}")

report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
report_text = classification_report(y_test, y_pred, zero_division=0)

print("\n" + "=" * 60)
print(f"{MODEL_NAME} — Classification Report")
print("=" * 60)
print(report_text)

print("=" * 60)
print("Summary metrics")
print("=" * 60)
print(f"Accuracy:                {accuracy:.4f}")
print(f"Balanced accuracy:        {balanced_acc:.4f}")
print(f"Precision (macro):        {precision_macro:.4f}")
print(f"Recall (macro):           {recall_macro:.4f}")
print(f"F1-score (macro):         {f1_macro:.4f}")
print(f"Precision (weighted):     {precision_weighted:.4f}")
print(f"Recall (weighted):        {recall_weighted:.4f}")
print(f"F1-score (weighted):      {f1_weighted:.4f}")
print(f"ROC-AUC (macro, OVR):     {roc_auc_macro:.4f}")
print(f"ROC-AUC (weighted, OVR):  {roc_auc_weighted:.4f}")
print(f"Matthews corr. coef:      {mcc:.4f}")
print(f"Cohen's kappa:            {kappa:.4f}")
print(f"Training time (s):        {train_time:.4f}")
print(f"Inference time (s):       {inference_time:.4f}")
print(f"Inference time/sample (ms): {inference_time_per_sample_ms:.4f}")

# Save all metrics to JSON
metrics_summary = {
    "model": MODEL_NAME,
    "random_state": RANDOM_STATE,
    "hyperparameters": rf_params,
    "accuracy": accuracy,
    "balanced_accuracy": balanced_acc,
    "precision_macro": precision_macro,
    "recall_macro": recall_macro,
    "f1_macro": f1_macro,
    "precision_weighted": precision_weighted,
    "recall_weighted": recall_weighted,
    "f1_weighted": f1_weighted,
    "roc_auc_macro_ovr": roc_auc_macro,
    "roc_auc_weighted_ovr": roc_auc_weighted,
    "matthews_corrcoef": mcc,
    "cohen_kappa": kappa,
    "training_time_seconds": train_time,
    "inference_time_seconds_full_test_set": inference_time,
    "inference_time_ms_per_sample": inference_time_per_sample_ms,
    "per_class_report": report_dict,
    "n_features_used": X_train_reduced.shape[1],
}
with open(f"metrics_{MODEL_NAME}.json", "w") as f:
    json.dump(metrics_summary, f, indent=2)
print(f"\nSaved full metrics to 'metrics_{MODEL_NAME}.json'")

# Confusion matrix — counts and row-normalized, saved as PNG
cm = confusion_matrix(y_test, y_pred, labels=classes)
cm_norm = confusion_matrix(y_test, y_pred, labels=classes, normalize="true")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=classes, yticklabels=classes, ax=axes[0],
)
axes[0].set_title(f"{MODEL_NAME} — Confusion Matrix (counts)")
axes[0].set_xlabel("Predicted label")
axes[0].set_ylabel("True label")

sns.heatmap(
    cm_norm, annot=True, fmt=".2f", cmap="Blues",
    xticklabels=classes, yticklabels=classes, ax=axes[1],
)
axes[1].set_title(f"{MODEL_NAME} — Confusion Matrix (row-normalized)")
axes[1].set_xlabel("Predicted label")
axes[1].set_ylabel("True label")

plt.tight_layout()
plt.savefig(f"confusion_matrix_{MODEL_NAME}.png", dpi=150)
plt.close()
print(f"Saved confusion matrix visualization to 'confusion_matrix_{MODEL_NAME}.png'")

# Feature importance plot
importances = pd.Series(rf.feature_importances_, index=X_train_reduced.columns)
top_importances = importances.sort_values(ascending=False).head(20)

plt.figure(figsize=(10, 8))
sns.barplot(x=top_importances.values, y=top_importances.index, color="steelblue")
plt.title(f"{MODEL_NAME} — Top 20 Feature Importances")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(f"feature_importance_{MODEL_NAME}.png", dpi=150)
plt.close()
print(f"Saved feature importance plot to 'feature_importance_{MODEL_NAME}.png'")

print("\nDone.")
