import logging
from transformers import pipeline

logger = logging.getLogger('trading_bot')

class FinBERTEngine:
    def __init__(self):
        logger.info("Initializing FinBERT Neural Network...")
        # Using ProsusAI's specialized financial model
        self.analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        logger.info("FinBERT Model loaded and ready.")

    def analyze_headline(self, text: str) -> dict:
        try:
            result = self.analyzer(text)[0]
            logger.info(f"Analyzed: '{text}' | Sentiment: {result['label'].upper()} | Confidence: {result['score']:.4f}")
            return result
        except Exception as e:
            logger.error(f"NLP Engine Failure: {e}")
            return {'label': 'neutral', 'score': 0.0}
