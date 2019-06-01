import pandas as pd
import numpy as np

def ichimoku(highs, lows, close):
    kenkansen = ((highs.rolling(9).max() + lows.rolling(9).min()) / 2)
    kijunsen = ((highs.rolling(26).max() + lows.rolling(26).min()) / 2)
    leading_span_a = ((kenkansen + kijunsen) / 2).shift(26)
    leading_span_b = ((highs.rolling(52).max() + lows.rolling(52).min()) / 2).shift(26)
    lagging_span = close.shift(-26)
    return kenkansen, kijunsen, leading_span_a, leading_span_b, lagging_span


def money_flow_index(high, low, close, volume, period=14):
    
    def pos_flow(money_flow, typical_price):
        result = money_flow[money_flow > 0].sum()
        return result
    
    def neg_flow(money_flow, typical_price):
        result = money_flow[money_flow < 0].sum()
        return result

    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    typical_price = typical_price - close.shift(1)
    pos_mf = money_flow.copy()
    pos_mf[typical_price > 0] = money_flow[typical_price > 0].rolling(14).sum()
    neg_mf = money_flow.copy()
    neg_mf[typical_price < 0] = money_flow[typical_price < 0].rolling(14).sum()

    return 100 * (pos_mf / (pos_mf + neg_mf))

def rsi(close, period=21):
    ups = pd.Series(0, index=close.index)
    downs = pd.Series(0, index=close.index)
    delta = close - close.shift(1)
    ups[delta > 0] = delta
    downs[delta < 0] = -delta
    ups.fillna(0, inplace=True)
    downs.fillna(0, inplace=True)
    rs = ups.rolling(period).mean() / downs.rolling(period).mean()
    return 100 - (100 / (1 + rs))

def stochastic(close, high, low):
    k_ = 100 * (close - low.rolling(5).min()) / (high.rolling(5).max() - low.rolling(5).min())
    d_ = k_.rolling(3).mean()
    d_slow = d_.rolling(3).mean()
    return k_, d_, d_slow

def tsi(close, mom_smooth=25, smooth_smooth=13):
    def ema(m0, n):
        return (2 / (n + 1)) * (m0 - ema(m0.shift(1), n) + ema(m0.shift(1), n))
    return 





