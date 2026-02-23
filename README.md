# Binance Futures Testnet Trading Bot

Hi! This is my submission for the Python Developer Intern application task. I've built a lightweight CLI trading bot in Python that places Market and Limit orders on the Binance Futures Testnet (USDT-M). 

## How to Set It Up

To get this running locally, you'll need Python 3 installed. 

1. **Clone the repo and enter the directory:**
   ```bash
   git clone [https://github.com/dhruvpathak23/binance-futures-testnet-bot.git](https://github.com/dhruvpathak23/binance-futures-testnet-bot.git)
   cd binance-futures-testnet-bot

   # Create a virtual environment and install dependencies (requests):

   python -m venv venv

# On Windows: 
'''bash
venv\Scripts\activate

# On Mac/Linux: 
'''bash
source venv/bin/activate

pip install -r requirements.txt



# Place a MARKET Buy Order:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Place a LIMIT Sell Order:
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 100000

# Some Notes & Assumptions
While building and testing this, I handled a few interesting edge cases to make sure the app was robust:

Binance's Testnet URL Change: Binance recently deprecated the old testnet.binancefuture.com URL mentioned in the assignment. To ensure the bot actually executes successfully on their current infrastructure, I configured the base API URL to point to their active unified Demo environment: https://demo-fapi.binance.com.

Fixing Signature Rejections: I noticed that passing a Python dictionary directly into requests.post() occasionally triggered -1022 INVALID_SIGNATURE errors from Binance. This happens because the requests library can silently re-encode float values or reorder keys behind the scenes before sending the payload over the network. To make the bot bulletproof, I engineered the client to construct a raw x-www-form-urlencoded string and send that instead, ensuring the server receives the exact string used to calculate the HMAC signature.

Limit Orders: I assumed all Limit orders should be "Good Till Canceled", so my code automatically attaches the timeInForce="GTC" parameter whenever a limit order is routed to the client.
