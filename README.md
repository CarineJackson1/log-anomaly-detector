# 🖥 Log Analyzer

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-1f77b4?style=for-the-badge)

---

## 🔹 Overview

**Log Analyzer** is a Python project for parsing, analyzing, and visualizing system and web logs.  
It helps **detect anomalies**, such as failed logins and suspicious IP activity, making it perfect for **SOC-style incident response workflows**.  

**Keywords:** Python, SOC, Anomaly Detection, Log Parsing, Regex, Visualization, Incident Response

---

## ✨ Features

- ✅ Parse **Linux Syslog**, **Windows Event Logs (CSV)**, and **Apache Web Logs**  
- ✅ Normalize logs into a **common schema**: `timestamp`, `host`, `event_type`, `message`, `source`  
- ✅ Detect anomalies:  
  - Failed logins (Linux/Windows)  
  - Suspicious IP activity (Web Server)  
- ✅ Interactive **Plotly charts** for visualization  
- ✅ Timestamped CSV exports for historical tracking  

---

## 📂 Project Structure

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

## 🎬 Demo

![Log Analyzer Demo](./github-readme-media/log_analyzer_demo.gif)

> Parsing logs → detecting anomalies → visualizing results in real-time.

---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/CarineJackson1/log-anomaly-detector.git
cd log-analyzer

	2.	Create a virtual environment:

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

	3.	Install dependencies:

pip install -r requirements.txt


⸻

python3 log_analyzer_advanced.py
```


🚀 Usage
	•	Combined logs saved to ./data/combined_logs_<timestamp>.csv
	•	Anomalies visualized in an interactive Plotly chart

⸻

💡 Future Enhancements
	•	Auto-generate synthetic log entries for stress-testing
	•	Integrate firewall/IDS logs for extended SOC coverage
	•	Export anomaly reports as PDF/HTML
	•	Build real-time dashboards using Dash/Plotly

⸻

📄 License

MIT License

⸻

👩‍💻 Author

Carine Jackson – LinkedIn | GitHub
