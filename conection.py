import MetaTrader5 as mt5
import time
import pandas as pd

# Configurações do robô
SYMBOL = "EURUSD"   # Ativo negociado
VOLUME = 0.1        # Lote padrão
SL_PIPS = 50        # Stop Loss (pips)
TP_PIPS = 100       # Take Profit (pips)
TIMEFRAME = mt5.TIMEFRAME_M5  # Período de 5 minutos

def connect_mt5():
    """Inicia conexão com MetaTrader 5."""
    if not mt5.initialize():
        print("Falha ao conectar ao MT5")
        return False
    return True

def get_ma(symbol, period, shift):
    """Obtém o valor da Média Móvel Simples."""
    rates = mt5.copy_rates_from_pos(symbol, TIMEFRAME, 0, period + shift)
    if rates is None:
        return None
    df = pd.DataFrame(rates)
    return df['close'].rolling(period).mean().iloc[-1]

def place_order(order_type):
    """Envia ordem de compra ou venda."""
    price = mt5.symbol_info_tick(SYMBOL).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(SYMBOL).bid
    deviation = 10  # Tolerância de variação de preço
    sl = price - SL_PIPS * 0.0001 if order_type == mt5.ORDER_TYPE_BUY else price + SL_PIPS * 0.0001
    tp = price + TP_PIPS * 0.0001 if order_type == mt5.ORDER_TYPE_BUY else price - TP_PIPS * 0.0001

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": VOLUME,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 123456,
        "comment": "Robo Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    order_result = mt5.order_send(request)
    return order_result

def trade_logic():
    """Executa a estratégia de cruzamento de médias móveis."""
    ma9 = get_ma(SYMBOL, 9, 0)
    ma21 = get_ma(SYMBOL, 21, 0)

    if ma9 is None or ma21 is None:
        print("Erro ao obter médias móveis")
        return

    open_orders = mt5.positions_get(symbol=SYMBOL)
    
    if ma9 > ma21 and not any(order.type == mt5.ORDER_TYPE_BUY for order in open_orders):
        print("Sinal de Compra - Executando ordem")
        place_order(mt5.ORDER_TYPE_BUY)
    
    elif ma9 < ma21 and not any(order.type == mt5.ORDER_TYPE_SELL for order in open_orders):
        print("Sinal de Venda - Executando ordem")
        place_order(mt5.ORDER_TYPE_SELL)

def main():
    """Loop principal do robô"""
    if not connect_mt5():
        return
    
    print("Robô iniciado. Monitorando o mercado...")
    while True:
        trade_logic()
        time.sleep(60)  # Executa a cada 60 segundos

if __name__ == "__main__":
    main()
