import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import logging

logger = logging.getLogger('trading_bot')

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://demo-fapi.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        
        # Set Content-Type explicitly so Binance knows we are sending a raw form string
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "X-MBX-APIKEY": self.api_key
        })

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def post_order(self, params: dict) -> dict:
        endpoint = "/fapi/v1/order"
        
        # 1. Add required safety parameters (recvWindow prevents timeout rejections)
        params['recvWindow'] = 60000
        params['timestamp'] = int(time.time() * 1000)
        
        # 2. Force convert all values to strings to prevent Python float formatting issues
        clean_params = {k: str(v) for k, v in params.items() if v is not None}
        
        # 3. Create the exact query string
        query_string = urlencode(clean_params)
        
        # 4. Generate the signature based on that exact string
        signature = self._generate_signature(query_string)
        
        # 5. Create the raw payload string.
        # Passing a raw string prevents the `requests` library from re-ordering 
        # or re-encoding the data behind the scenes.
        raw_payload = f"{query_string}&signature={signature}"
        url = f"{self.base_url}{endpoint}"
        
        logger.info(f"Sending POST request to {endpoint} with raw payload: {raw_payload}")
        try:
            # Send the raw string directly instead of a dictionary
            response = self.session.post(url, data=raw_payload)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API Response: {data}")
            return data
            
        except requests.exceptions.HTTPError as e:
            try:
                error_msg = e.response.json().get('msg', e.response.text)
            except Exception:
                error_msg = e.response.text
            logger.error(f"HTTP Error: {error_msg}")
            raise Exception(f"API Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise Exception(f"Network Error: {str(e)}")