# trading_logic.py
from oandapyV20.endpoints.orders import OrderCreate
from oanda_api import OandaAPI
from oandapyV20.endpoints.orders import Orders
from oandapyV20.endpoints.orders import OrdersPending
# from oandapyV20.types import  StopLossOrderRequest, TakeProfitOrderRequest

oanda = OandaAPI()

def calculate_trade_parameters(candle):
    # Simplified example logic; replace with your actual strategy
    bid_open = float(candle['bids'][0]['price'])  # Opening price (simulated)
    ask_close = float(candle['asks'][0]['price'])  # Closing price (simulated)
    
    previous_candle_range = bid_open - ask_close
    sl_tp_ratio = 2
    
    stop_loss_buy = bid_open - previous_candle_range
    stop_loss_sell = ask_close + previous_candle_range
    
    take_profit_buy = bid_open + previous_candle_range * sl_tp_ratio
    take_profit_sell = ask_close - previous_candle_range * sl_tp_ratio
    
    return stop_loss_buy, stop_loss_sell, take_profit_buy, take_profit_sell


from oandapyV20.endpoints.orders import OrderCreate
from oanda_api import OandaAPI

oanda = OandaAPI()

def place_order(instrument, units, stop_loss, take_profit, direction="buy"):
    # Construct the order data directly as a dictionary
    order_data = {
        "order": {
            "instrument": instrument,
            "units": str(units) if direction == "buy" else str(-units),
            "timeInForce": "FOK",  # Fill-Or-Kill: the order must be filled immediately or canceled
            "type": "MARKET",
            "positionFill": "DEFAULT",  # Use this for market orders
            "stopLossOnFill": {
                "price": str(stop_loss),
                "timeInForce": "GTC"  # Good 'Til Canceled
            },
            "takeProfitOnFill": {
                "price": str(take_profit),
                "timeInForce": "GTC"  # Good 'Til Canceled
            }
        }
    }
    
    # Create the order request
    order_request = OrderCreate(accountID=oanda.account_id, data=order_data)
    response = oanda.client.request(order_request)
    return response

def execute_trade(instrument, units):
    # Fetch the latest candle to base our decision on
    price_data = oanda.get_price(instrument)
    print(f"Price Data ====== {price_data}")
    current_candle = price_data['prices'][0]
    print(f"Current Candle = {current_candle}")
    stop_loss_buy, stop_loss_sell, take_profit_buy, take_profit_sell = calculate_trade_parameters(current_candle)

    print("stop_loss_buy: ", stop_loss_buy)
    print("stop_loss_sell: ", stop_loss_sell)
    print("take_profit_buy: ", take_profit_buy)
    print("take_profit_sell: ", take_profit_sell)    
    place_order(instrument, units, stop_loss_buy, take_profit_buy, direction="buy")
    
    # place_order(instrument, units, stop_loss_sell, take_profit_sell, direction="sell")

    return price_data

    
    # if signal == 1:  # Sell Signal
    #     return place_order(instrument, units, stop_loss_sell, take_profit_sell, direction="sell")
    # elif signal == 2:  # Buy Signal
    #     return place_order(instrument, units, stop_loss_buy, take_profit_buy, direction="buy")
    # else:
    #     return {"error": "Invalid signal"}



def get_orders():
    orders_request = Orders(accountID=oanda.account_id)
    response = oanda.client.request(orders_request)
    return response

def get_pending_orders():
    pending_orders_request = OrdersPending(accountID=oanda.account_id)
    response = oanda.client.request(pending_orders_request)
    return response
