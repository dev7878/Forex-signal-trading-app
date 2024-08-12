# oanda_api.py
from oandapyV20.endpoints.pricing import PricingInfo
from config import Config
import oandapyV20

class OandaAPI:
    def __init__(self):
        self.client = oandapyV20.API(access_token=Config.OANDA_API_KEY)
        self.account_id = Config.OANDA_ACCOUNT_ID

    def get_price(self, instrument):
        params = {
            "instruments": instrument
        }
        r = PricingInfo(accountID=self.account_id, params=params)
        response = self.client.request(r)
        return response
