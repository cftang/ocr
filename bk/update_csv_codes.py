import pandas as pd
import os

def update_stock_codes(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    if '代码' not in df.columns:
        print("Error: '代码' column not found in the CSV.")
        return

    print("Updating stock codes...")
    
    def add_prefix(code):
        x = str(code).strip().zfill(6)
            
        # skip if already has prefix
        if x.startswith(('SH', 'SZ', 'BJ')):
            return x

        # apply logic based on starting digits
        if x.startswith(('60', '68', '90')):
            return 'SH' + x
        elif x.startswith(('30', '00')):
            return 'SZ' + x
        elif x.startswith('92'):
            return 'BJ' + x
        
        return x

    df['代码'] = df['代码'].apply(add_prefix)

    output_file = file_path.replace('.csv', '_fixed.csv')
    print(f"Saving updated data to {output_file}...")
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print("Optimization complete!")

if __name__ == "__main__":
    target_csv = "concept_stocks2.csv"
    update_stock_codes(target_csv)
