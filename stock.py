"""
@author: Robert Jones
"""

import sqlite3
import requests
import time
import datetime


def save_tickers(num_tickers, filename):
    """
    :param num_tickers: number of tickers to save
    :param filename: file to store ticker names
    :return: none
    """
    from lxml import html
    page = requests.get('https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=150')
    tree = html.fromstring(page.content)
    companies = tree.xpath('//*[@id="CompanylistResults"]/tr/td[2]/h3/a/text()')
    companies = [x.strip() for x in companies]
    file = open(filename, 'w')
    for company in companies[:num_tickers]:
        file.write(company)
        file.write('\n')

    file.close()


def fetch_all_data(ticker_filename, num_tickers, time_limit, database_filename):
    """
    :param ticker_filename: filename of tickers to read from
    :param num_tickers: number of tickers to fetch
    :param time_limit: time (seconds) allocated to fetch date
    :param database_filename: name of database file to write to
    :return: none
    """

    from iex import Stock

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


def query(database_filename, ticker, time):
    """
    :param database_filename: name of database file to read from
    :param ticker: name of ticker we are indexing
    :param time: timestamp that we are indexing
    :return: none
    """
    data = [ticker, time]
    conn = sqlite3.connect(database_filename)

    c = conn.cursor()
    try:
        c.execute("SELECT * FROM StockData WHERE StockData.Ticker = ? AND StockData.Time = ?", data)
    except sqlite3.OperationalError:
        print("No matching table")

    rows = c.fetchall()

    header = ['Time', 'Ticker', 'Low', 'High', 'Open', 'Close', 'Price', 'Volume']

    try:
        return_data = list(zip(header, rows[0]))

        for x in return_data:
            print(x[0], '\t:', x[1])

    except IndexError:
        print("Data error")
