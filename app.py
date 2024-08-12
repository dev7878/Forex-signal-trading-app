# app.py
from flask import Flask, jsonify
from oanda_api import OandaAPI

app = Flask(__name__)
oanda = OandaAPI()

@app.route('/price/<instrument>', methods=['GET'])
def get_price(instrument):
    try:
        price_data = oanda.get_price(instrument)
        return jsonify(price_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
