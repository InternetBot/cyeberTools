import subprocess
import json

def extract_windows_logs(log_type='System'):
    # Command to fetch the newest 50 logs from the specified log type and convert them to JSON format
    command = f"Get-EventLog -LogName {log_type} -Newest 50 | ConvertTo-Json"

    # Execute the command using PowerShell
    p = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE)

    # Wait for the command to complete and capture the output
    output, err = p.communicate()

    # Check if there was any output and return it as a JSON object; if not, return an empty list
    return json.loads(output.decode('utf-8')) if output else []

# Call the function to get the logs
logs = extract_windows_logs()

# Print the logs to a file with formatted JSON
with open('pc.json', 'w') as json_file:
    json.dump(logs, json_file, indent=4, ensure_ascii=False)

print("Logs have been written to pc.json")
