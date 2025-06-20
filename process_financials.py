import pandas as pd
import os

# --- Part 1: SETUP FOR A SINGLE FILE TEST ---
file_to_test = 'data/2024-10q.xls' 

print(f"--- Starting Test on Single File: {file_to_test} ---")


# --- Part 2: THE FINAL, REFINED read_excel COMMAND ---
df = pd.read_excel(
    file_to_test, 
    sheet_name='INCOME_STATEMENT', # Correct sheet name
    skiprows=18, # CORRECTED: Skip 18 rows to start at "Net sales"
    header=None,
    usecols="B:F",
    names=[
        'Metric', 
        'Three Months Ended 2024',
        'Three Months Ended 2023',
        'Nine Months Ended 2024',
        'Nine Months Ended 2023'
    ]
)

# --- Part 3: VERIFY THE RESULT ---
print("\n Successfully read the data. Here's the first look:")
print(df.head(10))

print("\n--- DataFrame Info ---")
df.info()