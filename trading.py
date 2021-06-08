import pandas_datareader.data as web
import datetime
import pandas as pd
import re
import matplotlib.pyplot as plt


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
        self.tradeable_dates.sort()

    def update_prices(self,date):
        for i in self.tickers:
            self.assets[i].update_price(date)
    
    def rebalance(self, percent_cash=None, **kwargs):

        if int(percent_cash+sum(kwargs.values())) != 100:
            print('Weights do not add up to 100')
            return
        val=self.value()
        self.cash = val
        for ticker in self.tickers:
            self.assets[ticker].holding = 0

        for ticker, weight in kwargs.items():
            self.assets[ticker].holding = val*weight/(100*self.assets[ticker].price)
            self.cash -= self.assets[ticker].holding*self.assets[ticker].price
    
    def print_holdings(self):
        print('Total Value: {}'.format(self.cash +  sum([self.assets[i].holding*self.assets[i].price for i in self.tickers])))
        print('Cash: {}'.format(self.cash))
        for ticker in self.tickers:
            print('{} holding: {}, price: £{}, value: £{}'.format(ticker, self.assets[ticker].holding, self.assets[ticker].price, self.assets[ticker].holding*self.assets[ticker].price))
    
    def value(self):
        return self.cash +  sum([self.assets[i].holding*self.assets[i].price for i in self.tickers])

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

    def trading_strategy(self, date):
        self.port.update_prices(date)
        weights = {}
        cash_weight = 0
        for i in self.port.tickers:
            if self.port.assets[i].data['Adj Close'][date] > self.port.assets[i].data['Adj Close'].iloc[self.port.tradeable_dates.index(date)-10]:
                weights[i] = 1
            else:
                weights[i] = 0.5
                cash_weight += 0.5
        
        normalisation_factor = 100/(sum(weights.values())+cash_weight)
        cash_weight *= normalisation_factor
        for k in weights:
            weights[k] = weights[k]*normalisation_factor
            
        if True:
            self.port.rebalance(percent_cash = cash_weight, **weights)
            print('Trade')
        return cash_weight, weights

    def backtest(self, start, end):
        date_range=[]
        port_value=[]
        percent_change = [0]
        
        for date in self.port.tradeable_dates:
            if date>start and date<end:
                cash_weight, weights=self.trading_strategy(date)
                date_range.append(date)
                port_value.append(self.port.value())
                print(cash_weight)
                print(weights)

        for i in range(len(port_value)-1):
            percent_change.append((port_value[i+1]/port_value[i])-1)
            

        plt.scatter(date_range,port_value)
        plt.show()
        plt.scatter(date_range,percent_change)
        plt.show()
        return



if __name__ == '__main__':
    start = datetime.datetime(2011, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    tickers = ['SQQQ', 'TSLA']

    port = Portfolio(cash=10000, tickers=tickers, start=start, end=end)
    


    strat = Strategy(port)

    strat.backtest(datetime.datetime(2019, 1, 1),datetime.datetime(2021, 1, 31))
    port.print_holdings()

