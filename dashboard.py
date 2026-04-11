import streamlit as st
import pandas as pd
import time
from bot.ai_engine import FinBERTEngine
from bot.client import BinanceFuturesClient
from bot.strategy import execute_sentiment_trade
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Crypto Trader", page_icon="📈", layout="wide")
st.title("🤖 AI-ML Algorithmic Trading Dashboard")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🔧 System Controls")
status_placeholder = st.sidebar.empty()
run_bot = st.sidebar.checkbox("Activate AI Trading Bot")

# --- SESSION STATE ---
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

# --- MAIN UI LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Live Market Sentiment Analysis")
    sentiment_display = st.empty()

with col2:
    st.subheader("💼 Active Positions & PnL")
    pnl_display = st.empty()

# --- BOT LOGIC LOOP ---
if run_bot:
    status_placeholder.success("BOT STATUS: ACTIVE")
    
    # Initialize Engines (Scrubbing keys from environment)
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY", "").strip().replace('"', '')
    api_secret = os.environ.get("BINANCE_TESTNET_SECRET", "").strip().replace('"', '')
    
    ai = FinBERTEngine()
    client = BinanceFuturesClient(api_key, api_secret)
    
    while run_bot:
        # 1. Fetch Headline (Using the logic from auto_trader)
        from auto_trader import fetch_latest_crypto_headline
        headline = fetch_latest_crypto_headline()
        
        # 2. AI Analysis
        sentiment = ai.analyze_headline(headline)
        
        # 3. Update UI
        with sentiment_display.container():
            st.info(f"**Scanning:** {headline}")
            st.metric(label="AI Confidence Score", value=f"{sentiment['score']:.2%}", 
                      delta=sentiment['label'].upper())
        
        # 4. Execute Trade logic
        try:
            order = execute_sentiment_trade(client, "BTCUSDT", sentiment, 0.01)
            if order:
                st.session_state.trade_history.append(order)
        except Exception as e:
            st.error(f"Trade Error: {e}")

        # Update History Table
        with pnl_display.container():
            if st.session_state.trade_history:
                st.table(pd.DataFrame(st.session_state.trade_history).tail(5))
            else:
                st.write("Waiting for first high-confidence signal...")

        time.sleep(30) # Refresh every 30 seconds for the UI
        st.rerun()
else:
    status_placeholder.error("BOT STATUS: OFFLINE")
