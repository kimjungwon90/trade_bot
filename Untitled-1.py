#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

class naver_stock_crawler:

    def __init__(self):
        self.base_url = "https://m.stock.naver.com/api/item/getPriceDayList.nhn?code={}&pageSize=10000&page=1"
        pass
    
    def get_stock_list(self, code="006800"):
        pass

    def get_etf_list(self):
        url = "https://m.stock.naver.com/api/json/sise/etfItemListJson.nhn?pageSize=10000&page=1"
        response = requests.get(url)
        df_etfs = pd.DataFrame(response.json()["result"]["itemList"])
        return df_etfs

    def get_stock(self, code="006800"):
        url = self.base_url.format(code)
        response = requests.get(url)
        df_stock = pd.DataFrame(response.json()["result"]["list"])
        df_stock.index = pd.to_datetime(df_stock["dt"], format="%Y%m%d").reset_index(drop=True)
        df_stock = df_stock.sort_index().drop("dt", axis=1)
        self.data = df_stock
        print("{} Done.".format(code))
        return df_stock

#%%
test_api = naver_stock_crawler()
mad = test_api.get_stock("006800")
df_etfs = test_api.get_etf_list()
#%%
df_etfs
