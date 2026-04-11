import argparse
import os
import sys
from bot.logging_config import setup_logger
from bot.client import BinanceFuturesClient
from bot.validators import validate_order_input
from bot.orders import place_order

def main():
    logger = setup_logger()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot (Manual Override)")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=['BUY', 'SELL', 'buy', 'sell'], help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, choices=['MARKET', 'LIMIT', 'market', 'limit'], dest="order_type", help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price (required if type is LIMIT)", default=None)
    
    args = parser.parse_args()
    
    # --- SECURE API KEY HANDLING ---
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_SECRET")
    
    if not api_key or not api_secret:
        print("CRITICAL ERROR: API keys missing.")
        print("Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET as environment variables.")
        sys.exit(1)

    print(f"\n--- Manual Order Request Summary ---")
    print(f"Symbol: {args.symbol.upper()}")
    print(f"Side: {args.side.upper()}")
    print(f"Type: {args.order_type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.order_type.upper() == 'LIMIT':
        print(f"Price: {args.price}")
    print("------------------------------------\n")

    try:
        validate_order_input(args.symbol, args.side, args.order_type, args.quantity, args.price)
        client = BinanceFuturesClient(api_key, api_secret)
        response = place_order(client, args.symbol, args.side, args.order_type, args.quantity, args.price)
        
        print("[SUCCESS] Manual Order placed successfully!\n")
        print(f"Order ID: {response.get('orderId')}")
        
    except Exception as e:
        print(f"[FAILURE] Failed to place manual order.")
        print(f"Reason: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
