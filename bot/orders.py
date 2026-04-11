import logging

logger = logging.getLogger('trading_bot')

def place_order(client, symbol, side, order_type, quantity, price=None):
    """
    Standard Market or Limit order for entering a position.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    if order_type.upper() == "LIMIT" and price:
        params["price"] = price
        params["timeInForce"] = "GTC"

    try:
        return client.post_order(params)
    except Exception as e:
        logger.error(f"Failed to place {side} {order_type} order: {e}")
        return None

def place_tp_sl_orders(client, symbol, side, stop_price, quantity):
    """
    Special Trigger orders for Take Profit and Stop Loss.
    Uses 'reduceOnly' to ensure it only closes existing positions.
    """
    # Decide order type based on the price direction
    # side: SELL for long exit, BUY for short exit
    order_type = "STOP_MARKET" 
    
    # We use STOP_MARKET for both, but we label them clearly in logs
    # Note: Binance Futures uses 'stopPrice' for these triggers
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "stopPrice": stop_price,
        "quantity": quantity,
        "reduceOnly": "true" 
    }
    
    try:
        logger.info(f"Submitting {side} {order_type} at {stop_price}")
        return client.post_order(params)
    except Exception as e:
        logger.error(f"Failed to place TP/SL order: {e}")
        return None