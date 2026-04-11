import logging
from .orders import place_order, place_tp_sl_orders

logger = logging.getLogger('trading_bot')

def execute_sentiment_trade(client, symbol, sentiment_data, quantity):
    label = sentiment_data.get('label')
    confidence = sentiment_data.get('score', 0.0)
    
    if confidence < 0.85:
        logger.info(f"Low confidence ({confidence:.2f}). Holding.")
        return

    # 1. Execute the Entry Trade
    side = "BUY" if label == "positive" else "SELL"
    entry_response = place_order(client, symbol, side, "MARKET", quantity)
    
    if not entry_response:
        return

    # 2. Calculate TP/SL Prices
    # In a real bot, we'd fetch the current price from Binance. 
    # For now, we'll use the 'avgPrice' from the entry response.
    entry_price = float(entry_response.get('avgPrice', 0))
    if entry_price == 0: return

    # Risk Management Settings
    tp_percent = 0.01  # 1% Profit
    sl_percent = 0.005 # 0.5% Loss

    if side == "BUY":
        tp_price = round(entry_price * (1 + tp_percent), 2)
        sl_price = round(entry_price * (1 - sl_percent), 2)
        exit_side = "SELL"
    else:
        tp_price = round(entry_price * (1 - tp_percent), 2)
        sl_price = round(entry_price * (1 + sl_percent), 2)
        exit_side = "BUY"

    # 3. Place the Protection Orders
    logger.info(f"Setting TP at {tp_price} and SL at {sl_price}")
    place_tp_sl_orders(client, symbol, exit_side, tp_price, quantity) # Take Profit
    place_tp_sl_orders(client, symbol, exit_side, sl_price, quantity) # Stop Loss