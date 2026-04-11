import os
import sys
import time
import logging
from bot.logging_config import setup_logger
from bot.client import BinanceFuturesClient
from bot.ai_engine import FinBERTEngine
from bot.strategy import execute_sentiment_trade

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
    
    # Secure Retrieval
    raw_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    raw_secret = os.environ.get("BINANCE_TESTNET_SECRET")
    
    if not raw_key or not raw_secret:
        logger.error("Missing API Keys. Ensure environment variables are set.")
        sys.exit(1)

    # SECURE SCRUBBING: Removes quotes, spaces, and newlines from PowerShell inputs
    api_key = raw_key.strip().replace('"', '').replace("'", "")
    api_secret = raw_secret.strip().replace('"', '').replace("'", "")

    client = BinanceFuturesClient(api_key, api_secret)
    ai = FinBERTEngine()
    
    symbol = "BTCUSDT"
    trade_quantity = 0.01

    logger.info(f"System armed. Monitoring {symbol}")
    
    try:
        while True:
            logger.info("--- Initiating Market Scan ---")
            
            headline = fetch_latest_crypto_headline()
            sentiment = ai.analyze_headline(headline)
            
            execute_sentiment_trade(client, symbol, sentiment, trade_quantity)
            
            logger.info("Sleeping for 15 minutes...\n")
            time.sleep(900) 
            
    except KeyboardInterrupt:
        logger.info("Manual shutdown triggered. Exiting.")

if __name__ == "__main__":
    main()