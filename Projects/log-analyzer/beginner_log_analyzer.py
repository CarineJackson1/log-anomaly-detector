# beginner_log_analyzer.py
# A simple security log analyzer for beginners
# This tool helps you find suspicious activity in log files

print("🔍 Starting Security Log Analyzer...")
print("=" * 50)

# Step 1: Read a simple log file
def read_log_file(filename):
    """
    Reads a log file and returns each line as a list
    Think of this as opening a book and reading each page
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        print(f"✅ Successfully read {len(lines)} lines from {filename}")
        return lines
    except FileNotFoundError:
        print(f"❌ Could not find file: {filename}")
        return []

# Step 2: Look for suspicious words/phrases
def find_suspicious_activity(log_lines):
    """
    Looks through all log lines for scary words that might mean trouble
    Like a word search puzzle, but for security threats!
    """
    # These are words that usually mean something bad happened
    bad_words = [
        'failed', 'error', 'unauthorized', 'denied', 'blocked',
        'attack', 'intrusion', 'malware', 'virus', 'hack'
    ]
    
    suspicious_logs = []
    
    for line_number, line in enumerate(log_lines, 1):
        # Check if any bad words are in this line
        for bad_word in bad_words:
            if bad_word.lower() in line.lower():
                suspicious_logs.append({
                    'line_number': line_number,
                    'found_word': bad_word,
                    'full_line': line.strip()
                })
                break  # Found one bad word, move to next line
    
    return suspicious_logs

# Step 3: Count how many times each IP address appears
def count_ip_addresses(log_lines):
    """
    Counts how many times we see each IP address
    If one IP shows up too much, it might be suspicious!
    """
    import re
    
    # This pattern finds IP addresses (like 192.168.1.1)
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ip_counts = {}
    
    for line in log_lines:
        # Find all IP addresses in this line
        ips = re.findall(ip_pattern, line)
        for ip in ips:
            if ip in ip_counts:
                ip_counts[ip] += 1
            else:
                ip_counts[ip] = 1
    
    return ip_counts

# Step 4: Create a simple report
def create_report(suspicious_logs, ip_counts):
    """
    Makes a nice, easy-to-read report of what we found
    """
    print("\n📋 SECURITY ANALYSIS REPORT")
    print("=" * 50)
    
    # Report suspicious activities
    print(f"\n🚨 SUSPICIOUS ACTIVITIES FOUND: {len(suspicious_logs)}")
    if suspicious_logs:
        print("\nTop 5 most concerning entries:")
        for i, log in enumerate(suspicious_logs[:5], 1):
            print(f"{i}. Line {log['line_number']}: Found '{log['found_word']}'")
            print(f"   Full line: {log['full_line'][:80]}...")
            print()
    else:
        print("✅ No suspicious keywords found!")
    
    # Report IP addresses
    print(f"\n🌐 IP ADDRESS ANALYSIS:")
    if ip_counts:
        # Sort IPs by how many times they appear (most first)
        sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        
        print("Top 5 most active IP addresses:")
        for i, (ip, count) in enumerate(sorted_ips[:5], 1):
            status = "🚨 VERY SUSPICIOUS" if count > 10 else "⚠️ Watch this one" if count > 5 else "✅ Normal"
            print(f"{i}. {ip}: {count} times - {status}")
    else:
        print("No IP addresses found in logs")

# Step 5: Main program (this runs everything)
def main():
    """
    The main function that runs our security analysis
    """
    # Ask user for the log file name
    print("Please put your log file in the same folder as this script")
    filename = input("Enter the name of your log file (e.g., 'security.log'): ")
    
    # Step 1: Read the file
    log_lines = read_log_file(filename)
    if not log_lines:
        print("❌ Cannot continue without a valid log file")
        return
    
    # Step 2: Look for suspicious stuff
    print("\n🔍 Searching for suspicious activities...")
    suspicious_logs = find_suspicious_activity(log_lines)
    
    # Step 3: Count IP addresses
    print("🔍 Analyzing IP addresses...")
    ip_counts = count_ip_addresses(log_lines)
    
    # Step 4: Make the report
    create_report(suspicious_logs, ip_counts)
    
    # Save results to a file
    print(f"\n💾 Saving detailed results to 'security_report.txt'...")
    with open('security_report.txt', 'w') as report_file:
        report_file.write("SECURITY ANALYSIS REPORT\n")
        report_file.write("=" * 50 + "\n\n")
        
        report_file.write(f"SUSPICIOUS ACTIVITIES ({len(suspicious_logs)} found):\n")
        for log in suspicious_logs:
            report_file.write(f"Line {log['line_number']}: {log['full_line']}\n")
        
        report_file.write(f"\nIP ADDRESS COUNTS:\n")
        for ip, count in ip_counts.items():
            report_file.write(f"{ip}: {count} times\n")
    
    print("✅ Report saved! Check 'security_report.txt' for full details")
    print("\n🎉 Analysis complete!")

# This runs the program when you double-click the file
if __name__ == "__main__":
    main()


# BONUS: Sample log creator (if you don't have a log file to test with)
def create_sample_log():
    """
    Creates a sample log file for testing
    Run this first if you don't have a real log file
    """
    sample_logs = [
        "2024-01-15 10:30:15 192.168.1.100 User login successful",
        "2024-01-15 10:31:22 192.168.1.101 Failed login attempt for user admin",
        "2024-01-15 10:31:45 192.168.1.101 Failed login attempt for user admin",
        "2024-01-15 10:32:10 192.168.1.101 Failed login attempt for user admin",
        "2024-01-15 10:35:30 192.168.1.102 File download completed successfully",
        "2024-01-15 10:40:15 192.168.1.103 Unauthorized access attempt detected",
        "2024-01-15 10:45:20 192.168.1.101 Account blocked due to multiple failed attempts",
        "2024-01-15 11:00:00 192.168.1.104 Normal user activity",
        "2024-01-15 11:15:30 10.0.0.50 Potential malware detected in file",
        "2024-01-15 11:20:45 10.0.0.50 Virus scan completed - threat removed"
    ]
    
    with open('sample_security.log', 'w') as f:
        for log in sample_logs:
            f.write(log + '\n')
    
    print("✅ Created 'sample_security.log' for testing!")

# Uncomment the line below to create a sample log file:
# create_sample_log()
