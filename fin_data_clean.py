import pandas as pd
import numpy as np

def acc_dates(date):
    if date.month == 12:
        date = date + pd.offsets.Day(90)
    else:
        date = date + pd.offsets.Day(45)
    return date

def accounting_offset(dates):
    if type(dates) != pd.core.indexes.datetimes.DatetimeIndex:
        raise ValueError("Insert DatetimeIndex")
    dates = dates + pd.offsets.MonthEnd(0)
    result = pd.Series(dates).apply(acc_dates)
    return result