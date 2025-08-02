import pandas as pd
from datetime import datetime

DATE_STR = datetime.now().strftime('%m.%d.%y')

def areaCodeFinder():

    print("Starting script...")

    #Open Files
    input_df = pd.read_excel("input.xlsx", engine='openpyxl')
    npa_report_df = pd.read_csv("report/npa_report.csv", skiprows=1)

    #Correcting Input Header
    input_df.columns = input_df.columns.str.strip()
    if input_df.columns[0] != 'Phone':
        print(f"Warning: First column was '{input_df.columns[0]}', renaming to 'Phone'")
        input_df.columns.values[0] = 'Phone'

    #Clean Input
    input_df['CleanPhone'] = input_df['Phone'].astype(str).str.replace(r'\D', '', regex=True)
    input_df['CleanPhone'] = input_df['CleanPhone'].apply(lambda x: x[1:] if len(x) == 11 and x.startswith('1') else x)
    input_df['AreaCode'] = input_df['CleanPhone'].astype(str).str[:3]

    #Clean Primary Key
    npa_report_df['NPA_ID'] = npa_report_df['NPA_ID'].astype(str)

    #Peform Lookup
    merged_df = input_df.merge(npa_report_df[['NPA_ID', 'LOCATION', 'COUNTRY', 'IN_SERVICE']], left_on='AreaCode', right_on='NPA_ID', how='left')

    #Write File As CSV
    merged_df.to_csv(f'output {DATE_STR}.csv', index=False)

    #Script Complete
    print(f"Script complete! File save as 'output {DATE_STR}.csv'.")