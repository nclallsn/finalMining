import pandas as pd

# Load dataset
df = pd.read_csv("ready_dataset.csv")

print("Total rows:", len(df))

# Count labels
label_counts = df[" Label"].value_counts()
total_rows = len(df)

# BENIGN
selected_labels = ["BENIGN"]

# Add all attack labels with more than 100,000 rows
for label, count in label_counts.items():
    if label != "BENIGN" and count > 100000:
        selected_labels.append(label)

print("\nSelected Labels")
print("-" * 45)
print(f'{"Label":<15} {"Rows":>12} {"Percentage":>15}')
print("-" * 45)

for label in selected_labels:
    count = label_counts[label]
    percentage = (count / total_rows) * 100
    print(f'{label:<15} {count:>12,} {percentage:>14.2f}%')

print("\nExporting CSV files...")

# Export each selected label to its own CSV
for label in selected_labels:
    subset = df[df[" Label"] == label]

    filename = f"{label}.csv"
    subset.to_csv(filename, index=False)

    print(f"Saved {filename} ({len(subset):,} rows)")

print("\nDone!")