# log_analyzer_advanced.py
import pandas as pd
import re
import os
import plotly.express as px

# ----------------------------
# 1. Log Parsers (same as before)
# ----------------------------
def parse_syslog(file_path):
    pattern = r'(?P<timestamp>\w+ \d+ \d+:\d+:\d+) (?P<host>\S+) (?P<process>\S+): (?P<message>.*)'
    logs = []
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                logs.append(match.groupdict())
    df = pd.DataFrame(logs)
    df['source'] = 'Linux Syslog'
    df['event_type'] = df['process']
    return df[['timestamp','host','event_type','message','source']]

def parse_windows_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns={
        'TimeGenerated': 'timestamp',
        'ComputerName': 'host',
        'EventType': 'event_type',
        'Message': 'message'
    })
    df['source'] = 'Windows Event Log'
    return df[['timestamp','host','event_type','message','source']]

def parse_apache(file_path):
    pattern = r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] "(?P<request>.*?)" (?P<status>\d{3}) (?P<size>\d+)'
    logs = []
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                logs.append(match.groupdict())
    df = pd.DataFrame(logs)
    df['host'] = df['ip']
    df['event_type'] = 'web_request'
    df['message'] = df['request']
    df['source'] = 'Apache Web Log'
    return df[['timestamp','host','event_type','message','source']]

# ----------------------------
# 2. Combine Logs
# ----------------------------
def combine_logs(log_paths):
    combined = pd.DataFrame()
    for path, parser in log_paths:
        if os.path.exists(path):
            df = parser(path)
            combined = pd.concat([combined, df], ignore_index=True)
        else:
            print(f"[!] File not found: {path}")
    return combined

# ----------------------------
# 3. Basic Anomaly Detection
# ----------------------------
def detect_anomalies(df):
    anomalies = pd.DataFrame()
    
    # Linux failed logins
    failed_login_mask = df['message'].str.contains('failed password', case=False, na=False)
    failed_logins = df[failed_login_mask].copy()
    failed_logins['alert'] = 'Failed Login'
    
    # Multiple hits from same IP in web logs
    web_requests = df[df['source']=='Apache Web Log']
    ip_counts = web_requests['host'].value_counts()
    suspicious_ips = ip_counts[ip_counts > 50].index  # threshold example
    brute_force_attempts = web_requests[web_requests['host'].isin(suspicious_ips)].copy()
    brute_force_attempts['alert'] = 'Suspicious IP Activity'
    
    anomalies = pd.concat([failed_logins, brute_force_attempts])
    return anomalies

# ----------------------------
# 4. Visualization
# ----------------------------
def visualize_anomalies(anomalies):
    if anomalies.empty:
        print("[+] No anomalies detected.")
        return
    
    fig = px.histogram(
        anomalies, 
        x='host', 
        color='alert',
        title='Detected Security Anomalies by Host/IP',
        labels={'host':'Host/IP','alert':'Anomaly Type'},
        height=500
    )
    fig.show()

# ----------------------------
# 5. Main Execution
# ----------------------------
if __name__ == "__main__":
    log_files = [
        ('./data/sample_syslog.log', parse_syslog),
        ('./data/sample_windows.csv', parse_windows_csv),
        ('./data/sample_apache.log', parse_apache)
    ]
    
    all_logs = combine_logs(log_files)
    print(f"[+] Combined {len(all_logs)} log entries from {len(log_files)} sources")
    
    all_logs.to_csv('./data/combined_logs.csv', index=False)
    print("[+] Saved combined logs to ./data/combined_logs.csv")
    
    anomalies = detect_anomalies(all_logs)
    print(f"[+] Detected {len(anomalies)} anomalies")
    
    visualize_anomalies(anomalies)
