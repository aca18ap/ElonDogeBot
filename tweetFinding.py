from bc import getAllCoins

coins = getAllCoins()

def elonParse(text):
    text = str(text).lower()
    if text.find("doge") != -1 or text.find("dogecoin") != -1:
        print(text.find("doge"))
        return 'DOGEUSDT'

    if text.find("btc") != -1 or text.find("bitcoin") != -1:
        return 'BTCUSDT'
    
    return None

def coinParse(text):
    text = text.upper()
    txt = text.split()
    for i in txt:
        if i[0] == '$' or i[0] == '#':
            i = i[1:]
        if i in coins:
            return i + 'USDT'
    return None

