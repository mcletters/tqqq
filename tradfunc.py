def getYFinData(symbol, start, end):
    """ Obtains data from Yahoo Finanace. """
    
    import yfinance as yf
    
    # https://ranaroussi.github.io/yfinance/reference/index.html

    # Documentation on yf.download
    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
    
    # Fetch daily data
    df = yf.download(symbol, 
                     start=start,
                     end=end,
                     progress=False, 
                     multi_level_index = False)
    
    if df.empty:
        raise SystemExit("No data fetched. Check symbol/dates/network.")
    
    else:
        
        print('Yahoo Finance data read in')
        print('  symbol:',symbol)
        print('  start :',start)
        print('  end   :',end)
        
        print('\nShape of DataFrame:',df.shape)
        print('\nSummary of DataFrame:\n',df.describe())

        return df


def get_ema(df, window_range, close='close'):
    """
    Calculates the Exponential Moving Average (EMA) for a given window
    
    EMA = Closing price x multiplier + EMA_prev_day x (1-multiplier)
    Multiplier = smoothing / (N_days + 1)
        Note: common value for smoothing = 2
    NOTE: for first EMA, use previous day's sma as EMA
    """
    from ta.trend import EMAIndicator
    from ta.volatility import AverageTrueRange
    
    # create EMA 
    ema = EMAIndicator(close = df["close"], window = window_range, fillna=True)

    var_name = 'ema' + str(window_range)
    df[var_name] = ema.ema_indicator()   # or ema.indicator()
    
    return df


def get_true_range(hi, low, prev_close, debug='no'):
    """ 
    Calculates the true range.
    Calculate:
      a) High - Low
      b) abs(High - prev close)
      c) abs(Low - prev close)
    Take Max of 3 ests = "true range" (TR)
    """
    hi_minus_low = hi - low
    abs_hi_prv = abs(hi - prev_close)
    abs_low_prv = abs(low - prev_close)

    if debug.lower() == 'yes':
        print('hi - low:',hi_minus_low)
        print('abs(hi - prev. close):',abs_hi_prv)
        print('abs(low - prev. close):',abs_low_prv)
    
    # returns the true range
    return max(hi_minus_low, abs_hi_prv, abs_low_prv)


if __name__ == "__main__":
    print('Functions for Trading Project')
