import calculate

from tabulate import tabulate


def result_table(fmt='latex_booktabs'):
    """Return a LaTeX table for the strategy results."""
    
    names = [
        "ETF EW.",
        "Antonacci ETF",
        "Antonacci ETF Inv. Vol.",
        "Futures EW.",
        "Antonacci Futures",
        "Antonacci Futures Inv. Vol.",
        "TSMOM Futures Low Vol.",
        "TSMOM Futures High Vol."
    ]

    # Get stats for each strategy
    s1 = calculate.stats_from_parameters(name='Antonacci', price_set='ETF',     fee_rate_bps=10, get_top=7,  target_vol=40,  periods=6, vol_weight=False)
    s2 = calculate.stats_from_parameters(name='Antonacci', price_set='ETF',     fee_rate_bps=10, get_top=2,  target_vol=40,  periods=6, vol_weight=False)
    s3 = calculate.stats_from_parameters(name='Antonacci', price_set='ETF',     fee_rate_bps=10, get_top=2,  target_vol=40,  periods=6, vol_weight=True)
    s4 = calculate.stats_from_parameters(name='Antonacci', price_set='Futures', fee_rate_bps=10, get_top=47, target_vol=40,  periods=6, vol_weight=False)
    s5 = calculate.stats_from_parameters(name='Antonacci', price_set='Futures', fee_rate_bps=10, get_top=10, target_vol=40,  periods=6, vol_weight=False)
    s6 = calculate.stats_from_parameters(name='Antonacci', price_set='Futures', fee_rate_bps=10, get_top=10, target_vol=40,  periods=6, vol_weight=True)
    s7 = calculate.stats_from_parameters(name='TSMOM',     price_set='Futures', fee_rate_bps=10, get_top=10, target_vol=40,  periods=6, vol_weight=False)
    s8 = calculate.stats_from_parameters(name='TSMOM',     price_set='Futures', fee_rate_bps=10, get_top=10, target_vol=100, periods=6, vol_weight=False)

    # The relevant columns from the summary data
    cols = [3, 4, 5, 6]
    num_assets = [7, 2, 2, 47, 10, 10, 47, 47]
    stats = [s1, s2, s3, s4, s5, s6, s7, s8]
    table = [names]
    
    # Collecting the results
    for i, col in enumerate(cols):
        col_list = [round(stat['summary'][col], 2) for stat in stats]
        table.append(col_list)

    table.append(num_assets)
    table = list(map(list, zip(*table))) # Transpose
    
    # Creating table headers
    headers = ['Strategy Name', 'Annual Return', 'Annual Vol.', 'Sharpe', 'Max. Drawdown', '# Assets']
    
    # Returning latex table
    tbl = tabulate(table, headers, tablefmt=fmt)
    print(tbl)
    
    return tbl