import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
base_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(base_dir, 'credentials.json')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(credentials)
sheet_id = '1j4S10Y5Kpe_I3rQYazOPed8c_wjU28CDSdyhpqwXi4I'
sheet = client.open_by_key(sheet_id).sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)
input_name = input("Enter the name to check: ")
if input_name in df['Name'].tolist():
    idx = df[df['Name'] == input_name].index[0]
    existing_status = df.loc[idx, 'Status']

    if existing_status == 'In Progress':
        print(f"The name '{input_name}' is already in 'In Progress' status.")
        reason = input(f"Provide a reason why '{input_name}' should be allotted again: ")
        if reason:
            df.loc[idx, 'Comments'] = reason
            sheet.update(f'F{idx + 2}', [[reason]])
            empty_name_idx = df[df['Name'] == ""].index
            if len(empty_name_idx) > 0:
                df.loc[empty_name_idx[0], 'Name'] = input_name
                df.loc[empty_name_idx[0], 'Status'] = "In Progress"
                row_values = df.loc[empty_name_idx[0]].tolist()
                sheet.update(f'A{empty_name_idx[0] + 2}', [row_values])
                print(f"The name '{input_name}' has been assigned to an empty row with 'In Progress' status.")
            else:
                print("No empty row found. Cannot assign the new name.")
        else:
            print("No reason provided. Cannot proceed with allotment.")
    else:
        print(f"The name '{input_name}' exists with status '{existing_status}'.")
else:
    empty_name_idx = df[df['Name'] == ""].index
    if len(empty_name_idx) > 0:
        df.loc[empty_name_idx[0], 'Name'] = input_name
        df.loc[empty_name_idx[0], 'Status'] = "In Progress"
        row_values = df.loc[empty_name_idx[0]].tolist()
        sheet.update(f'A{empty_name_idx[0] + 2}', [[row_values]])
        print(f"The name '{input_name}' has been assigned to an empty row with 'In Progress' status.")
    else:
        print("No empty row found. Cannot assign the new name.")
print("Current data in the sheet:")
print(df)
in_progress_df = df[df['Status'] == 'In Progress']
names_in_progress = in_progress_df['Name'].tolist()
print("Names with status 'In Progress':")
print(names_in_progress)
