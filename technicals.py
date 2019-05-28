import pandas as pd
import numpy as np

def ichimoku(highs, lows, close):
    kenkansen = (highs.rolling(9).max() + lows.rolling(9).min()) / 2
    kijunsen = (highs.rolling(26).max() + lows.rolling(26).min()) / 2
    leading_span_a = (kenkansen + kijunsen) / 2
    leading_span_b = (highs.rolling(52).max() + lows.rolling(52).min()) / 2
    lagging_span = close.shift(26)
    return kenkansen, kijunsen, leading_span_a, leading_span_b, lagging_span

