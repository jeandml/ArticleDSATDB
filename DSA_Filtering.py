# dsa_analyzer.py
import pandas as pd
import zipfile
from pathlib import Path
import io

def analyze_data(input_folder, output_file, keywords=['disinformation', 'misinformation']):
    """Extract rows containing keywords from nested zip files and save to CSV"""
    matching_rows = []
    input_dir = Path(input_folder)
    
    print(f"Looking for data in: {input_dir}")
    
    for outer_zip in input_dir.rglob('*.zip'):
        print(f"\nProcessing {outer_zip.name}")
        try:
            with zipfile.ZipFile(outer_zip, 'r') as outer_zf:
                inner_zips = [f for f in outer_zf.namelist() if f.endswith('.zip')]
                print(f"Found {len(inner_zips)} inner ZIP files")
                
                for inner_zip in inner_zips:
                    print(f"Processing inner ZIP: {inner_zip}")
                    try:
                        inner_zip_data = io.BytesIO(outer_zf.read(inner_zip))
                        with zipfile.ZipFile(inner_zip_data) as inner_zf:
                            csv_files = [f for f in inner_zf.namelist() if f.endswith('.csv')]
                            print(f"Found {len(csv_files)} CSV files")
                            
                            for csv_file in csv_files:
                                print(f"Reading {csv_file}")
                                df = pd.read_csv(inner_zf.open(csv_file), low_memory=False)
                                print(f"Found {len(df)} rows")
                                
                                mask = df.astype(str).apply(
                                    lambda x: x.str.contains('|'.join(keywords), case=False)
                                ).any(axis=1)
                                
                                if mask.any():
                                    matching_rows.append(df[mask])
                                    print(f"Found {mask.sum()} matching rows")
                                    
                    except Exception as e:
                        print(f"Error processing inner ZIP {inner_zip}: {e}")
                        
        except Exception as e:
            print(f"Error processing outer ZIP {outer_zip}: {e}")
    
    if matching_rows:
        all_matches = pd.concat(matching_rows, ignore_index=True)
        all_matches.to_csv(output_file, index=False)
        print(f"\nSaved {len(all_matches)} matching rows to: {output_file}")
    else:
        print("\nNo matching rows found")

if __name__ == "__main__":
    input_folder = "input_folder"
    output_file = "output_file.csv""
    analyze_data(input_folder, output_file)