import pandas as pd
import os
import glob

# --- 1. SETUP ---
data_folder_path = 'data/'
output_file_name = 'master_financial_data.csv'
all_data_frames = []
all_files = glob.glob(os.path.join(data_folder_path, "*.xls*"))

print(f"Found {len(all_files)} files to process...")

# --- 2. LOOP THROUGH AND PROCESS EACH FILE ---
for file in all_files:
    print(f"Processing: {file}...")
    
    try:
        # --- Attempt to read the WIDE format (e.g., Q2, Q3, Q4/10-K reports) ---
        df = pd.read_excel(
            file,
            sheet_name='INCOME_STATEMENT',
            skiprows=18,
            header=None,
            usecols="B:F",
            names=[
                'Metric', 'Current Quarter', 'Prior Year Quarter',
                'Current YTD', 'Prior Year YTD'
            ]
        )
    except pd.errors.ParserError:
        # --- If it fails, it's likely the NARROW format (e.g., a Q1 report) ---
        print(f"  -> Caught a ParserError. Retrying with a narrow column format.")
        df = pd.read_excel(
            file,
            sheet_name='INCOME_STATEMENT',
            skiprows=18,
            header=None,
            usecols="B:D", # Only read the first 3 columns
            names=['Metric', 'Current Quarter', 'Prior Year Quarter']
        )

    # --- Part B: CLEANING ---
    # The rest of the script remains largely the same
    numeric_cols = df.columns.drop('Metric') # Cleverly get all numeric columns
    df.dropna(subset=numeric_cols, how='all', inplace=True)
    df['Metric'] = df['Metric'].str.strip().str.replace(':', '')
    metrics_to_keep = [
        'Products', 'Services', 'Total net sales', 'Gross margin',
        'Research and development', 'Selling, general and administrative',
        'Total operating expenses', 'Operating income', 'Net income'
    ]
    df = df[df['Metric'].isin(metrics_to_keep)]
    
    # --- Part C: RESHAPING (MELTING) ---
    df_melted = df.melt(
        id_vars=['Metric'],
        var_name='Period_Type_Raw',
        value_name='Amount'
    )
    
    # --- Part D: FEATURE ENGINEERING ---
    filename = os.path.basename(file)
    # Using .lower() to handle both 'q' and 'Q'
    year_from_file = int(filename.lower().split('-')[0])
    quarter_from_file = filename.lower().split('-')[1].split('.')[0]
    
    df_melted['Fiscal Year'] = year_from_file
    df_melted['Fiscal Quarter'] = quarter_from_file.upper() # Standardize to upper-case 'Q'
    
    all_data_frames.append(df_melted)

# --- 3. COMBINE AND SAVE THE MASTER FILE ---
master_df = pd.concat(all_data_frames, ignore_index=True)

# Final clean up to ensure data types are correct
master_df['Amount'] = pd.to_numeric(master_df['Amount'])

master_df.to_csv(output_file_name, index=False)

print(f"\n✅ Processing complete!")
print(f"Master file '{output_file_name}' has been created with {len(master_df)} rows.")
print("This file is now ready to be loaded into Power BI or Tableau.")