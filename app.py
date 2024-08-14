# app.py
from flask import Flask, jsonify, request
from trading_logic import execute_trade, get_orders, get_pending_orders

app = Flask(__name__)

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()

    print(data)

    instrument = data["instrument"]
    units = data["units"]
    print(instrument)
    # units = data.get('units', 1000)
    trade_response = execute_trade(instrument, units)
    # return jsonify(data)
    return jsonify(trade_response)

@app.route('/orders', methods=['GET'])
def orders():
    orders_response = get_orders()
    return jsonify(orders_response)

@app.route('/pending_orders', methods=['GET'])
def pending_orders():
    pending_orders_response = get_pending_orders()
    return jsonify(pending_orders_response)

# @app.route('/cancel_order/<order_id>', methods=['DELETE'])
# def cancel_order_route(order_id):
#     cancel_order_response = cancel_order(order_id)
#     return jsonify(cancel_order_response)

if __name__ == '__main__':
    app.run(debug=True)
