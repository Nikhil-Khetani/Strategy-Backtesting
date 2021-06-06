import pandas_datareader.data as web
import datetime
import pandas as pd



class Portfolio(object):
    def __init__(self, cash, tickers, start, end):
        super().__init__()
        self.cash = cash
        self.tickers = tickers
        self.assets = {i:Asset(i, start, end) for i in tickers}

    def update_prices(self,date):
        for i in tickers:
            self.assets[i].update_price(date)
    
    def rebalance(self, percent_cash, **kwargs):
        self.value = cash +  sum([self.assets[i].holding*self.assets[i].price for i in self.tickers])
        for key, weight in kwargs.items():
            self.assets[key].holding = self.value*weight/(100*self.assets[key].price)



class Asset():
    def __init__(self, ticker, start, end):
        super().__init__()
        self.holding = 0
        self.data = web.DataReader(ticker, 'yahoo', start, end).reset_index(level=0)
    
    def update_price(self, date):

        return





class Strategy():
    def __init__(self, portfolio):
        super().__init__()
        self.port = portfolio

    def trading_strategy(self):
        self.port.rebalance()
        return

    def backtest(self, start, end):
        return


if __name__ == '__main__':
    start = datetime.datetime(2011, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    tickers = ['GBPJPY=X']
    port = Portfolio(cash=10000, tickers=tickers, start=start, end=end)
    

    print(port.assets[0].data)