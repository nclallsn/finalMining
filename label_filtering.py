import pandas as pd

df = pd.read_csv("ready_dataset.csv")

label_column = " Label"
minimum_rows = 100000

print("Total rows:", len(df))

label_counts = df[label_column].value_counts()

selected_dfs = []

print("\nLabel Analysis")
print("-" * 90)
print(
    f'{"Label":<20}'
    f'{"Original":>15}'
    f'{"Null Rows":>15}'
    f'{"Duplicates":>15}'
    f'{"Adjusted":>15}'
)
print("-" * 90)

for label, original_count in label_counts.items():

    # Get all rows for the current label
    subset = df[df[label_column] == label]

    # Count rows containing at least one null value
    null_row_count = subset.isnull().any(axis=1).sum()

    # Count duplicate rows while keeping the first occurrence
    duplicate_row_count = subset.duplicated(keep="first").sum()

    # Adjusted row count 
    adjusted_row_count = (
        original_count
        - null_row_count
        - duplicate_row_count
    )

    print(
        f'{str(label):<20}'
        f'{original_count:>15,}'
        f'{null_row_count:>15,}'
        f'{duplicate_row_count:>15,}'
        f'{adjusted_row_count:>15,}'
    )

    # Keep the ORIGINAL rows if the adjusted count is > 100,000
    if adjusted_row_count > minimum_rows:
        selected_dfs.append(subset)

# Combine all selected labels into one DataFrame
final_df = pd.concat(selected_dfs, ignore_index=True)

output_file = "top5_class.csv"
final_df.to_csv(output_file, index=False)

print(f"\nSaved {len(final_df):,} original rows to {output_file}")
print("Done!")
