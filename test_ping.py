import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

# Hardcoding the exact keys from your screenshot
API_KEY = "OQmynjjFiJMp1Y43Zcf4ERhXooFtsYDcJiYTps1pYwswFTFMNhusGj9I2NXBXhKu"
API_SECRET = "u7a9Q0iECw2cYDXNSIdTy3WuxgzMGcyQ2FK6ddsjvYX3eN94lN0YL4rHpuwOLTnX"

def diagnose_connection(base_url):
    endpoint = "/fapi/v1/order"
    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 0.01,
        "recvWindow": 60000,
        "timestamp": int(time.time() * 1000)
    }
    
    clean_params = {k: str(v) for k, v in params.items()}
    query_string = urlencode(clean_params)
    
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    
    print(f"--- Pinging {base_url} ---")
    response = requests.post(url, headers={"X-MBX-APIKEY": API_KEY})
    
    if response.status_code == 200:
        print("[SUCCESS] Trade Executed! This is the correct database.")
    else:
        print(f"[FAILED] HTTP {response.status_code}: {response.text}")
    print("-" * 50 + "\n")

print("Initiating Diagnostic Test...\n")
diagnose_connection("https://testnet.binancefuture.com")
diagnose_connection("https://testnet.binance.vision")