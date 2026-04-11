import logging

def setup_logger():
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)

    # File handler for permanent record
    fh = logging.FileHandler('trading_bot.log')
    fh.setLevel(logging.INFO)

    # Formatter for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        
        # --- NEW: Console handler for live AI monitoring ---
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
