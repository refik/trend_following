import pdb

import numpy as np
import pandas as pd


def antonacci_price(daily_price):
    """Return aggregated price for Antonacci strategy."""
    # We work with monthly returns on this strategy
    return daily_price.resample('M').last()


def antonacci_weight(daily_price, get_top=2, periods=6):
    """Return equally weighted weights for the Antonacci strategy.
    
    get_top -- Number of assets that will be selected based on their return.
    periods -- How many periods to look back for ranking historical return.
    """
    monthly_return = daily_price.resample('M').last().pct_change(periods=periods)
    monthly_return_numpy = monthly_return.to_numpy()
    
    # Dimensions of the returns. n number of assets, t time
    t, n = monthly_return_numpy.shape
    
    # Sorting returns per period, getting only winning sorted indices
    sorted_winners = np.argsort(-monthly_return_numpy)[:, range(get_top)]

    # A matrix with same shape as data, full column indices for every row
    col_indices_matrix = np.tile(np.arange(n), (t, 1))

    # Get true in place of winning assets
    winner_matrix = np.stack([
        np.isin(indices, winners) for indices, winners
        in zip(col_indices_matrix, sorted_winners)
    ])

    signal = pd.DataFrame(
        data=winner_matrix.astype(int),
        index=monthly_return.index, 
        columns=monthly_return.columns
    )     
    
    return signal * (1 / get_top)


def antonacci_inv_vol_weight(daily_price, get_top=2, periods=6):
    """Return inverse volatility weighted weights for the Antonacci strategy.
    
    get_top -- Number of assets that will be selected based on their return.
    periods -- How many periods to look back for ranking historical return.
    """
    annual_days = 261
    center_of_mass = 60
    
    # Get returns from price data
    daily_return = daily_price.pct_change()
    
    # Calculate volatility by exponential weighted average
    daily_vol = daily_return.ewm(com=center_of_mass).std()
    
    # Annualize the volatility
    annualized_daily_vol = daily_vol * np.sqrt(annual_days)
    
    # We will reweight every month so only get the end of month
    end_of_month_vol = annualized_daily_vol.resample('M').last()

    monthly_return = daily_price.resample('M').last().pct_change(periods=periods)
    monthly_return_numpy = monthly_return.to_numpy()
    
    # Dimensions of the returns. n number of assets, t time
    t, n = monthly_return_numpy.shape
    
    # Sorting returns per period, getting only winning sorted indices
    sorted_winners = np.argsort(-monthly_return_numpy)[:, range(get_top)]

    # A matrix with same shape as data, full column indices for every row
    col_indices_matrix = np.tile(np.arange(n), (t, 1))

    # Get true in place of winning assets
    winner_matrix = np.stack([
        np.isin(indices, winners) for indices, winners
        in zip(col_indices_matrix, sorted_winners)
    ])

    signal = pd.DataFrame(
        data=winner_matrix.astype(int),
        index=monthly_return.index, 
        columns=monthly_return.columns
    )
    
    # Weighting by inverse volatility
    vol_signal = signal * (1 / end_of_month_vol + 1e-5)
    vol_signal_sum = vol_signal.sum(axis=1)
    vol_signal_weighted = vol_signal.divide(vol_signal_sum, axis=0)

    return vol_signal_weighted


def tsmom_price(daily_price):
    """Return aggregated price for TSMOM strategy."""
    # We are using monthly returns
    return daily_price.resample('M').last()


def tsmom_weight(daily_price, target_vol=0.4, periods=12):
    """Return weights for the TSMOM strategy.
    
    target_vol -- Per asset volatility target.
    periods -- How many periods to look back for ranking historical return.
    """
    monthly_price = daily_price.resample('M').last()
    return_12m = monthly_price.pct_change(periods=periods)
    signal = np.sign(return_12m)
    
    # Weights are adjusted according to the volatility
    # Volatility is calculated annually and on a rolling basis
    annual_days = 261
    center_of_mass = 60
    
    # Get returns from price data
    daily_return = daily_price.pct_change()
    number_of_assets = daily_return.shape[1]
    
    # Calculate volatility by exponential weighted average
    daily_vol = daily_return.ewm(com=center_of_mass).std()
    
    # Annualize the volatility
    annualized_daily_vol = daily_vol * np.sqrt(annual_days)
    
    # We will reweight every month so only get the end of month
    end_of_month_vol = annualized_daily_vol.resample('M').last()
    
    # Adjust according to our target volatility
    return signal * (target_vol / end_of_month_vol / number_of_assets)