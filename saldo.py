import MetaTrader5 as mt5

# Conectar ao MetaTrader 5
if not mt5.initialize():
    print("Erro ao conectar ao MT5")
    quit()

# Obter informações da conta
account_info = mt5.account_info()

if account_info:
    print(f"Saldo: {account_info.balance}")
    print(f"Capital Líquido: {account_info.equity}")
    print(f"Margem Livre: {account_info.margin_free}")
else:
    print("Não foi possível obter informações da conta.")

# Encerrar a conexão
mt5.shutdown()
