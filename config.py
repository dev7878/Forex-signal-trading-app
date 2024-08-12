# config.py
import configparser

class Config:
    config = configparser.ConfigParser()
    config.read('config.cfg')

    OANDA_API_KEY = config['OANDA']['API_KEY']
    OANDA_ACCOUNT_ID = config['OANDA']['ACCOUNT_ID']

# For debugging purposes, you can add print statements to ensure values are loaded correctly
print(f"API_KEY: {Config.OANDA_API_KEY}")
print(f"ACCOUNT_ID: {Config.OANDA_ACCOUNT_ID}")
