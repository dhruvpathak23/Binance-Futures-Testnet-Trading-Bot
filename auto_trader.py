import os
import sys
import time
import logging
from bot.logging_config import setup_logger
from bot.client import BinanceFuturesClient
from bot.ai_engine import FinBERTEngine
from bot.strategy import execute_sentiment_trade

# For demonstration, we use a mock news fetcher. 
# You can replace this with requests.get() to a real News API later.
def fetch_latest_crypto_headline():
    import random
    headlines = [
        "Bitcoin ETF approved by SEC, massive institutional inflows expected.",
        "Major crypto exchange hacked, millions stolen in security breach.",
        "Markets trade sideways as investors await inflation data.",
        "Ethereum network upgrade reduces gas fees significantly, driving adoption."
    ]
    return random.choice(headlines)

def main():
    logger = setup_logger()
    logger.info("=== Starting AI Automated Trading System ===")
    
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_SECRET")
    
    if not api_key or not api_secret:
        logger.error("Missing API Keys in environment. Shutting down.")
        sys.exit(1)

    client = BinanceFuturesClient(api_key, api_secret)
    ai = FinBERTEngine()
    
    symbol = "BTCUSDT"
    trade_quantity = 0.01

    logger.info(f"System armed. Monitoring {symbol} with trade size {trade_quantity}")
    
    try:
        while True:
            logger.info("--- Initiating Market Scan ---")
            
            # 1. Fetch News
            headline = fetch_latest_crypto_headline()
            
            # 2. Analyze Sentiment
            sentiment = ai.analyze_headline(headline)
            
            # 3. Execute Strategy
            execute_sentiment_trade(client, symbol, sentiment, trade_quantity)
            
            # Wait 15 minutes before checking the news again
            logger.info("Sleeping for 15 minutes...\n")
            time.sleep(900) 
            
    except KeyboardInterrupt:
        logger.info("Manual shutdown triggered. Exiting AI Auto-Trader.")

if __name__ == "__main__":
    main()
