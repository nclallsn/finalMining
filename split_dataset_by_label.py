import pandas as pd

# Load dataset
df = pd.read_csv('ready_dataset.csv')

print("Total rows: ", len(df))

# Print BENIGN and the TOP 4 DDoS attack types
# Count Labels
label_counts = df[" Label"].value_counts()

# Separate BENIGN
benign_count = label_counts.get("BENIGN", 0)

# Top 4 attack
top_attacks = label_counts.drop("BENIGN").head(4)

# Total rows
total_rows = len(df)

print("\nSelected Labels")
print("-" * 45)
print(f'{"Label":<15} {"Rows":>10} {"Percentage":>15}')
print("-" * 45)

# Print BENIGN first
print(f'{"BENIGN":<15} {benign_count:>10,} {(benign_count/total_rows*100):>14.2f}%')

# Print top 4 attacks
for label, count in top_attacks.items():
    percentage = count / total_rows * 100
    print(f'{label:<15} {count:>10,} {percentage:>14.2f}%')

# Labels to export
selected_labels = ["BENIGN"] + list(top_attacks.index)

for label in selected_labels:
    subset = df[df[" Label"] == label]

    filename = f"{label}.csv"
    subset.to_csv(filename, index=False)

    print(f"Saved {filename} ({len(subset):,} rows)")