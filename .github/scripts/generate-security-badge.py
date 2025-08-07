import json
import os

# Path to your scan summary (from your Python report generator)
SUMMARY_PATH = "security-reports/summary_report.md"
OUTPUT_JSON = ".github/badges/security-badge.json"

# Define severity levels we want to count
def count_high_severity(summary_md):
    high_count = 0
    for line in summary_md.splitlines():
        if "Severity: HIGH" in line:
            high_count += 1
    return high_count

def determine_color(count):
    if count == 0:
        return "green"
    elif count <= 2:
        return "yellow"
    elif count <= 5:
        return "orange"
    else:
        return "red"

def main():
    if not os.path.exists(SUMMARY_PATH):
        print("Summary report not found.")
        return

    with open(SUMMARY_PATH, "r") as f:
        summary = f.read()

    high_issues = count_high_severity(summary)
    color = determine_color(high_issues)

    badge = {
        "schemaVersion": 1,
        "label": "security",
        "message": f"{high_issues} high issues",
        "color": color
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(badge, f, indent=2)

    print(f"Badge updated: {high_issues} high issues ({color})")

if __name__ == "__main__":
    main()
