import pandas as pd
import requests
from io import BytesIO
import json

# --- Config ---
url = "https://raw.githubusercontent.com/madhu-bcs/start-stop-vm/main/newstart/Infra_CMDB_Template.xlsx"  # replace with your GitHub raw file URL

# --- Download Excel ---
response = requests.get(url, timeout=10)
response.raise_for_status()

# --- Load Excel ---
excel_data = pd.read_excel(BytesIO(response.content))
excel_data = excel_data.fillna("")  # replace NaN with empty string

# --- Prepare columns ---
base_columns = ['Hostname', 'Instance Id', 'Account', 'Region', 'Platform']
app_columns = [col for col in excel_data.columns if str(col).startswith("Approver")]

# --- Create flat JSON output ---
result = excel_data[base_columns + app_columns].astype(str).to_dict(orient="records")

# --- Print full JSON in ##gbStart## format ---
print(f"##gbStart##output1##splitKeyValue##{json.dumps(result)}##gbEnd##")

# --- Optional: Print each Approver column separately ---
def format_approver_output(app_key, values):
    """Format Approver values as [{key: value}, ...]"""
    return ",".join([f'{{"{app_key}": "{v}"}}' for v in values if v != ""])

for col in app_columns:
    values = excel_data[col].astype(str).tolist()
    formatted = format_approver_output(col, values)
    print(f"##gbStart##{col.lower().replace(' ', '')}##splitKeyValue##[{formatted}]##gbEnd##")
