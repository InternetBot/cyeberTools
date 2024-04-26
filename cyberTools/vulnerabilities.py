"""
This code gets list of all vulnerabilities on nist.gov and stores in a json file 
"""
import requests
import json

def fetch_all_vulnerabilities(keyword, results_per_page=20):
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    all_vulnerabilities = []
    start_index = 0

    while True:
        params = {
            'keywordSearch': keyword,
            'resultsPerPage': results_per_page,
            'startIndex': start_index
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Ensure the request succeeded
        data = response.json()

        # Accessing the list of vulnerabilities
        vulnerabilities = data.get('vulnerabilities', [])
        all_vulnerabilities.extend(vulnerabilities)

        # Break the loop if the number of results returned is less than requested (last page)
        if len(vulnerabilities) < results_per_page:
            break

        # Update start_index to fetch the next page
        start_index += results_per_page

    return all_vulnerabilities

# Usage example
keyword = "Windows"
vulnerabilities = fetch_all_vulnerabilities(keyword)
print(f"Total vulnerabilities fetched: {len(vulnerabilities)}")

# Optionally, save to a JSON file
with open('all_vulnerabilities.json', 'w', encoding='utf-8') as file:
    json.dump(vulnerabilities, file, indent=4, ensure_ascii=False)
