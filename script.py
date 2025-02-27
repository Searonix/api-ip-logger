import requests
import os
import urllib3

urllib3.disable_warnings()

API_URL = "https://render-api-test-vdza.onrender.com/ips"  # ตรวจสอบว่า URL ถูกต้อง
DATA_FILE = "data.txt"

def fetch_api_data():
    response = requests.get(API_URL, verify=False)
    print(f"🔍 API Response Code: {response.status_code}")
    print(f"🔍 API Data: {response.text}")

    if response.status_code == 200:
        try:
            raw_ips = response.json()
            clean_ips = {ip.strip() for ip in raw_ips if ip.strip()}  # 🔹 ลบค่าว่าง
            return clean_ips
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
            return set()
    return set()

def load_existing_ips():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return set(file.read().splitlines())  # โหลดเป็นเซ็ต
    return set()

def save_new_ips(new_ips):
    all_ips = load_existing_ips() | new_ips  # รวม IP เก่ากับใหม่

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)  # ลบไฟล์เดิมก่อน

    with open(DATA_FILE, "w") as file:
        for ip in sorted(all_ips):
            if ip.strip():  # 🔹 ป้องกันการเขียนค่าว่างลงไฟล์
                file.write(ip.strip() + "\n")

    print(f"✅ Updated {len(new_ips)} new IPs, total {len(all_ips)} IPs recorded.")

def delta_query():
    existing_ips = load_existing_ips()
    fetched_ips = fetch_api_data()

    if not fetched_ips:
        print("⚠️ No data fetched from API!")
        return

    new_ips = fetched_ips - existing_ips

    if new_ips:
        save_new_ips(new_ips)
    else:
        print("✅ No new IPs found!")

if __name__ == "__main__":
    delta_query()
