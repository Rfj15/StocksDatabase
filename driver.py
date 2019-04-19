"""
@author: Robert Jones
"""

from stock import save_tickers
from stock import fetch_all_data
from stock import query

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--operation')
parser.add_argument('--ticker_count', type=int, default=1)
parser.add_argument('--time_limit', type=int, default=60)
parser.add_argument('--db', default="stocks_new.db")
parser.add_argument('--time')
parser.add_argument('--ticker', default="YI")

args = parser.parse_args()

if args.operation == 'Ticker':
    save_tickers(args.ticker_count, "tickers.txt")

elif args.operation == 'Fetcher':
    fetch_all_data("tickers.txt", args.ticker_count, args.time_limit, args.db)

elif args.operation == 'Query':
    query(args.db, args.ticker, args.time)
