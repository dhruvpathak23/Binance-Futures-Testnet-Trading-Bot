import logging

def setup_logger():
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)
    
    # File handler for detailed logs
    fh = logging.FileHandler('trading_bot.log')
    fh.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
        
    return logger