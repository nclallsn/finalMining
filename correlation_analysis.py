import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif

df = pd.read_csv("sampled.csv")  

# Separate features (X) from target (y)
target_column = "label"  
X = df.drop(columns=[target_column])
y = df[target_column]

# Compute the correlation matrix
corr_matrix = X.corr().abs()

# Visualize it as a heatmap
plt.figure(figsize=(20, 16))
sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    annot=False,
    linewidths=0.5,
    cbar_kws={"label": "Absolute Correlation"}
)
plt.title("Feature Correlation Heatmap", fontsize=16)
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Identify highly correlated feature pairs 
upper = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)

threshold = 0.9
high_corr_pairs = (
    upper.stack()
    .reset_index()
    .rename(columns={"level_0": "Feature_1", "level_1": "Feature_2", 0: "Correlation"})
)
high_corr_pairs = high_corr_pairs[high_corr_pairs["Correlation"] > threshold].sort_values(
    "Correlation", ascending=False
)
print("Highly correlated feature pairs (> 0.9):")
print(high_corr_pairs)

# Compute Mutual Information scores against the target
print("\nComputing mutual information scores...")
mi_scores = mutual_info_classif(X, y, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns)

print("\nTop 15 features by mutual information:")
print(mi_series.sort_values(ascending=False).head(15))

# For each highly correlated pair, drop the one with LOWER mutual information
to_drop = set()

for _, row in high_corr_pairs.iterrows():
    f1, f2 = row["Feature_1"], row["Feature_2"]

    # Skip if either feature was already dropped in an earlier chain
    if f1 in to_drop or f2 in to_drop:
        continue

    if mi_series[f1] >= mi_series[f2]:
        to_drop.add(f2)
    else:
        to_drop.add(f1)

X_reduced = X.drop(columns=to_drop)

print(f"\nDropped {len(to_drop)} columns: {sorted(to_drop)}")
print(f"Remaining columns: {X_reduced.shape[1]} (from original {X.shape[1]})")

# Save the reduced dataset (features + target) to a new CSV
df_reduced = X_reduced.copy()
df_reduced[target_column] = y  

output_filename = "sampled_reduced.csv"
df_reduced.to_csv(output_filename, index=False)

print(f"\nSaved reduced dataset to '{output_filename}'")
print(f"Final shape: {df_reduced.shape[0]} rows x {df_reduced.shape[1]} columns")
