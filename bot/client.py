import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import logging

logger = logging.getLogger('trading_bot')

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        # 1. Using the dedicated Futures Testnet endpoint
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        
        self.session.headers.update({
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
        
        params['recvWindow'] = 60000
        params['timestamp'] = int(time.time() * 1000)
        
        # Clean and sort params for signature consistency
        clean_params = {k: str(v) for k, v in params.items() if v is not None}
        query_string = urlencode(clean_params)
        signature = self._generate_signature(query_string)
        
        # Construct the final URL with the signature
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        logger.info(f"Submitting order to Futures Testnet...")
        try:
            # We use an empty POST body because the signature is in the URL
            response = self.session.post(url, timeout=10)
            
            # This check prevents the 'Expecting value' error by showing the real error
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_detail = response.json().get('msg', response.text)
                except: pass
                logger.error(f"Binance rejected trade: {error_detail}")
                raise Exception(f"API Error: {error_detail}")

            data = response.json()
            logger.info(f"TRADE SUCCESSFUL: {data.get('orderId')}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection Error: {e}")
            raise Exception(f"Network Error: {str(e)}")