'''Portfolio Analysis using Sharpe's Ratio for Machine Learning for Trading Udacity Course'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def test_run():
    #Pre-defined symbols for portfolio analysis
    symbols = ['SPY','AAPL', 'GLD', 'GOOG']
    symbol_print = print_symbols(symbols)

    #Get dates for portfolio analysis
    #dates = get_dates()
    dates = ['2017-07-25','2016-07-28']
    dates=pd.date_range(dates[0],dates[1])
    
    #Create empty dataframe using user-provided date range
    df=pd.DataFrame(index=dates)
    
    #Get stock allocations
    symbol_allocs, allocs = get_allocations(symbols)
    
    #Load stock data from CSV files provided
    df=load_stocks(df,symbols)
    total_investment = get_total_investment()
    df_portfolio = get_portfolio(df,symbols,allocs,total_investment)

    #Compute and print portfolio's cumulative returns and sharpe_ratio
    cumulative_returns = compute_cumulative_returns(allocs,df,total_investment)
    sharpe_ratio = compute_sharpe_ratio(allocs,df,total_investment)
    print "Portfolio's cumulative returns: {}\nPortfolio's Sharpe ratio: {}".format(cumulative_returns,sharpe_ratio)
    plot_data(df_portfolio,normal=True)
    

'''Function that reads in and prints the dates for stock analysis'''
def get_dates():
    dates = []
    for i in range(2):
        date_type = str('Starting Date: ' if i == 0 else 'Ending Date: ')
        print '\nInput ' + date_type
        temp_year = str(input('Enter the year (YYYY): '))
        temp_month = str(input('Enter the month (MM): '))
        temp_day = str(input('Enter the day (DD): '))
        date = temp_year + '-' + temp_month + '-' + temp_day
        dates.append(date)
        print date_type + date
    dates=pd.date_range(dates[0],dates[1])
    return dates

'''Function to load all given stocks into Pandas dataframe'''
def load_stocks(df,symbols):
    for symbol in symbols:
        df_temp = pd.read_csv("data/{}.csv".format(symbol), index_col="Date", parse_dates=True, na_values=['NaN'], usecols=['Date','Close'])
        df_temp = df_temp.rename(columns = {'Close' : symbol})
        if symbol == 'SPY':
            df = df_temp
        else:
            df = df.join(df_temp)
        df=df.dropna()
    df = df.sort_index(ascending=True, axis=0)
    return df

'''Function that prints out the list of stocks in the portfolio'''
def print_symbols(symbols):
    if symbols:
        print "List of stocks in portfolio:"
        for symbol in symbols:
            print "Stock: {} ".format(symbol)
        return True
    else:
        print "No available symbols"
        return False

'''Function that returns dataframe with stock values from total investment and allocations'''
def get_portfolio(df,symbols,allocs,total_investment):
    df_portfolio = normalize_data(df)
    for i in range(4):
        df_portfolio.loc[:,symbols[i]] *= (allocs[i]*total_investment)
    return df_portfolio

'''Function that reads in the allocations for each of the portfolio's stocks'''
def get_allocations(symbols):
    symbol_allocs = []
    allocs = []
    print "Enter stock allocations (total must equal 1.0)"
    for symbol in symbols:
        prompt = "Input allocation for {} (must be between 0 and 1): ".format(symbol)
        alloc = input(prompt)
        pair = (symbol, alloc)
        symbol_allocs.append(pair)
        allocs.append(alloc)
    print symbol_allocs
    return symbol_allocs, allocs

'''Function that retrieves the total investment in dollars'''
def get_total_investment():
    total_investment = input('Enter total investment : $')
    return total_investment

'''Function to compute Sharpe ratio for given portfolio'''
def compute_sharpe_ratio(allocs,df,total_investment, trading_days=252, daily_rfr=0):
    daily_returns = compute_daily_returns(df)
    daily_returns_mean = daily_returns.mean()
    daily_returns_std = daily_returns.std()
    sharpe_ratio = (daily_returns_mean-daily_rfr)/daily_returns_std
    return sharpe_ratio

'''Function that returns cumulative returns of a portfolio'''
def compute_cumulative_returns(allocs, df, total_investment):
    allocs = df * allocs
    portfolio_value = allocs * total_investment
    portfolio_value = portfolio_value.sum(axis=1)
    cumulative_returns = (portfolio_value[-1] / portfolio_value[0]) - 1
    return cumulative_returns

'''Function to compute and return daily returns for portfolio'''
def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0,:] = 0
    daily_returns = daily_returns.sum(axis=1)
    return daily_returns

'''Helper function that normalizes dataframe (for plotting)'''
def normalize_data(df):
    return df/df.ix[0,:]

'''Function that plots dataframe closing prices (normalized or standard)'''
def plot_data(df,normal,title="Stock Closing Prices"):
    if normal == True:
        df=normalize_data(df)
    ax = df.plot(title = title, fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    plt.show()

if __name__ == "__main__":
    test_run()
