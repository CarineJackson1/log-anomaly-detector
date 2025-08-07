import json

report_path = "security-reports/summary_report.md"
badge_path = ".github/badges/security-badge.json"

high_count = 0

try:
    with open(report_path, "r") as file:
        for line in file:
            if "(Severity: HIGH)" in line:
                high_count += 1
except FileNotFoundError:
    pass

badge = {
    "schemaVersion": 1,
    "label": "security",
    "message": f"{high_count} high",
    "color": "green" if high_count == 0 else "red"
}

with open(badge_path, "w") as f:
    json.dump(badge, f)
