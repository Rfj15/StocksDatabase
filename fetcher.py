"""
@author: Robert Jones
"""
from iex import Stock
import time
import datetime
import sqlite3


def fetch_all_data(ticker_filename, num_tickers, time_limit, database_filename):
    """
    This module fetches the data of the tickers in "tickers.txt" and writes them to a database
    :param ticker_filename: the filename where the tickers are stored
    :param num_tickers: the number of tickers to fetch
    :param time_limit: amount of time (in seconds) to update database
    :param database_filename: name of db to store data
    :return: success or failure
    """
    tickers = open(ticker_filename, 'r')
    curr_time = datetime.datetime.now().strftime('%H:%M')
    conn = sqlite3.connect(database_filename)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS StockData("
              "`Time` VARCHAR(45) NOT NULL,"
              "`Ticker` VARCHAR(45) NOT NULL,"
              "`Low` INT NOT NULL,"
              "`High` INT NOT NULL,"
              "`Open` INT NOT NULL,"
              "`Close` INT NOT NULL,"
              "`Price` INT NOT NULL,"
              "`Volume` INT NOT NULL,"
              "UNIQUE ('Ticker'),"
              "PRIMARY KEY (`Ticker`, 'Time'))")
    minutes = time_limit / 60
    counter = 0
    while counter < minutes:
        if counter > 0:
            time.sleep(60)
        for line in tickers:
            line = line.strip()
            try:
                stock = Stock(line).quote()
                data = [curr_time, stock['symbol'], stock['low'], stock['high'], stock['open'],
                        stock['close'], stock['latestPrice'], stock['latestVolume']]
                c.execute('INSERT OR REPLACE INTO StockData VALUES(?,?,?,?,?,?,?,?)', data)
                conn.commit()
            except BaseException:
                print('No entry made')
        counter = counter + 1
