import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

import requests
import pandas as pd


def stock_to_df(code):
    stock = code
    response = requests.get("https://m.stock.naver.com/api/item/getPriceDayList.nhn?code={}&pageSize=10000&page=1".format(stock))

    df_stock = pd.DataFrame(response.json()["result"]["list"])
    df_stock.index = pd.to_datetime(df_stock["dt"], format="%Y%m%d").reset_index(drop=True)
    df_stock = df_stock.sort_index().drop("dt", axis=1)
    print("{} done.".format(code), end="\t")
    return df_stock

def pool_crawl(stock_list):
    pool = Pool(processes=(cpu_count() - 1))
    results = pool.map(stock_to_df, stock_list)
    pool.close()
    pool.join()
    return results




kospi_info = pd.read_csv("./market_info/kospi.csv", index_col=0)
kosdaq_info = pd.read_csv("./market_info/kosdaq.csv", index_col=0)
date_info = pd.read_csv("./market_info/date_df.csv", index_col=0)["dt"]
date_info = pd.to_datetime(date_info, format="%Y%m%d").sort_values(ascending=True).reset_index(drop=True)

kospi_list = pd.Series(kospi_info[kospi_info["section"] == 1].index).apply(lambda x: x[1:])
kosdaq_list = pd.Series(kosdaq_info[kosdaq_info["section"] == 1].index).apply(lambda x: x[1:])

df_kospi = pool_crawl(kospi_list)
df_kosdaq = pool_crawl(kosdaq_list)

df_open_kospi = pd.DataFrame(columns=kospi_list)
df_close_kospi = pd.DataFrame(columns=kospi_list)
df_high_kospi = pd.DataFrame(columns=kospi_list)
df_low_kospi = pd.DataFrame(columns=kospi_list)
df_rtn_kospi = pd.DataFrame(columns=kospi_list)
df_vol_kospi = pd.DataFrame(columns=kospi_list)


df_open_kosdaq = pd.DataFrame(columns=kosdaq_list)
df_close_kosdaq = pd.DataFrame(columns=kosdaq_list)
df_high_kosdaq = pd.DataFrame(columns=kosdaq_list)
df_low_kosdaq = pd.DataFrame(columns=kosdaq_list)
df_rtn_kosdaq = pd.DataFrame(columns=kosdaq_list)
df_vol_kosdaq = pd.DataFrame(columns=kosdaq_list)

for x, y in zip(df_kospi, kospi_list):
    df_open_kospi[y] = x["ov"]
    df_close_kospi[y] = x["ncv"]
    df_high_kospi[y] = x["hv"]
    df_low_kospi[y] = x["lv"]
    df_rtn_kospi[y] = x["cr"] / 100
    df_vol_kospi[y] = x["aq"]

for x, y in zip(df_kosdaq, kosdaq_list):
    df_open_kosdaq[y] = x["ov"]
    df_close_kosdaq[y] = x["ncv"]
    df_high_kosdaq[y] = x["hv"]
    df_low_kosdaq[y] = x["lv"]
    df_rtn_kosdaq[y] = x["cr"] / 100
    df_vol_kospi[y] = x["aq"]
    
df_open_kospi.to_csv("kospi_open.csv")
df_close_kospi.to_csv("kospi_close.csv")
df_high_kospi.to_csv("kospi_high.csv")
df_low_kospi.to_csv("kospi_low.csv")
df_rtn_kospi.to_csv("kospi_rtn.csv")

df_open_kosdaq.to_csv("kosdaq_open.csv")
df_close_kosdaq.to_csv("kosdaq_close.csv")
df_high_kosdaq.to_csv("kosdaq_high.csv")
df_low_kosdaq.to_csv("kosdaq_low.csv")
df_rtn_kosdaq.to_csv("kosdaq_rtn.csv")