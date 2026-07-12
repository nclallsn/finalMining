# Hyperparameter tuning for the Random Forest classifier.

import json
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Config
TRAIN_CSV = "train_reduced.csv"
TARGET_COLUMN = "label"
RANDOM_STATE = 42

# Load the already-split, already-feature-filtered training set
train_df = pd.read_csv(TRAIN_CSV)
X_train_reduced = train_df.drop(columns=[TARGET_COLUMN])
y_train = train_df[TARGET_COLUMN]

print(f"Loaded '{TRAIN_CSV}': {X_train_reduced.shape[0]} rows, {X_train_reduced.shape[1]} features")

# Hyperparameter grid
param_grid = {
    "n_estimators": [200, 300, 500],
    "max_depth": [10, 20, 30, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"],
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
    param_grid,
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
    verbose=2,
)

print("\nRunning grid search...")
grid.fit(X_train_reduced, y_train)

print("\nBest parameters found:")
print(grid.best_params_)
print(f"\nBest cross-validated macro F1: {grid.best_score_:.4f}")

# Save best params
with open("best_rf_params.json", "w") as f:
    json.dump(grid.best_params_, f, indent=2)

print("\nSaved best parameters to 'best_rf_params.json'.")