import os
import pandas as pd
import gspread
from google.oauth2 import service_account
import requests
from datetime import datetime, timedelta

# CONFIGURATIONS
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_NAME = "Predicciones Hospitalarias"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not GOOGLE_SHEETS_CREDENTIALS:
    raise ValueError("❌ Missing GOOGLE_SHEETS_CREDENTIALS")
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ Missing configuration TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")

# Authentication with explicit scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = service_account.Credentials.from_service_account_info(
    eval(GOOGLE_SHEETS_CREDENTIALS), scopes=scopes
)
gc = gspread.authorize(creds)

# FUNCTIONS
def send_telegram_alert(message: str):
  """Send alert to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"📩 Alert sent:{message[:80]}...")
        return "✅ Sent"
    else:
        print(f"⚠️Error sending alert: {response.text}")
        return "⚠️ Error"

def read_sheet(sheet_name):
    """Reads a Google Sheets document and returns it as a DataFrame"""
    sh = gc.open(SPREADSHEET_NAME)
    ws = sh.worksheet(sheet_name)
    df = pd.DataFrame(ws.get_all_records())
    print(f"📊 '{sheet_name}' loaded with {len(df)} rows.")
    return df

def get_or_create_log_sheet(sh):
   """Gets the log sheet (or creates it if it doesn't exist)"""
    try:
        return sh.worksheet("alertas_log")
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="alertas_log", rows=1, cols=6)
        ws.append_row(["timestamp", "tipo", "hospital", "fecha", "ocupacion_%", "estado_envio"])
        print("🗂️ 'alerts_log' sheet created.")
        return ws

def log_alerts_batch(ws, alertas):
   "Adds multiple alerts to the log in a single batch"
    if not alertas:
        return
    rows = [list(a.values()) for a in alertas]
    ws.append_rows(rows)
    print(f"📝 {len(rows)} alerts recorded in 'alerts_log''.")

# DATA READING
df_real = read_sheet("hospital_data")
df_pred = read_sheet("predicciones")

# Filter the last 6 months
fecha_limite = datetime.utcnow() - timedelta(days=180)

df_real["fecha"] = pd.to_datetime(df_real["fecha"], errors="coerce")
df_real = df_real[df_real["fecha"] >= fecha_limite]

df_pred["fecha"] = pd.to_datetime(df_pred["fecha"], errors="coerce")
df_pred = df_pred[df_pred["fecha"] >= fecha_limite]

print(f"📅 Analyzing data from: {fecha_limite.date()}")

sh = gc.open(SPREADSHEET_NAME)
ws_log = get_or_create_log_sheet(sh)

alertas_a_registrar = []

# ACTUAL OCCUPANCY ALERTS (85%)
df_real["ocupacion_total_%"] = (
    (df_real["camas_ocupadas_planta"] + df_real["camas_ocupadas_uci"]) /
    (df_real["camas_habilitadas_planta"] + df_real["camas_habilitadas_uci"]) * 100
).round(2)

# limit values ​​to 100%
df_real["ocupacion_total_%"] = df_real["ocupacion_total_%"].clip(upper=100)

# Reconstruct the hospital name from the one-hot columns
# Example: columns ['hospital_A', 'hospital_B', 'hospital_C'] -> hospital = 'A' or 'B' or 'C'
hospital_cols = [c for c in df_real.columns if c.startswith("hospital_")]

def obtener_nombre_hospital(row):
    for col in hospital_cols:
        if row.get(col) == 1:
            return col.replace("hospital_", "")
    return "Desconocido"

df_real["hospital_nombre"] = df_real.apply(obtener_nombre_hospital, axis=1)

# Filter real alerts >= 85%
alertas_reales = df_real[df_real["ocupacion_total_%"] >= 85]

for _, row in alertas_reales.iterrows():
    hospital = row.get("hospital_nombre", "Desconocido")
    msg = (
        f"🚨 <b>ALERTA REAL - 85%</b>\n"
        f"🏥 Hospital: {hospital}\n"
        f"📅 Fecha: {row['fecha'].date()}\n"
        f"💢 Ocupación total: {row['ocupacion_total_%']}%"
    )
    estado = send_telegram_alert(msg)

    alertas_a_registrar.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": "REAL 85%",
        "hospital": hospital,
        "fecha": str(row['fecha'].date()),
        "ocupacion_%": row["ocupacion_total_%"],
        "estado_envio": estado
    })


# PREDICTION ALERTS (95%)
df_pred["ocupacion_pred_%"] = (
    df_pred["pred_camas_total"] /
    (df_pred["camas_habilitadas_planta"] + df_pred["camas_habilitadas_uci"]) * 100
).round(2)

alertas_pred = df_pred[df_pred["ocupacion_pred_%"] >= 95]

for _, row in alertas_pred.iterrows():
    hospital = row.get("hospital", "Desconocido")
    msg = (
        f"🤖 <b>ALERTA PREDICCIÓN - 95%</b>\n"
        f"🏥 Hospital: {hospital}\n"
        f"📅 Fecha: {row['fecha'].date()}\n"
        f"📈 Ocupación proyectada: {row['ocupacion_pred_%']}%"
    )
    estado = send_telegram_alert(msg)

    alertas_a_registrar.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": "PREDICCIÓN 95%",
        "hospital": hospital,
        "fecha": str(row['fecha'].date()),
        "ocupacion_%": row["ocupacion_pred_%"],
        "estado_envio": estado
    })

# REGISTRATION IN A SINGLE CALL
log_alerts_batch(ws_log, alertas_a_registrar)

print(f"🎯 Agente ejecutado correctamente: {len(alertas_a_registrar)} alertas procesadas.")



