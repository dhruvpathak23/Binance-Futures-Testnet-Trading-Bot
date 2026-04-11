# 🤖 AI-ML Algorithmic Trading Bot (Binance Futures)

A professional-grade, autonomous trading system that leverages **NLP (Natural Language Processing)** to trade cryptocurrency futures based on real-time market sentiment. 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link.streamlit.app/)

## 🌟 Overview
This project integrates a **FinBERT Neural Network** with the **Binance Futures API** to automate trading decisions. Unlike traditional bots that rely solely on technical indicators (RSI, MACD), this system "reads" the news to gauge market psychology and executes trades with sub-second precision.

### 🧠 Key Features
* **Sentiment Analysis:** Uses `ProsusAI/finbert`, a specialized BERT model trained on financial data.
* **Autonomous Execution:** Automatically places Market Buy/Sell orders on high-confidence signals (>85%).
* **Risk Management:** Every trade is protected by automated **Take Profit (1%)** and **Stop Loss (0.5%)** orders.
* **Interactive Dashboard:** A live Streamlit UI providing real-time sentiment metrics and trade logs.
* **Secure Infrastructure:** Implements HMAC-SHA256 request signing and environment-based secret management.

---

## 🏗️ Project Structure
```text
├── .streamlit/          # Streamlit Cloud configuration
├── bot/                 # Core logic package
│   ├── ai_engine.py     # FinBERT model initialization & inference
│   ├── client.py        # Binance API wrapper & request signing
│   ├── orders.py        # Order placement functions (Market, TP/SL)
│   └── strategy.py      # Decision-making logic & risk ratios
├── dashboard.py         # Main Streamlit UI entry point
├── auto_trader.py       # CLI-based trading script
├── requirements.txt     # Dependency list
└── README.md            # Documentation
🛠️ Technical Implementation
1. NLP Inference
The bot utilizes the FinBERT transformer model. It classifies market headlines into three categories: Positive, Negative, and Neutral.

2. Cryptographic Signing
To interact with Binance, the bot generates a secure signature for every request using the HMAC-SHA256 algorithm. This ensures the integrity and authenticity of the trading commands.

3. Execution Pipeline
Scan: Pulls real-time crypto headlines.

Analyze: FinBERT returns sentiment labels and confidence scores.

Validate: Only triggers if confidence > 0.85.

Execute: Places a Market order and immediately hedges with TP/SL trigger orders.

🚀 Getting Started
Prerequisites
Python 3.11+

Binance Testnet API Keys

Installation
Clone the repository:

Bash
git clone [https://github.com/dhruvpathak23/Binance-Futures-Testnet-Trading-Bot.git](https://github.com/dhruvpathak23/Binance-Futures-Testnet-Trading-Bot.git)
Install dependencies:

Bash
pip install -r requirements.txt
Set your secrets in .streamlit/secrets.toml:

Ini, TOML
BINANCE_TESTNET_API_KEY = "your_key"
BINANCE_TESTNET_SECRET = "your_secret"
Run the dashboard:

Bash
streamlit run dashboard.py
💡 Technical Challenges Overcome
Subdomain Routing: Resolved conflicts between binance.vision (Key Authentication) and binancefuture.com (Futures Endpoints).

Data Sanitization: Implemented an aggressive scrubbing layer to prevent invisible characters in environment variables from corrupting HMAC signatures.

Resource Optimization: Utilized @st.cache_resource to keep the 400MB AI model in RAM, preventing UI lag during live market scans.

👨‍💻 Developer
Dhruv Pathak Final Semester B.Tech (CSE - AI & ML)

Disclaimer: This bot is for educational purposes and runs on the Binance Testnet. Trading involves significant risk.


---

### 🚀 What's next?
1. **Paste this** into your `README.md` file in VS Code.
2. **Push the change** to GitHub:
   ```bash
   git add README.md
   git commit -m "Update professional README with deployment info"
   git push origin main
