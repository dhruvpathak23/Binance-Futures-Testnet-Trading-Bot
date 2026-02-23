# Binance Futures Testnet Trading Bot

A Python CLI application to place Market and Limit orders on the Binance Futures Testnet (USDT-M).

## Setup Steps

1. Clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   * **Note on API Endpoint:** Binance recently deprecated the old `testnet.binancefuture.com` environment and now redirects users to their unified Demo Trading platform. Consequently, this bot uses the updated active base URL (`https://demo-fapi.binance.com`) as required by the current Binance testing infrastructure.