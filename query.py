"""
@author: Robert Jones
"""
import sqlite3


def query(database_filename, ticker, time):
    """
    This module retrieves the information based on the given ticker name and timestamp (HH:MM)
    :param database_filename: name of the db file to read from
    :param ticker: name of the ticker to retrieve information of
    :param time: timestamp (HH:MM) of data to find
    :return:
    """

    data = [ticker, time]
    conn = sqlite3.connect(database_filename)

    c = conn.cursor()
    try:
        c.execute("SELECT * FROM StockData WHERE StockData.Ticker = ? AND StockData.Time = ?", data)
    except sqlite3.OperationalError:
        print("No matching table")
        return

    rows = c.fetchall()

    header = ['Time', 'Ticker', 'Low', 'High', 'Open', 'Close', 'Price', 'Volume']

    return_data = list(zip(header, rows[0]))

    for x in return_data:
        print(x[0], '\t:', x[1])

