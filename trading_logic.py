# trading_logic.py
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.types import StopLossDetails, TakeProfitDetails
from oanda_api import OandaAPI

oanda = OandaAPI()

def calculate_trade_parameters(candle):
    # Example logic based on your notebook
    previous_candleR = float(str(candle['bid']['o'])) - float(str(candle['bid']['c']))
    SLTPRatio = 2
    
    SLBuy = float(str(candle['bid']['o'])) - previous_candleR
    SLSell = float(str(candle['bid']['o'])) + previous_candleR
    
    TPBuy = float(str(candle['bid']['o'])) + previous_candleR * SLTPRatio
    TPSell = float(str(candle['bid']['o'])) - previous_candleR * SLTPRatio
    
    return SLBuy, SLSell, TPBuy, TPSell

def place_order(instrument, units, stop_loss, take_profit, direction="buy"):
    mo = OrderCreate(
        accountID=oanda.account_id,
        data={
            "order": {
                "units": str(units),
                "instrument": instrument,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT",
                "stopLossOnFill": StopLossDetails(price=stop_loss).data,
                "takeProfitOnFill": TakeProfitDetails(price=take_profit).data
            }
        }
    )
    if direction == "sell":
        mo.data['order']['units'] = str(-units)
    response = oanda.client.request(mo)
    return response

def execute_trade(instrument="EUR_USD", units=1000, signal=2):
    price_data = oanda.get_price(instrument)
    current_candle = price_data['prices'][0]
    
    SLBuy, SLSell, TPBuy, TPSell = calculate_trade_parameters(current_candle)
    
    if signal == 1:  # Sell Signal
        return place_order(instrument, units, stop_loss=SLSell, take_profit=TPSell, direction="sell")
    elif signal == 2:  # Buy Signal
        return place_order(instrument, units, stop_loss=SLBuy, take_profit=TPBuy, direction="buy")
    e
