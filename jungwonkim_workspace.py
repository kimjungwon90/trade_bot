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
    column_name = list(pd.DataFrame(column_name).iloc[:, 0])
    del column_name[column_name.index('DT')]
    column = list(['DATE'])
    column.extend(column_name)

    data.columns = column
    data = data.set_index('DATE')
    
    return data


xx = fetch_data('con_2', 'INDEX_SET_BDAY', '2019-01-01', '2019-03-31')

#%%
#%% Visualization
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

np.random.seed(1000)
y = np.random.standard_normal(20)
x = range(len(y))
plt.plot(x, y)
plt.plot(y.cumsum())
plt.grid(True)
#plt.axis('tight')
plt.xlim(-1, 20)
plt.ylim(np.min(y.cumsum())-1, np.max(y.cumsum())+1)

plt.figure(figsize=(7,4))
plt.plot(y.cumsum(), 'b', lw=1.5)
plt.plot(y.cumsum(),'ro')
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

np.random.seed(2000)
y = np.random.standard_normal((20,2)).cumsum(axis=0)
plt.plot(y, lw=1.5)
plt.plot(y, 'ro')
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

plt.figure(figsize=(7,4))
plt.plot(y[:,0],lw=1.5, label='1st')
plt.plot(y[:,1],lw=1.5, label='2nd')
plt.plot(y,'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

fig, ax1 = plt.subplots()
plt.plot(y[:,0], 'b', lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.grid(True)
plt.legend(loc=8)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value 1st')
plt.title('A Simple Plot')
ax2 = ax1.twinx()
plt.plot(y[:,1], 'g', lw=1.5, label='2nd')
plt.plot(y[:,1], 'ro')
plt.legend(loc=0)
plt.ylabel('value 2nd')

plt.figure(figsize=(7,5))
plt.subplot(211)
plt.plot(y[:,0], lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.ylabel('value')
plt.title('A Simple Plot')
plt.subplot(212)
plt.plot(y[:,1], 'g', lw=1.5, label='2nd')
plt.plot(y[:,1], 'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.ylabel('value')

plt.figure(figsize=(9,4))
plt.subplot(121)
plt.plot(y[:,0], lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('1st Data Set')
plt.subplot(122)
plt.bar(np.arange(len(y)), y[:,1], width=0.5, color='g', label='2nd')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.title('2nd Data Set')

y = np.random.standard_normal((1000, 2))
plt.figure(figsize=(7, 5))
plt.plot(y[:, 0], y[:, 1], 'ro')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

plt.figure(figsize=(7, 5))
plt.scatter(y[:, 0], y[:, 1], marker='o')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

c = np.random.randint(0, 10, len(y))
plt.figure(figsize=(7,5))
plt.scatter(y[:, 0], y[:, 1],c=c, marker='o')
plt.colorbar()
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

plt.figure(figsize=(7,4))
plt.hist(y, label=['1st', '2nd'], bins=25)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

plt.figure(figsize=(7,4))
plt.hist(y, label=['1st', '2nd'], bins=25)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

plt.figure(figsize=(7,4))
plt.hist(y, label=['1st', '2nd'], color=['b', 'g'], stacked=True, bins=20)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

fig, ax = plt.subplots(figsize=(7, 4))
plt.boxplot(y)
plt.grid(True)
plt.setp(ax, xticklabels=['1st', '2nd'])
plt.xlabel('data set')
plt.ylabel('value')
plt.title('Boxplot')


from matplotlib.patches import Polygon
def func(x):
    return 0.5 * np.exp(x) + 1

a, b = 0.5, 1.5 # integral limits
x = np.linspace(0, 2)
y = func(x)
fig, ax = plt.subplots(figsize=(7, 5))
plt.plot(x, y, 'b', linewidth=2)
plt.ylim(ymin=0)
# Illustrate the integral value, i.e. the area under the function
# between the lower and upper limits
Ix = np.linspace(a, b)
Iy = func(Ix)
verts = [(a, 0)] + list(zip(Ix, Iy)) + [(b, 0)]
poly = Polygon(verts, facecolor='0.7', edgecolor='0.5')
ax.add_patch(poly)
plt.text(0.5 * (a + b), 1, r"$\int_a^b f(x)\mathrm{d}x$",
horizontalalignment='center', fontsize=20)
plt.figtext(0.9, 0.075, '$x$')
plt.figtext(0.075, 0.9, '$f(x)$')
ax.set_xticks((a, b))
ax.set_xticklabels(('$a$', '$b$'))
ax.set_yticks([func(a), func(b)])
ax.set_yticklabels(('$f(a)$', '$f(b)$'))
plt.grid(True)

import mpl_finance as mpf
import FinanceDataReader as fdr
sp500 = fdr.DataReader( "SPY" , start = "1/1/2000" , end = "4/14/2014" )
sp500.info()
#ohlcv 순으로 되어있는 경우
fig, ax = plt.subplots(figsize=(8, 5))
fig.subplots_adjust(bottom=0.2)
mpf.candlestick(ax, sp500, width=0.6, colorup=‘b’, colordown=‘r’)
plt.grid(True)
ax.xaxis_date()
# dates on the x-axis
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=30)

strike = np.linspace(50, 150, 24)
ttm = np.linspace(0.5, 2.5, 24)
strike, ttm = np.meshgrid(strike, ttm)

strike
ttm
#%%
import naver_crawler as naver

df = fetch_data('con_2','INDEX_SET_BDAY','2015-01-05', '2018-12-30')
df = pd.DataFrame(df[df['SPX'].notnull()]['SPX'])
#x = np.array(df['SPX'].values)
#nv = naver.naver_stock_crawler()
#stock_price = nv.get_stock(code="005930")
#samsung = stock_price['ncv']

period=20
#x = samsung[-period:]
#x = x[-period:]


def willr(price_series, look_back=20):
    close = price_series[-1]
    highest_high = max(price_series[-period:])
    lowest_low = min(price_series[-period:]) 
    r = -100*((highest_high-close)/(highest_high-lowest_low))

    return r

def technical_trade(price_series, indicator, look_back=20, sell_threshold=-20, buy_threshold=-80):
    current = price_series[-1]
    indicate = indicator(price_series, look_back)

    if indicate > sell_threshold:
        signal = -1
    elif indicate < buy_threshold:
        signal = 1
    else :
        signal = 0
    
    return signal

df['willr'] = 1000000
for i in range(19,  df['SPX'].count()):
    price_series = df['SPX'][i-19:i+1]
    df['willr'][i] = willr(price_series,20)
    print(df['SPX'][i], df['willr'][i])

df['return'] = df['SPX']/df['SPX'].shift(1)-1

df['signal'] = 0
df['signal'][df['willr']<-80]  = 1
df['signal'][df['willr']>-20]  = -1

df['signal_1'] = df['signal'].rolling(5).sum()
df['signal_2'] = 0
df['signal_2'][df['signal_1']>=3] = 1
df['signal_2'][df['signal_1']<=-3] = 0 #short sell의 경우 -1

df['position_return'] = 0
df['position_return'] = df['return'][df['signal_2'].shift(1)==1]
df['position_return'][df['position_return'].isnull()] = 0
df['final_return'] = df['position_return'].cumsum().apply(np.exp)

plt.figure(figsize=(16,7))
plt.subplot(411)
plt.plot(df['SPX'][20:], lw=1.5, label='SPX')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('SPX')
plt.title('Timeseries')
plt.subplot(412)
plt.plot(df['willr'][20:], lw=1.5, label='willr')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('Willam %r')
plt.title('William %r')
plt.subplot(413)
plt.plot(df['signal_2'][20:], lw=1.5, label='signal')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('signal')
plt.title('signal')
plt.subplot(414)
plt.plot(df['final_return'][20:], lw=1.5, label='signal')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('return')
plt.title('cum return')

plt.plot(df['final_return'][20:], lw=1.5, label='signal')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('return')
plt.title('cum return')

plt.figure(figsize=(16,7))
plt.plot(df['signal_2'][20:], lw=1.5, label='signal')
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('Date')
plt.ylabel('signal')
plt.title('signal')


#%%
