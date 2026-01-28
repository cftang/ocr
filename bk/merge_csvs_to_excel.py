import pandas as pd
import os
import sys

def merge_csvs_to_csv(input_files, output_file):
    """
    Reads multiple CSV files and merges them into a single CSV file.

    Args:
        input_files: List of input CSV file paths
        output_file: Path to the output merged CSV file
    """

    if not input_files:
        print("ERROR: No input files provided.")
        sys.exit(1)

    # Verify all input files exist
    for filepath in input_files:
        if not os.path.exists(filepath):
            print(f"ERROR: Input file does not exist: '{filepath}'")
            sys.exit(1)

    print(f"Processing {len(input_files)} CSV file(s)...\n")

    all_dataframes = []
    total_rows = 0

    # Read each CSV file
    for i, csv_filepath in enumerate(input_files, 1):
        csv_filename = os.path.basename(csv_filepath)
        print(f"[{i}] Reading: {csv_filename}")

        try:
            df = pd.read_csv(csv_filepath)
            print(f"    -> Rows: {len(df)}, Columns: {len(df.columns)}")
            all_dataframes.append(df)
            total_rows += len(df)
            print(f"    -> Loaded successfully.\n")
        except pd.errors.EmptyDataError:
            print(f"    -> WARNING: CSV file is empty. Skipping.\n")
        except Exception as e:
            print(f"    -> ERROR: Could not process this file. Details: {e}\n")
            sys.exit(1)

    if not all_dataframes:
        print("ERROR: No data to merge.")
        sys.exit(1)

    # Merge all dataframes
    print("Merging dataframes...")
    merged_df = pd.concat(all_dataframes, ignore_index=True)

    # Save to output CSV
    try:
        merged_df.to_csv(output_file, index=False)
        print(f"\n=== SUCCESS ===")
        print(f"Merged CSV file '{output_file}' created successfully!")
        print(f"Total rows: {total_rows}")
        print(f"Total columns: {len(merged_df.columns)}")
    except Exception as e:
        print(f"\nERROR: Could not save output file. Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_csvs_to_excel.py <input1.csv> <input2.csv> ... <output.csv>")
        print("Example: python merge_csvs_to_excel.py file1.csv file2.csv file3.csv merged_output.csv")
        sys.exit(1)

    # Last argument is the output file
    output_file = sys.argv[-1]

    # All arguments except the last one are input files
    input_files = sys.argv[1:-1]

    merge_csvs_to_csv(input_files, output_file)