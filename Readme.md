# 🧠 Hospital Monitoring Automation with Intelligent Agents

This project implements an **automated pipeline** based on **GitHub Actions** and Python agents to manage and monitor hospital data in real time.

The system combines data integration, occupancy analysis, and automatic alerts sent via Telegram.

The CSV files of historical data and forecasting predictions are a product of this project [Predictive Model of Health Deterioration in Hospitalized Patients in Spain](https://github.com/BarbaraAngelesOrtiz/Proyecto-Predicci-n-hospitalaria)

---

## ⚙️ System Architecture

### 🧩 Agent 1 – Data Integration and Updates
**Agent 1** connects to a **Google Drive** folder where the daily CSV files are stored:

- `hospital_data.csv` → actual hospital occupancy data.

- `predicciones.csv` → projected values ​​from the predictive model.

Automatically:

- Downloads the CSV files from Drive.
- Converts them into **Pandas DataFrames.**
- Uploads them to the **Google Spreadsheet** `Predicciones Hospitalarias`, updating the [sheets](https://docs.google.com/spreadsheets/d/1LjwDLl9KPb1Zid3uYbDMo99rCDElX2WxmY82phOFY3w/edit?gid=294779051#gid=294779051):
  - `hospital_data`
  - `predicciones`
  - `alertas_log`

This maintains a **centralized and up-to-date repository** of historical and predictive information.

<img width="1468" height="942" alt="predicciones" src="https://github.com/user-attachments/assets/b2a6abee-6f5d-455b-af4c-080b13ccfa7e" />
<img width="1275" height="943" alt="Alerts" src="https://github.com/user-attachments/assets/f0c7c299-86b7-4399-b8e9-9ded288ebe3d" />
<img width="1476" height="934" alt="hospital_data" src="https://github.com/user-attachments/assets/c7bf19b1-1af7-4fd9-9f9c-db1b08ad6d51" />

---

### 🤖 Agent 2 – Analysis, Risk Detection, and Alerts

**Agent 2** takes the data from the same Google Sheet and performs the occupancy analysis:

- **Actual occupancy (%)** → based on occupied beds vs. available beds (ward + ICU).
- **Predicted occupancy (%)** → derived from the prediction model.

The agent also:

- 🧹 **Cleans the data** and limits occupancy values ​​to 100%.
- 🏥 **Reconstructs the hospital** name from one-hot coded columns.
- 📲 **Sends automatic alerts via Telegram** when:
  - **Actual occupancy ≥ 85%**
  - **Projected occupancy ≥ 95%**
- 🗂️ **Record each event** in the `alerts_log` sheet with:
- Timestamp
- Alert Type
- Hospital
- Date
- Occupancy Percentage
- Submission Status

---

### 💬 Ejemplo de Alerta

🚨 ALERTA REAL (REAL ALERT) - 85%

🏥 Hospital: Central

📅 Fecha (Date): 2025-10-28 

💢  Ocupación total (Total Occupancy): 88.3%

<img width="1256" height="862" alt="Telegram" src="https://github.com/user-attachments/assets/f775ac35-9eb8-4df3-ae4c-ae6455364e05" />

---

## 🧰 Technology Stack

| Technology | Main use |
|-------------|----------------|
| **Python** | Processing, analysis, and automation|
| **Pandas** | Data cleaning and manipulation |
| **Google Drive API** | Download CSV files|
| **Google Sheets API (GSpread)** | Updating and reading spreadsheets |
| **Telegram Bot API** | Sending real-time alerts |
| **GitHub Actions** | Daily pipeline automation |

---

## 🚀 Automated Pipeline

The entire flow is executed automatically using **GitHub Actions**, which orchestrates both agents sequentially:

1. **Agent 1** → Sync data from Google Drive to Google Sheets.
2. **Agent 2** → It analyzes occupancy and sends alerts.

Each execution is logged in the GitHub Actions logs and in the `alertas_log` file.

---

## 🗂️ Repository Structure

```bash

📁 Proyecto-Predicci-n-hospitalaria/
├── data/                                                              # Clean data, ready for analysis
│     ├── hospital_data.csv                                            # Dataset Data Engineer 
│     └── predicciones.csv                                             # Dataset ML Forecasting 
│ 
├── Automation Agents/
│   ├── Agent1_data.py                                                 # Agent that synchronizes data from Google Drive to Google Sheets
│   └── Agent2_alerts.py                                               # Agent that analyzes occupancy and sends alerts
│
├── .github/                                          
│   └──workflows/                                                       
│       ├── Agent 1.yaml                                               # Workflow to run Agent 1: data integration from Google Drive to Google Sheets
│       └── Agent 2.yaml                                               # Workflow for Agent 2: processing hospital data and sending prediction alerts
│
├── image/                                                             # Agent visualizations and charts
│
├── README.md                                                          # Project Overview
└── requirements.txt                                                   # Libraries required to run the project
```

## Author
**Bárbara de los Ángeles Ortiz**

<img src="https://github.com/user-attachments/assets/30ea0d40-a7a9-4b19-a835-c474b5cc50fb" width="115">

[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | [GitHub](https://github.com/BarbaraAngelesOrtiz)

![Status](https://img.shields.io/badge/status-finished-brightgreen) 📅 Octubre 2025

![Python](https://img.shields.io/badge/Python-3.10-blue)
![GoogleAPI](https://img.shields.io/badge/Google_API-integrated-yellow)
![Telegram](https://img.shields.io/badge/Alerts-Telegram-blueviolet)
![GitHubActions](https://img.shields.io/badge/CI-GitHub_Actions-black)


