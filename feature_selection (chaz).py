import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------
# Step 0: Read dataset
# ------------------------------------------------------
df = pd.read_csv("sampled_500k_dataset.csv")

target_column = "label"

X = df.drop(columns=[target_column])
y = df[target_column]

# ------------------------------------------------------
# Step 1: Train-test split FIRST to avoid data leakage
# ------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ------------------------------------------------------
# Step 2: Feature selection using TRAINING SET ONLY
# Correlation filtering + Mutual Information
# ------------------------------------------------------
corr_matrix = X_train.corr().abs()

upper = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)

threshold = 0.90

high_corr_pairs = (
    upper.stack()
    .reset_index()
    .rename(columns={
        "level_0": "Feature_1",
        "level_1": "Feature_2",
        0: "Correlation"
    })
)

high_corr_pairs = high_corr_pairs[
    high_corr_pairs["Correlation"] > threshold
].sort_values("Correlation", ascending=False)

print("Highly correlated feature pairs (> 0.90):")
print(high_corr_pairs)

# ------------------------------------------------------
# Step 3: Mutual information using TRAINING SET ONLY
# ------------------------------------------------------
print("\nComputing mutual information scores...")

mi_scores = mutual_info_classif(
    X_train,
    y_train,
    random_state=42
)

mi_series = pd.Series(mi_scores, index=X_train.columns)

print("\nTop 15 features by mutual information:")
print(mi_series.sort_values(ascending=False).head(15))

# ------------------------------------------------------
# Step 4: Drop lower-MI feature from each highly correlated pair
# ------------------------------------------------------
to_drop = set()

for _, row in high_corr_pairs.iterrows():
    f1 = row["Feature_1"]
    f2 = row["Feature_2"]

    if f1 in to_drop or f2 in to_drop:
        continue

    if mi_series[f1] >= mi_series[f2]:
        to_drop.add(f2)
    else:
        to_drop.add(f1)

selected_features = [col for col in X_train.columns if col not in to_drop]

X_train_selected = X_train[selected_features]
X_test_selected = X_test[selected_features]

print(f"\nDropped {len(to_drop)} columns:")
print(sorted(to_drop))

print(f"\nRemaining features: {len(selected_features)}")
print(selected_features)

# ------------------------------------------------------
# Step 5: Feature scaling for KNN
# Fit scaler on TRAINING SET ONLY
# ------------------------------------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_selected)
X_test_scaled = scaler.transform(X_test_selected)

X_train_scaled = pd.DataFrame(
    X_train_scaled,
    columns=selected_features,
    index=X_train_selected.index
)

X_test_scaled = pd.DataFrame(
    X_test_scaled,
    columns=selected_features,
    index=X_test_selected.index
)

# ------------------------------------------------------
# Step 6: Save outputs
# ------------------------------------------------------
train_unscaled = X_train_selected.copy()
train_unscaled[target_column] = y_train

test_unscaled = X_test_selected.copy()
test_unscaled[target_column] = y_test

train_scaled = X_train_scaled.copy()
train_scaled[target_column] = y_train.values

test_scaled = X_test_scaled.copy()
test_scaled[target_column] = y_test.values

train_unscaled.to_csv("train_selected_unscaled.csv", index=False)
test_unscaled.to_csv("test_selected_unscaled.csv", index=False)

train_scaled.to_csv("train_selected_scaled.csv", index=False)
test_scaled.to_csv("test_selected_scaled.csv", index=False)

print("\nSaved files:")
print("train_selected_unscaled.csv  -> for Decision Tree / Random Forest")
print("test_selected_unscaled.csv   -> for Decision Tree / Random Forest")
print("train_selected_scaled.csv    -> for KNN")
print("test_selected_scaled.csv     -> for KNN")