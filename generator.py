#!/usr/bin/env python

import os
import sys
import logging
import json
from binance.spot import Spot
from binance.error import ClientError, Error

logging.basicConfig(level=logging.INFO)

logging.info("reading key and secrect from env")

try:
    os.environ["KEY"] or os.environ["SECRET"]
except KeyError:
    logging.error("please set KEY and SECRET")
    sys.exit(1)

key = os.environ['KEY']
secret = os.environ['SECRET']

base_url = 'https://testnet.binance.vision'

test_client = Spot(key=key, secret=secret, base_url=base_url)

response = test_client.exchange_info()

symbols = []
for symbol in response['symbols']:
    s = {}
    s['symbol'] = symbol['symbol']
    symbols.append(s)

# client connect to production
prod_client = Spot()
for symbol in symbols:
    ticker = prod_client.ticker_price(symbol['symbol'])
    logging.info('getting ticker for {}'.format(symbol['symbol']))
    symbol['price'] = ticker['price']

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
    try:
        test_client.new_order(**sell_params)
    except ClientError as error:
        logging.error('seeing error when placing order')
        logging.error(error)
        logging.error(symbol)


for symbol in symbols:
    qty = 1
    if (symbol['symbol'].startswith('XRP') or symbol['symbol'].startswith('TRX')):
        qty = 1000
    logging.info('placeing buy order for: {}'.format(symbol['symbol']))
    place_order(symbol['symbol'], 'BUY',  symbol['price'], qty)
    logging.info('placeing sell order for: {}'.format(symbol['symbol']))
    place_order(symbol['symbol'], 'SELL',  symbol['price'], qty)

logging.info('validating trades for all pairs')

for symbol in symbols:
    trades = test_client.my_trades(symbol['symbol'])
    logging.info("symbol: " + symbol['symbol'] + " has trades: " + str(len(trades)))
