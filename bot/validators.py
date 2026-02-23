def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be 'BUY' or 'SELL'.")
    if order_type.upper() not in ['MARKET', 'LIMIT']:
        raise ValueError("Order type must be 'MARKET' or 'LIMIT'.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    if order_type.upper() == 'LIMIT' and (price is None or price <= 0):
        raise ValueError("A valid positive price is required for LIMIT orders.")
    return True