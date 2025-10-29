import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from io import BytesIO
import gspread

# GENERAL SETTINGS
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

if not DRIVE_FOLDER_ID:
    raise ValueError("❌ Variable DRIVE_FOLDER_ID not defined in the environment.")
if not GOOGLE_SHEETS_CREDENTIALS:
    raise ValueError("❌ Variable GOOGLE_SHEETS_CREDENTIALS not defined in the environment.")

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Create credentials with valid scopes
creds = service_account.Credentials.from_service_account_info(
    eval(GOOGLE_SHEETS_CREDENTIALS),
    scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=creds)
gc = gspread.authorize(creds)

# AUXILIARY FUNCTIONS
def download_csv_from_drive(filename):
  """Download a CSV from the DRIVE_FOLDER_ID folder"""
    query = f"'{DRIVE_FOLDER_ID}' in parents and name='{filename}' and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        raise FileNotFoundError(f"⚠️ The file '{filename}' was not found in the Drive folder.")
    
    file_id = items[0]['id']
    request = drive_service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = drive_service._http.request(request.uri)
    content = downloader[1]
    df = pd.read_csv(BytesIO(content))
    print(f"✅ Archive '{filename}' successfully loaded with {len(df)} rows.")
    return df

def upload_to_google_sheets(df, spreadsheet_name, sheet_name):
   "Upload DataFrame to a specific sheet within a Google Sheet"
    try:
        sh = gc.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(spreadsheet_name)
        print(f"📘 New Google Sheet created: {spreadsheet_name}")
    
    try:
        worksheet = sh.worksheet(sheet_name)
        sh.del_worksheet(worksheet)
        worksheet = sh.add_worksheet(title=sheet_name, rows=df.shape[0]+1, cols=df.shape[1])
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=sheet_name, rows=df.shape[0]+1, cols=df.shape[1])
    
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(f"📤 Data loaded into sheet: '{sheet_name}' ({len(df)} rows)")

# DOWNLOAD CSVs FROM DRIVE
print("📁 Downloading files from Google Drive...")
hospital_df = download_csv_from_drive("hospital_data.csv")
predicciones_df = download_csv_from_drive("predicciones.csv")

# UPLOAD TO GOOGLE SHEETS
SPREADSHEET_NAME = "Predicciones Hospitalarias"
upload_to_google_sheets(hospital_df, SPREADSHEET_NAME, "hospital_data")
upload_to_google_sheets(predicciones_df, SPREADSHEET_NAME, "predicciones")

print("🎯 Upload completed successfully.")
