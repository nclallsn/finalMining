import pandas as pd

input_file = "combined.csv"
output_file = "sampled_500k_dataset.csv"

# Read combined dataset
df = pd.read_csv(input_file)

sampled_parts = []

# Labels to sample
labels = ["BENIGN", "TFTP", "UDP", "SSDP", "NTP"]

for label in labels:
    label_df = df[df["Label"] == label]

    # Check if enough rows exist
    if len(label_df) < 100000:
        raise ValueError(
            f"{label} has only {len(label_df):,} rows. Cannot sample 100,000 rows."
        )

    sampled = label_df.sample(n=100000, random_state=42)
    sampled_parts.append(sampled)

    print(f"{label}: sampled {len(sampled):,} rows")

# Combine all sampled data
final_df = pd.concat(sampled_parts, ignore_index=True)

# Shuffle the dataset
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
final_df.to_csv(output_file, index=False)

print("\nSaved:", output_file)
print("Final shape:", final_df.shape)

# Show final class distribution
print("\nFinal class distribution:")
counts = final_df["Label"].value_counts()

for label, count in counts.items():
    percentage = count / len(final_df) * 100
    print(f"{label:<10} {count:>8,} ({percentage:.2f}%)")