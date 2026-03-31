import os, time, logging, requests

API_URL = os.getenv("API_BASE_URL")
LIMIT = 10000
MAX_RETRIES = 3

def fetch_crime_data():
    all_records, offset = [], 0
    while True:
        params = {"$limit": LIMIT, "$offset": offset}
        for attempt in range(MAX_RETRIES):
            try:
                r = requests.get(API_URL, params=params, timeout=10)
                r.raise_for_status()
                data = r.json()
                if not data:
                    return all_records
                all_records.extend(data)
                offset += LIMIT
                break
            except Exception:
                time.sleep(2**attempt)
        else:
            break
    return all_records
