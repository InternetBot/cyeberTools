import requests
from html import unescape
import re
import json
import csv

def fetch_vulnerabilities(keyword, results_per_page=20):
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        'keywordSearch': keyword,
        'resultsPerPage': results_per_page
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    vulnerabilities = data.get('vulnerabilities', [])
    return vulnerabilities

def clean_html(raw_html):
    clean_text = re.sub('<.*?>', '', raw_html)
    return unescape(clean_text)

def save_results(vulnerabilities, filename, format_type):
    if format_type == 'json':
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(vulnerabilities, f, indent=4)
    elif format_type == 'txt':
        with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
            for vuln in vulnerabilities:
                f.write(f"CVE ID: {vuln['cve']['id']}\n")
                f.write(f"Description: {clean_html(vuln['cve']['descriptions'][0]['value'])}\n\n")
    elif format_type == 'csv':
        with open(f"{filename}.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['CVE ID', 'Description'])
            for vuln in vulnerabilities:
                writer.writerow([vuln['cve']['id'], clean_html(vuln['cve']['descriptions'][0]['value'])])

def main():
    while True:
        print("#############################################################################")
        print("# I recommend you know the exact name of the vulnerability you looking for  #")
        print("#           For example \"CVE-2021-34527\" for a more accurate result         #")
        print("#                          PRESS 0 to Exit Script                           #")
        print("#############################################################################")
        keyword = input("Enter the keyword to search vulnerabilities for: ")
        if keyword == '0':
            break

        vulnerabilities = fetch_vulnerabilities(keyword)
        
        if not vulnerabilities:
            print("Match not found for the provided keyword.")
        else:
            print(f"Total vulnerabilities fetched: {len(vulnerabilities)}\n")
            for vuln in vulnerabilities:
                print(f"CVE ID: {vuln['cve']['id']}")
                print(f"Description: {clean_html(vuln['cve']['descriptions'][0]['value'])}\n")
            
            if input("Do you want to save these results? (yes/no): ").lower() == 'yes':
                print("")
                filename = input("Enter filename: ")
                format_type = input("Choose the format (json/txt/csv): ").lower()
                save_results(vulnerabilities, filename, format_type)
                print("")
                print(f"Data saved to {filename}.{format_type}")
                print("")

if __name__ == '__main__':
    main()
