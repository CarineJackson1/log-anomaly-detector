# 🖥 Log Analyzer

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/plotly-1f77b4?style=for-the-badge)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

---

## Overview

**Log Analyzer** is a Python-based security project designed to parse, analyze, and visualize system and web logs from multiple sources.  
It helps identify anomalies such as failed logins, suspicious IP activity, and potential security incidents, making it ideal for **SOC/incident response workflows**.

**Keywords:** Python, SOC, Anomaly Detection, Regex, Log Parsing, Visualization, Incident Response, Security Analytics

---

## Features

- Parses **Linux syslog**, **Windows Event Logs (CSV)**, and **Apache web server logs**
- Normalizes logs into a **common schema**: `timestamp`, `host`, `event_type`, `message`, `source`
- Detects **anomalies**:
  - Failed logins (Linux/Windows)
  - Suspicious IP activity (web server)
- Generates **interactive charts** using Plotly
- Saves **timestamped combined CSVs** to track analysis history

---

## Project Structure

log-analyzer/
├── log_analyzer_advanced.py   # Main Python script
├── data/
│   ├── sample_syslog.log
│   ├── sample_windows.csv
│   └── sample_apache.log
├── outputs/
│   ├── reports/               # Optional: anomaly reports
│   └── visualizations/        # Optional: Plotly charts
├── README.md
└── requirements.txt

---

## Demo

![Log Analyzer Demo](./github-readme-media/log_analyzer_demo.gif)

> The GIF above demonstrates parsing multiple log sources, detecting anomalies, and generating a visualization chart.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/CarineJackson1/log-anomaly-detector.git
cd log-analyzer

	2.	Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

	3.	Install dependencies:

pip install -r requirements.txt
```
⸻

Usage

python3 log_analyzer_advanced.py

	•	Combined logs are saved to ./data/combined_logs_<timestamp>.csv
	•	Detected anomalies are visualized in an interactive Plotly chart

⸻

Future Enhancements
	•	Auto-generate synthetic log entries for stress-testing
	•	Integrate firewall/IDS logs for extended SOC coverage
	•	Export anomaly reports as PDF/HTML
	•	Add real-time log monitoring dashboard using Dash or Plotly

⸻

License

MIT License

⸻

Author

Carine Jackson – LinkedIn | GitHub
