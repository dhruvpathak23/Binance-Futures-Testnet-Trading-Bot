import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import logging

logger = logging.getLogger('trading_bot')

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def post_order(self, params: dict) -> dict:
        endpoint = "/fapi/v1/order"
        params['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        logger.info(f"Sending POST request to {endpoint} with params: {params}")
        try:
            response = self.session.post(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get('msg', e.response.text)
            logger.error(f"HTTP Error: {error_msg}")
            raise Exception(f"API Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise Exception(f"Network Error: {str(e)}")