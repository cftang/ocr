import pandas as pd
import os
import sys

def csvs_to_excel_sheets(input_files, output_file):
    """
    Reads multiple CSV files and saves each as a separate sheet in an Excel file.

    Args:
        input_files: List of input CSV file paths
        output_file: Path to the output Excel file (.xlsx)
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

    total_rows = 0
    total_sheets = 0

    # Use ExcelWriter to create Excel file with multiple sheets
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Read each CSV file and save as a sheet
            for i, csv_filepath in enumerate(input_files, 1):
                csv_filename = os.path.basename(csv_filepath)
                print(f"[{i}] Reading: {csv_filename}")

                try:
                    df = pd.read_csv(csv_filepath)
                    print(f"    -> Rows: {len(df)}, Columns: {len(df.columns)}")

                    # Create sheet name from filename (remove extension and sanitize)
                    sheet_name = os.path.splitext(csv_filename)[0]

                    # Excel sheet names have limitations
                    # Max 31 characters, cannot contain: \ / ? * [ ] :
                    sheet_name = ''.join(c for c in sheet_name[:31] if c.isalnum() or c in (' ', '_', '-'))

                    # Save to sheet
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"    -> Saved to sheet: '{sheet_name}'")

                    total_rows += len(df)
                    total_sheets += 1
                    print(f"    -> Loaded successfully.\n")

                except pd.errors.EmptyDataError:
                    print(f"    -> WARNING: CSV file is empty. Skipping.\n")
                except Exception as e:
                    print(f"    -> ERROR: Could not process this file. Details: {e}\n")
                    sys.exit(1)

        print(f"\n=== SUCCESS ===")
        print(f"Excel file '{output_file}' created successfully!")
        print(f"Total sheets: {total_sheets}")
        print(f"Total rows across all sheets: {total_rows}")

    except Exception as e:
        print(f"\nERROR: Could not create Excel file. Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_csvs_to_excel.py <input1.csv> <input2.csv> ... <output.xlsx>")
        print("Example: python merge_csvs_to_excel.py file1.csv file2.csv file3.csv output.xlsx")
        print("\nNote: Each input CSV will be saved as a separate sheet in the Excel file.")
        print("Sheet names are derived from the CSV filenames (with extensions removed).")
        sys.exit(1)

    # Last argument is the output file
    output_file = sys.argv[-1]

    # All arguments except the last one are input files
    input_files = sys.argv[1:-1]

    csvs_to_excel_sheets(input_files, output_file)
    