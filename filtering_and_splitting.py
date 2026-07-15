import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif

INPUT_CSV = "sampled_500k_dataset.csv"   
TARGET_COLUMN = "label"                 
CORR_THRESHOLD = 0.9
TEST_SIZE = 0.20
RANDOM_STATE = 8

df = pd.read_csv(INPUT_CSV)
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE,
)

corr_matrix = X_train.corr().abs()

plt.figure(figsize=(20, 16))
sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    annot=False,
    linewidths=0.5,
    cbar_kws={"label": "Absolute Correlation"},
)
plt.title("Feature Correlation Heatmap (Train Set Only)", fontsize=16)
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150)
plt.close()

upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

high_corr_pairs = (
    upper.stack()
    .reset_index()
    .rename(columns={"level_0": "Feature_1", "level_1": "Feature_2", 0: "Correlation"})
)
high_corr_pairs = high_corr_pairs[
    high_corr_pairs["Correlation"] > CORR_THRESHOLD
].sort_values("Correlation", ascending=False)

print(f"\nHighly correlated feature pairs (> {CORR_THRESHOLD}), computed on train set:")
print(high_corr_pairs)

print("\nComputing mutual information scores on the training set...")
mi_scores = mutual_info_classif(X_train, y_train, random_state=RANDOM_STATE)
mi_series = pd.Series(mi_scores, index=X_train.columns)

print("\nTop 15 features by mutual information (train set):")
print(mi_series.sort_values(ascending=False).head(15))

to_drop = set()
for _, row in high_corr_pairs.iterrows():
    f1, f2 = row["Feature_1"], row["Feature_2"]
    if f1 in to_drop or f2 in to_drop:
        continue
    if mi_series[f1] >= mi_series[f2]:
        to_drop.add(f2)
    else:
        to_drop.add(f1)

print(f"\nDropped {len(to_drop)} columns (decision made on train set only): {sorted(to_drop)}")

# Apply the SAME drop list to both train and test — no re-fitting on test
X_train_reduced = X_train.drop(columns=to_drop)
X_test_reduced = X_test.drop(columns=to_drop)

print(f"Remaining columns: {X_train_reduced.shape[1]} (from original {X.shape[1]})")

train_out = X_train_reduced.copy()
train_out[TARGET_COLUMN] = y_train.values
test_out = X_test_reduced.copy()
test_out[TARGET_COLUMN] = y_test.values
train_out.to_csv("train_reduced.csv", index=False)
test_out.to_csv("test_reduced.csv", index=False)
