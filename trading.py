import pandas_datareader.data as web
import datetime



class Portfolio(object):
    def __init__(self, cash, tickers, start, end):
        super().__init__()
        self.cash = cash
        self.tickers = tickers
        self.assets = [Asset(i, start, end) for i in tickers]

class Asset():
    def __init__(self, ticker, start, end):
        super().__init__()
        self.holding = 0
        self.data = web.DataReader(ticker, 'yahoo', start, end).reset_index(level=0)




class Strategy():
    def __init__(self, portfolio):
        super().__init__()
        self.port = portfolio


if __name__ == '__main__':
    start = datetime.datetime(2011, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    tickers = ['GBPJPY=X']

    port = Portfolio(cash=10000, tickers=tickers, start=start, end=end)

    print(port.assets[0].data)