# 🧠 Automatización de Monitoreo Hospitalario con Agentes Inteligentes

Este proyecto implementa un **pipeline automatizado** basado en **GitHub Actions** y agentes en Python para gestionar y monitorear datos hospitalarios en tiempo real.  
El sistema combina integración de datos, análisis de ocupación y envío de alertas automáticas por Telegram.

Los archivos csv de datos historicos y predicción forecasting son producto del proyecto [Modelo Predictivo de Deterioro de Salud en Pacientes Hospitalizados en España](https://github.com/BarbaraAngelesOrtiz/Proyecto-Predicci-n-hospitalaria)

---

## ⚙️ Arquitectura del Sistema

### 🧩 Agente 1 – Integración y Actualización de Datos
El **Agente 1** se conecta a una carpeta de **Google Drive** donde se alojan los archivos CSV diarios:

- `hospital_data.csv` → datos reales de ocupación hospitalaria.  
- `predicciones.csv` → valores proyectados del modelo predictivo.

Automáticamente:
- Descarga los CSV desde Drive.  
- Los convierte en **DataFrames de Pandas**.  
- Los sube al **Google Spreadsheet** `Predicciones Hospitalarias`, actualizando las hojas:
  - `hospital_data`
  - `predicciones`

De esta forma se mantiene un **repositorio centralizado y actualizado** de información histórica y predictiva.

<img width="1468" height="942" alt="predicciones" src="https://github.com/user-attachments/assets/b2a6abee-6f5d-455b-af4c-080b13ccfa7e" />
<img width="1275" height="943" alt="Alerts" src="https://github.com/user-attachments/assets/f0c7c299-86b7-4399-b8e9-9ded288ebe3d" />
<img width="1476" height="934" alt="hospital_data" src="https://github.com/user-attachments/assets/c7bf19b1-1af7-4fd9-9f9c-db1b08ad6d51" />

---

### 🤖 Agente 2 – Análisis, Detección de Riesgos y Alertas

El **Agente 2** toma los datos desde el mismo Google Sheet y realiza el análisis de ocupación:

- **Ocupación real (%)** → basada en camas ocupadas vs. camas habilitadas (planta + UCI).  
- **Ocupación predicha (%)** → proveniente del modelo de predicción.

El agente además:

- 🧹 **Limpia los datos** y limita los valores de ocupación al 100%.  
- 🏥 **Reconstruye el nombre del hospital** desde columnas one-hot codificadas.  
- 📲 **Envía alertas automáticas por Telegram** cuando:
  - La **ocupación real ≥ 85%**.  
  - La **ocupación proyectada ≥ 95%**.  
- 🗂️ **Registra cada evento** en la hoja `alertas_log` con:
  - Timestamp  
  - Tipo de alerta  
  - Hospital  
  - Fecha  
  - Porcentaje de ocupación  
  - Estado de envío

---

### 💬 Ejemplo de Alerta

🚨 ALERTA REAL - 85%

🏥 Hospital: Central

📅 Fecha: 2025-10-28

💢 Ocupación total: 88.3%

<img width="1256" height="862" alt="Telegram" src="https://github.com/user-attachments/assets/f775ac35-9eb8-4df3-ae4c-ae6455364e05" />

---

## 🧰 Stack Tecnológico

| Tecnología | Uso principal |
|-------------|----------------|
| **Python** | Procesamiento, análisis y automatización |
| **Pandas** | Limpieza y manipulación de datos |
| **Google Drive API** | Descarga de archivos CSV |
| **Google Sheets API (GSpread)** | Actualización y lectura de hojas de cálculo |
| **Telegram Bot API** | Envío de alertas en tiempo real |
| **GitHub Actions** | Automatización diaria del pipeline |

---

## 🚀 Pipeline Automatizado

El flujo completo se ejecuta automáticamente mediante **GitHub Actions**, que orquesta ambos agentes en secuencia:

1. **Agente 1** → sincroniza datos desde Google Drive a Google Sheets.  
2. **Agente 2** → analiza la ocupación y envía alertas.  

Cada ejecución queda registrada en los logs de GitHub Actions y en la hoja `alertas_log`.

---

## Author
**Bárbara Ángeles Ortiz**

<img src="https://github.com/user-attachments/assets/30ea0d40-a7a9-4b19-a835-c474b5cc50fb" width="115">

[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | [GitHub](https://github.com/BarbaraAngelesOrtiz)

![Status](https://img.shields.io/badge/status-finished-brightgreen) 📅 Octubre 2025

![Python](https://img.shields.io/badge/Python-3.10-blue)
![GoogleAPI](https://img.shields.io/badge/Google_API-integrated-yellow)
![Telegram](https://img.shields.io/badge/Alerts-Telegram-blueviolet)
![GitHubActions](https://img.shields.io/badge/CI-GitHub_Actions-black)


