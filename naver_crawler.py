#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

class naver_stock_crawler:

    def __init__(self):
        kospi_url = "https://m.stock.naver.com/api/json/sise/siseListJson.nhn?menu=market_sum&sosok=0&pageSize=10000&page=1"
        kosdaq_url = "https://m.stock.naver.com/api/json/sise/siseListJson.nhn?menu=market_sum&sosok=1&pageSize=10000&page=1"
        etf_url = "https://m.stock.naver.com/api/json/sise/etfItemListJson.nhn?pageSize=10000&page=1"
        response = requests.get(kospi_url).json()["result"]["itemList"]
        df_list = pd.DataFrame(response)[["cd", "nm"]]
        self.kospi_list = df_list
        response = requests.get(kosdaq_url).json()["result"]["itemList"]
        df_list = pd.DataFrame(response)[["cd", "nm"]]
        self.kosdaq_list = df_list
        response = requests.get(etf_url)
        df_etfs = pd.DataFrame(response.json()["result"]["itemList"])[["cd", "nm"]]
        self.etf_list = df_etfs
    
    def get_stock(self, code="006800"):
        base_url = "https://m.stock.naver.com/api/item/getPriceDayList.nhn?code={}&pageSize=10000&page=1"
        url = base_url.format(code)
        response = requests.get(url)
        df_stock = pd.DataFrame(response.json()["result"]["list"])
        df_stock.index = pd.to_datetime(df_stock["dt"], format="%Y%m%d").reset_index(drop=True)
        df_stock = df_stock.sort_index().drop("dt", axis=1)
        self.data = df_stock
        print("{} Done.".format(code))
        return df_stock
