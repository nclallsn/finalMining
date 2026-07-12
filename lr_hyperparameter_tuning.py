# Hyperparameter tuning for the Logistic Regression classifier (multinomial).

import json
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Config
TRAIN_CSV = "train_reduced.csv"
TARGET_COLUMN = "label"
RANDOM_STATE = 8

# Load the already-split, already-feature-filtered training set
train_df = pd.read_csv(TRAIN_CSV)
X_train_reduced = train_df.drop(columns=[TARGET_COLUMN])
y_train = train_df[TARGET_COLUMN]

print(f"Loaded '{TRAIN_CSV}': {X_train_reduced.shape[0]} rows, {X_train_reduced.shape[1]} features")

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(
        random_state=RANDOM_STATE,
        max_iter=5000,
    )),
])

# Hyperparameter grid
param_grid = [
    {
        "clf__solver": ["lbfgs"],
        "clf__l1_ratio": [0],
        "clf__C": [0.001, 0.01, 0.1, 1, 10],
    },
    {
        "clf__solver": ["saga"],
        "clf__l1_ratio": [0, 1],
        "clf__C": [0.001, 0.01, 0.1, 1, 10],
    },
    {
        "clf__solver": ["saga"],
        "clf__l1_ratio": [0.15, 0.5, 0.85],
        "clf__C": [0.001, 0.01, 0.1, 1, 10],
    },
]

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=3,
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
best_params_clean = {
    key.replace("clf__", ""): value for key, value in grid.best_params_.items()
}

with open("best_logreg_params.json", "w") as f:
    json.dump(best_params_clean, f, indent=2)

print("\nSaved best parameters to 'best_logreg_params.json'.")