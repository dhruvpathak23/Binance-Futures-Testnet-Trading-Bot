import streamlit as st
import pandas as pd
import time
import os
import logging
from bot.ai_engine import FinBERTEngine
from bot.client import BinanceFuturesClient
from bot.strategy import execute_sentiment_trade

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Crypto Trader", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a sleek look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI-ML Algorithmic Trading Dashboard")
st.markdown("---")

# --- SIDEBAR: CONTROLS & STATUS ---
st.sidebar.header("🔧 System Controls")

# Activation Toggle
run_bot = st.sidebar.checkbox("Activate AI Trading Bot", value=False)

if run_bot:
    st.sidebar.success("BOT STATUS: RUNNING")
else:
    st.sidebar.error("BOT STATUS: OFFLINE")

st.sidebar.markdown("---")
st.sidebar.info("""
**Strategy:** FinBERT Sentiment  
**Asset:** BTCUSDT  
**Database:** Unified Testnet
""")

# --- STATE MANAGEMENT ---
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(message):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    # Keep only last 10 logs
    if len(st.session_state.logs) > 10:
        st.session_state.logs.pop(0)

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Live Market Monitor")
    sentiment_placeholder = st.empty()
    log_placeholder = st.expander("View System Logs", expanded=True)

with col2:
    st.subheader("💼 Trade Execution History")
    history_placeholder = st.empty()

# --- EXECUTION LOOP ---
if run_bot:
    # 1. KEY SANITIZATION PIPELINE
    # Fetch from environment
    raw_key = os.environ.get("BINANCE_TESTNET_API_KEY", "")
    raw_secret = os.environ.get("BINANCE_TESTNET_SECRET", "")
    
    # Aggressive cleaning (removes spaces, single quotes, and double quotes)
    api_key = str(raw_key).strip().replace("'", "").replace('"', "").replace(" ", "")
    api_secret = str(raw_secret).strip().replace("'", "").replace('"', "").replace(" ", "")

    if not api_key or not api_secret:
        st.error("❌ API Keys missing! Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET in your terminal.")
        st.stop()

    # 2. INITIALIZE ENGINES
    try:
        # We cache the AI engine to prevent reloading on every loop
        @st.cache_resource
        def load_ai():
            return FinBERTEngine()
        
        ai = load_ai()
        client = BinanceFuturesClient(api_key, api_secret)
        
        # 3. CONTINUOUS SCANNING
        while run_bot:
            from auto_trader import fetch_latest_crypto_headline
            headline = fetch_latest_crypto_headline()
            
            # AI Analysis
            sentiment = ai.analyze_headline(headline)
            label = sentiment['label'].upper()
            score = sentiment['score']
            
            # Update Sentiment UI
            with sentiment_placeholder.container():
                st.info(f"**Current Headline:** {headline}")
                s_col1, s_col2 = st.columns(2)
                s_col1.metric("Sentiment", label)
                s_col2.metric("AI Confidence", f"{score:.2%}")
            
            # Trade Logic
            try:
                order = execute_sentiment_trade(client, "BTCUSDT", sentiment, 0.01)
                if order:
                    st.session_state.trade_history.append({
                        "Time": time.strftime("%H:%M:%S"),
                        "Symbol": "BTCUSDT",
                        "Order ID": order.get('orderId'),
                        "Status": "FILLED"
                    })
                    st.toast(f"✅ Trade Success! ID: {order.get('orderId')}", icon='🚀')
                    add_log(f"SUCCESS: Order {order.get('orderId')} placed.")
                else:
                    add_log(f"SCAN: Sentiment {label} ({score:.2f}) below threshold.")
            
            except Exception as e:
                error_msg = str(e)
                st.error(f"Execution Error: {error_msg}")
                add_log(f"ERROR: {error_msg}")

            # Update Log UI
            with log_placeholder:
                st.text("\n".join(st.session_state.logs[::-1]))

            # Update History Table
            with history_placeholder.container():
                if st.session_state.trade_history:
                    df = pd.DataFrame(st.session_state.trade_history)
                    st.dataframe(df.tail(10), use_container_width=True)
                else:
                    st.write("No trades executed in this session.")

            time.sleep(15) # Scan every 15 seconds
            st.rerun()

    except Exception as e:
        st.error(f"Critical System Failure: {e}")