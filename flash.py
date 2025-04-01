from flask import Flask, jsonify
import MetaTrader5 as mt5

app = Flask(__name__)

def connect_mt5():
    if not mt5.initialize():
        return False
    return True

@app.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """Retorna o preço atual do ativo"""
    if not connect_mt5():
        return jsonify({"error": "Falha na conexão com MT5"}), 500
    
    tick = mt5.symbol_info_tick(symbol)
    return jsonify({"symbol": symbol, "bid": tick.bid, "ask": tick.ask})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
