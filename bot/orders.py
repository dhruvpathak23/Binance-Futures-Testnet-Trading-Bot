from .client import BinanceFuturesClient
import logging

logger = logging.getLogger('trading_bot')

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }
    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"
        
    logger.info(f"Attempting to place {order_type} {side} order for {quantity} {symbol}")
    return client.post_order(params)