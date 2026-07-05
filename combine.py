import pandas as pd
import os

input_dir = "separated_datasets"
output_file = "combined.csv"

# CSV files to use
files = [
    "BENIGN.csv",
    "TFTP.csv",
    "UDP.csv",
    "SSDP.csv",
    "NTP.csv"
]

# Read each CSV into a DataFrame
dfs = [pd.read_csv(os.path.join(input_dir, file)) for file in files]

# Combine all DataFrames
final_df = pd.concat(dfs, ignore_index=True)

# Shuffle the dataset
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
final_df.to_csv(output_file, index=False)

print(f"Saved {len(final_df)} rows to {output_file}")