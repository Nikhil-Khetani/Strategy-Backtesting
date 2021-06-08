import pandas_datareader.data as web
import datetime
import pandas as pd
import re



class Portfolio(object):
    def __init__(self, cash, tickers, start, end):
        super().__init__()
        self.cash = cash
        self.tickers = []
        self.assets = {re.sub('=', '', i):Asset(i, start, end) for i in tickers}
        for i in tickers:
            self.tickers.append(re.sub('=', '', i))
        self.tradeable_dates = list(pd.date_range(start,end))
        for i in self.tickers:
            self.tradeable_dates = list(set(self.tradeable_dates).intersection(set(self.assets[i].data.index)))

    def update_prices(self,date):
        for i in self.tickers:
            self.assets[i].update_price(date)
    
    def rebalance(self, percent_cash, **kwargs):
        
        self.value = self.cash +  sum([self.assets[i].holding*self.assets[i].price for i in self.tickers])

        if percent_cash+sum(kwargs.values()) != 100:
            print('Weights do not add up to 100')
            return
        for ticker in self.tickers:
            self.cash = self.value
            self.assets[ticker].holding = 0

        for ticker, weight in kwargs.items():
            self.assets[ticker].holding = self.value*weight/(100*self.assets[ticker].price)
            self.cash -= self.assets[ticker].holding*self.assets[ticker].price
    
    def print_holdings(self):
        print('Total Value: {}'.format(self.cash +  sum([self.assets[i].holding*self.assets[i].price for i in self.tickers])))
        print('Cash: {}'.format(self.cash))
        for ticker in self.tickers:
            print('{} holding: {}, price: £{}, value: £{}'.format(ticker, self.assets[ticker].holding, self.assets[ticker].price, self.assets[ticker].holding*self.assets[ticker].price))
            

class Asset():
    def __init__(self, ticker, start, end):
        super().__init__()
        self.holding = 0
        self.data = web.DataReader(ticker, 'yahoo', start, end) #.reset_index(level=0)
    
    def update_price(self, date):
        self.price = self.data['Adj Close'][str(date)]
        return




class Strategy():
    def __init__(self, portfolio):
        super().__init__()
        self.port = portfolio

    def trading_strategy(self):
        
        self.port.rebalance(percent_cash=75, JPYGBPX=-25, TSLA=50)

        return

    def backtest(self, start, end):
        for date in self.port.tradeable_dates:
            if date>start and date<end:
                print(date)
                
        return



if __name__ == '__main__':
    start = datetime.datetime(2011, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    tickers = ['JPYGBP=X', 'TSLA']

    port = Portfolio(cash=10000, tickers=tickers, start=start, end=end)
    
    print(port.assets['JPYGBPX'].data)
    port.update_prices(datetime.datetime(2020,1,31))

    port.rebalance(percent_cash=75, JPYGBPX=-25, TSLA=50)
    port.update_prices(datetime.datetime(2020,2,28))
    port.print_holdings()


