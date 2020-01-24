import numpy as np
import pandas as pd
import functools


@functools.lru_cache(maxsize=None)
def risk_free_rate():
    """Return risk free rate from 3 month t-bills."""
    raw = pd.read_csv('data/US_3M_daily_rate.csv', 
                      parse_dates=[0], names=['date', 'rate'], 
                      index_col='date', header=0, na_values='.', 
                      dtype={'rate': np.float64})
    
    raw = raw.ffill()  # Forward fill missing days

    return raw / 100 # To make it percent


@functools.lru_cache(maxsize=None)
def futures_price(path='../data/clean/excess_returns.xlsx'):
    """Return excess return prices from Moskowitz futures data set."""
    path = 'data/excess_returns.xlsx'
    
    # Retreiving correct excel sheet
    return_excess = pd.read_excel(path, sheet_name='simple_excess_returns', 
                                  index_col=0, header=[0, 1])
    
    # Transforming returns to prices
    return (return_excess + 1).cumprod()


@functools.lru_cache(maxsize=None)
def etf_price():
    """
    This function renames assets to understandable names returns asset prices as
    pandas data frames, one asset per each column.
    """
    path = 'data/antonacci.csv'
    
    simple_names = {
        'FRUSS1L': 'Equity US',    'SPEU35$': 'Equity Europe',
        'MSJPAN$': 'Equity Japan', 'MSPXJP$': 'Equity Asia',
        'LHT7T10': 'Bonds 7-10yr', 'LHUT1T3': 'Bonds 1-3yr',
        'GOLDBLN': 'Gold'
    }

    price = (
        pd.read_csv(path, parse_dates=[3])
            .pivot(index='date', columns='symbol', values='price')
            .rename(columns=simple_names)[simple_names.values()]
    ).dropna()
    
    asset_class = ['Equity', 'Equity', 'Equity', 'Equity', 'Bonds', 'Bonds', 'Gold']
    col_index = pd.MultiIndex.from_arrays([asset_class, price.columns.values])
    price.columns = col_index
    
    return price
