#%%
from pandas import Series, DataFrame
from pandas.tseries.offsets import Day, MonthEnd
import math
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import cx_Oracle
import pandas as pd
import datetime

#%%
con_1 = cx_Oracle.connect("scott/tiger@172.16.116.99:1521/XE")
con_2 = cx_Oracle.connect("scott/tiger@172.16.116.113:1521/XE")
#conn = create_engine()
cur_1 = con_1.cursor()

#%%
def fetch_data(connection, table_name, date_from, date_to):
    sql_value = """ SELECT a.*
                  FROM %s a
                 WHERE DT BETWEEN '%s' AND '%s'
                 ORDER BY DT""" %(table_name,date_from, date_to) 
                 
    sql_column = """SELECT COLUMN_NAME
                      FROM ALL_TAB_COLUMNS
                     WHERE TABLE_NAME = '%s'""" %(table_name)

    if connection == 'con_1':
        con = cx_Oracle.connect("scott/tiger@172.16.116.99:1521/XE")
    elif connection == 'con_2':
        con = cx_Oracle.connect("scott/tiger@172.16.116.113:1521/XE")
    
    cur = con.cursor()
    cur.execute(sql_value)
    data = cur.fetchall()
    data = pd.DataFrame(data)

    cur.execute(sql_column)
    column_name = cur.fetchall()
    column_name = list(pd.DataFrame(column_name).iloc[:,0])
    del column_name[column_name.index('DT')]
    column = list(['DATE'])
    column.extend(column_name)

    data.columns = column
    data = data.set_index('DATE')
    
    return data


xx = fetch_data('con_2', 'INDEX_SET_BDAY', '2019-01-01', '2019-03-31')

#%%
import naver_crawler as naver

nv = naver.naver_stock_crawler()
stock_price = nv.get_stock(code="005930")
samsung = stock_price['ncv']

period=20
x = samsung[-period:]

def willr(price_series, look_back=20):
    close = price_series[-1]
    highest_high = max(price_series[-period:])
    lowest_low = min(price_series[-period:]) 
    r = -100*((highest_high-close)/(highest_high-lowest_low))

    return r

def technical_trade(price_series, indicator, look_back=20, buy_threshold=20, sell_threshold=80):
    current = price_series[-1]
    indicate = indicator(price_series, look_back)

    if indicate > sell_threshold:
        signal = -1
    elif indicate < buy_threshold:
        signal = 1
    else :
        signal = 0
    
    return signal

x = samsung.map(willr)

type(samsung)


