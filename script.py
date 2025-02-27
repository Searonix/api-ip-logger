import requests
import os
import urllib3

urllib3.disable_warnings()

API_URL = "https://render-api-test-vdza.onrender.com/ips/ips"  # เปลี่ยนเป็น API จริง
DATA_FILE = "data.txt"

def fetch_api_data():
    response = requests.get(API_URL, verify=False)
    return response.json() if response.status_code == 200 else []

def load_existing_ips():
    return set(open(DATA_FILE).read().splitlines()) if os.path.exists(DATA_FILE) else set()

def save_new_ips(new_ips):
    with open(DATA_FILE, "a") as file:
        for ip in new_ips:
            if ip.strip():
                file.write(ip + "\n")
    print(f"✅ Added {len(new_ips)} new IPs")

def delta_query():
    existing_ips = load_existing_ips()
    fetched_ips = set(fetch_api_data())
    new_ips = fetched_ips - existing_ips
    if new_ips:
        save_new_ips(new_ips)
    else:
        print("✅ No new IPs found!")

if __name__ == "__main__":
    delta_query()
