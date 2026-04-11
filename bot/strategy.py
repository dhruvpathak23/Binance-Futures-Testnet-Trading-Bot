import logging
from .client import BinanceFuturesClient
from .orders import place_order

logger = logging.getLogger('trading_bot')

def execute_sentiment_trade(client: BinanceFuturesClient, symbol: str, sentiment_data: dict, quantity: float):
    label = sentiment_data.get('label')
    confidence = sentiment_data.get('score', 0.0)
    
    # Strict risk management: Only trade if FinBERT is >85% confident
    CONFIDENCE_THRESHOLD = 0.85 

    if confidence < CONFIDENCE_THRESHOLD:
        logger.info(f"AI Confidence ({confidence:.2f}) below threshold. Holding position.")
        return None

    try:
        if label == 'positive':
            logger.info(f"STRONG BULLISH SIGNAL. Executing LONG on {symbol}.")
            return place_order(client, symbol, "BUY", "MARKET", quantity)
            
        elif label == 'negative':
            logger.info(f"STRONG BEARISH SIGNAL. Executing SHORT on {symbol}.")
            return place_order(client, symbol, "SELL", "MARKET", quantity)
            
        else:
            logger.info("Market sentiment neutral. No action taken.")
            return None
            
    except Exception as e:
        logger.error(f"Strategy execution failed: {e}")
