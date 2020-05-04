#!/usr/bin/env python

import os
import sys
import logging
import json
import binance
from binance.error import APIException, BinanceException

logging.basicConfig(level=logging.INFO)

logging.info("reading key and secrect from env")

try:
    os.environ["KEY"] or os.environ["SECRET"]
except KeyError:
    logging.error("please set KEY and SECRET")
    sys.exit(1)

key = os.environ['KEY']
secret = os.environ['SECRET']

base_url='https://testnet.binance.vision'

test_client = binance.Market(base_url=base_url)

response = test_client.exchange_info()

symbols = []
for symbol in response['symbols']:
    s = {}
    s['symbol'] = symbol['symbol']
    symbols.append(s)

# client connect to production
client = binance.Market()
for symbol in symbols:
    ticker = client.ticker_price(symbol['symbol'])
    logging.info('getting ticker for {}'.format(symbol['symbol']))
    symbol['price'] = ticker['price']

test_client = binance.Trade(key, secret, base_url=base_url)

logging.info('start to place orders')

def place_order(symbol, side,  price, qty):
    sell_params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': qty,
        'price': price
    }

    test_client.new_order(**sell_params)

for symbol in symbols:
    logging.info('placeing buy order for: {}'.format(symbol['symbol']))
    qty = 1

    try:
        place_order(symbol['symbol'], 'BUY',  symbol['price'], 1)
    except APIException as error:
        logging.error('seeing error when placing order')
        logging.error('retry by increase the qty ')
        place_order(symbol['symbol'], 'BUY',  symbol['price'], 10000)

    logging.info('placeing sell order for: {}'.format(symbol['symbol']))

    try:
        place_order(symbol['symbol'], 'SELL',  symbol['price'], 1)
    except APIException as error:
        logging.error('seeing error when placing order')
        logging.error('retry by increase the qty ')
        place_order(symbol['symbol'], 'SELL',  symbol['price'], 10000)

logging.info('validating trades for all pairs')

for symbol in symbols:
    trades = test_client.my_trades(symbol['symbol'])
    logging.info("symbol: " + symbol['symbol'] + " has trades: "  + str(len(trades)))
