import MetaTrader5 as mt5
import time
import pandas as pd

# Configuração do robô
PAR_MOEDA = "EURUSD"
PERIODO = mt5.TIMEFRAME_M1  # 1 Minuto
LOTE = 0.1
SL = 50  # Stop Loss (em pontos)
TP = 100  # Take Profit (em pontos)

# Inicializar conexão com MetaTrader 5
if not mt5.initialize():
    print("Erro ao conectar ao MT5")
    quit()

# Função para obter dados do mercado
def obter_dados():
    barras = mt5.copy_rates_from_pos(PAR_MOEDA, PERIODO, 0, 50)
    df = pd.DataFrame(barras)
    df["media_movel"] = df["close"].rolling(10).mean()
    return df

# Função para abrir ordens
def abrir_ordem(tipo):
    preco = mt5.symbol_info_tick(PAR_MOEDA).ask if tipo == "buy" else mt5.symbol_info_tick(PAR_MOEDA).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": PAR_MOEDA,
        "volume": LOTE,
        "type": mt5.ORDER_TYPE_BUY if tipo == "buy" else mt5.ORDER_TYPE_SELL,
        "price": preco,
        "sl": preco - SL * mt5.symbol_info(PAR_MOEDA).point if tipo == "buy" else preco + SL * mt5.symbol_info(PAR_MOEDA).point,
        "tp": preco + TP * mt5.symbol_info(PAR_MOEDA).point if tipo == "buy" else preco - TP * mt5.symbol_info(PAR_MOEDA).point,
        "deviation": 10,
        "magic": 123456,
        "comment": "Robo MT5",
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    resultado = mt5.order_send(request)
    print("Ordem enviada!", resultado)

# Loop principal do robô
print("Robô iniciado. Monitorando o mercado...")
while True:
    df = obter_dados()
    
    if df["close"].iloc[-1] > df["media_movel"].iloc[-1]:
        print("Sinal de Compra - Executando ordem")
        abrir_ordem("buy")
    elif df["close"].iloc[-1] < df["media_movel"].iloc[-1]:
        print("Sinal de Venda - Executando ordem")
        abrir_ordem("sell")
    
    time.sleep(60)  # Espera 1 minuto antes de verificar novamente
