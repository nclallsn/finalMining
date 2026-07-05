import pandas as pd
import os

input_dir = "separated_datasets"
output_file = "sampled_500k_dataset.csv"

# CSV files to use
files = [
    "BENIGN.csv",
    "TFTP.csv",
    "MSSQL.csv",
    "NetBIOS.csv",
    "UDP.csv"
]

sampled_parts = []

for file in files:
    path = os.path.join(input_dir, file)

    df = pd.read_csv(path)

    # Check if enough rows exist
    if len(df) < 100000:
        raise ValueError(f"{file} has only {len(df):,} rows. Cannot sample 100,000 rows.")

    sampled = df.sample(n=100000, random_state=42)

    sampled_parts.append(sampled)

    print(f"{file}: sampled {len(sampled):,} rows")

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
counts = final_df[" Label"].value_counts()

for label, count in counts.items():
    percentage = count / len(final_df) * 100
    print(f"{label:<10} {count:>8,} ({percentage:.2f}%)")