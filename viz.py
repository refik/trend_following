import numpy as np

import matplotlib.pyplot as plt
from ipywidgets import interact


def stats_plot(stats):
    """Return useful plots of portfolio statistics."""
    # Create figures for the plots
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    
    # Net asset value
    stats['nav'].plot(ax=axs[0][0])
    axs[0][0].set_title('Portfolio NAV')
      
    # If all weights greater than 1, stack them
    if np.any(stats['asset_class_weights'] < 0):
        stats['asset_class_weights'].plot(ax=axs[0][1])
    else:   
        stats['asset_class_weights'].plot.area(ax=axs[0][1])   
    axs[0][1].set_title('Asset Weights')
    
    # Leverage of the portfolio
    stats['leverage'].plot(ax=axs[0][2])
    axs[0][2].set_title('Portfolio Leverage')
    
    # Drawdown of the portfolio
    stats['drawdown'].plot(ax=axs[1][0])
    axs[1][0].set_title('Portfolio Drawdown')
    
    # Rolling volatility of portfolio
    stats['ewm_volatility'].plot(ax=axs[1][1])
    axs[1][1].set_title('EWM Volatility')

    # Rolling mean of portfolio turnover
    stats['turnover_annual'].plot(ax=axs[1][2])
    axs[1][2].set_title('12m Rolling Turnover')