import json
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from decimal import Decimal
from datetime import datetime
from usr import getBinanceKeys, getPushKey
from pushbullet import Pushbullet
import sys

api_key = getBinanceKeys().get('api_key')
api_secret = getBinanceKeys().get('secret_key')

client = Client(api_key, api_secret)

info = client.futures_exchange_info()
symbols_n_precision = {}

pbKey = getPushKey().get('api_key')
pb = Pushbullet(pbKey)


for item in info['symbols']:
    symbols_n_precision[item['symbol']] = item['quantityPrecision'] 


def findPrice(coin):
    prices = client.get_all_tickers()
    for item in prices:
        if item.get('symbol') == coin:
            print(item.get('price'))
            return item.get('price')


def tradeFutures(leverage, coin, size, percentage_increase):
    try:
        ##gets current futures mark price slightly increased and rounds it do 6dp
        price = round(float((client.futures_mark_price(symbol = coin)).get('markPrice')),6)

        ##amount of coins to be bought based on leverage and margin size
        trade_size = size * leverage
        
        lvg = leverage
        sym = coin
        
        ##amount of coins over current price
        order_amount = trade_size/price
        precision = symbols_n_precision[sym]

        ##binance is picky so gets precision from its database
        precise_order_amount = "{:0.0{}f}".format(order_amount, precision)

        ##setting leverage
        client.futures_change_leverage(symbol = sym, leverage = lvg)
        
        ##stop price, change .XX for the percentage desired
        takeProfit = round(float("{:0.0{}f}".format((price * (1 + percentage_increase/100)), precision)),6)
        stopLoss = round(float("{:0.0{}f}".format((price * 0.9990), precision)),6)
    
        

        ##Creating 3 futures orders
        ##Buying at current price the specified amount
        client.futures_create_order(symbol = sym, type = 'MARKET', side='BUY', quantity=precise_order_amount)

        ##Setting take profit at stop price calculated earlier
        client.futures_create_order(symbol = sym, type = 'TAKE_PROFIT_MARKET', side ='SELL', stopPrice = takeProfit, closePosition = 'true')

        ##Adding a stop loss order just below entry to avoid big losses
        client.futures_create_order(symbol = sym, type = 'STOP_MARKET', side ='SELL', stopPrice = stopLoss, closePosition = 'true')

        push = pb.push_note("ELON DOGE BOT", "Currency: " + str(sym) + '\n' + "Price: " + str(price) + '\n' + "TP/SL: " + str(takeProfit) + '/' + str(stopLoss) )
        printTrade(size, takeProfit, lvg, sym, precise_order_amount, price, trade_size, stopLoss)


    except BinanceAPIException as err:
        print("Something went wrong with your trade, it may have still been partially completed though")
        print(err)
    except:
        print(sys.exc_info()[0])
        print("Something went wrong, python stuff")



##Prints trade details
def printTrade(margin, takeProfit, leverage, coin, trueSize, price, trade_size, stopLoss):
    print(takeProfit, price, trueSize)
    pnl = (float(takeProfit) - float(price)) * float(trueSize)
    roe = round(pnl/margin*100,2)
    print("COIN PAIR = ", coin)
    print("COIN PRICE = ", price)
    print("TAKE PROFIT = ", takeProfit)
    print("STOP LOSS = ", stopLoss)
    print("LEVERAGE = x" + str(leverage) )
    print("MARGIN = ", str(margin) + '$')
    print("COIN AMOUNT = ", str(trueSize) + '₿')
    print("PREDICTED ROE = ", str(roe) + '%')
    print("PREDICTED PROFIT = ", str(pnl))


##returns list of all coins tradeable in futures
def getAllCoins():
    coinPairs = []
    for items in (info['symbols']):
        coinPairs.append(items.get('symbol'))

    coins = [x[:-4] for x in coinPairs]
    return coins

def getMaxLeverage(coin):
    for i in info['symbols']:
        if i.get('symbol') == coin:
            print(i)

def elonTrigger(coin):
    print("Elon has spoken")
    if coin == 'DOGEUSDT':
        print("About to trade the mighty shiba")
        tradeFutures(50, coin, 30, 8)
    ##else:
      ##  print("Moving fat markets on btc")
        ##tradeFutures(50, coin, 10, 3)

def wizardTrigger(coin):
    print("Wizard has spoken, looking at 3% profit")
    tradeFutures(50, coin, 10, 3)

def testTrigger(coin):
    print("Just a test call")
    tradeFutures(20, coin, 10, 1)

def worthInvesting(username, coin):
    if username == 'elonmusk':
        elonTrigger(coin)
    elif username == 'piaalbi':
        testTrigger(coin)
    else:
        wizardTrigger(coin)

