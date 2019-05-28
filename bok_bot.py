import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

class bok_api:

    key = "RK4O8KBR4N0O4E2W6V9E"
    url_base = "http://ecos.bok.or.kr/api/"
    table = None
    stat_code = None
    data_format = {
        "DD": "%Y%m%d",
        "MM": "%Y%m",
        "YY": "%Y"
    }
    
    def __init__(self):
        url = self.url_base + "StatisticTableList/{}/json/kr/0/{}".format(self.key, str(1000))
        result = requests.get(url)
        result = pd.DataFrame(result.json()["StatisticTableList"]["row"])
        self.table = result
    
    def get_stat_list_detail(self, stat_code="", rows=1000):
        if stat_code == "":
            raise ValueError("Stat code not provided! Please insert stat code!")
        url = self.url_base + "StatisticItemList/{}/json/kr/0/{}/{}".format(self.key, str(rows), stat_code)
        self.stat_code = stat_code
        result = requests.get(url)
        result = pd.DataFrame(result.json()["StatisticItemList"]["row"])
        self.table_detail = result
    
    def get_stat_data(self, item_code, stat_code="", rows=10000, start="19000101", end="30000101"):
        if item_code == "":
            raise ValueError("Item code not provided! Please insert item code!")
        if stat_code != "":
            self.stat_code = stat_code
        self.item_code = item_code
        self.period = self.table_detail[self.table_detail["ITEM_CODE"] == self.item_code]["CYCLE"].values[0]
        data_format = self.data_format[self.period]
        url = self.url_base + "StatisticSearch/{}/json/kr/0/{}/{}/{}/{}/{}/{}".format(self.key, rows, self.stat_code, self.period, start, end, self.item_code)
        result = requests.get(url)
        unit = result.json()["StatisticSearch"]["row"][0]["UNIT_NAME"]
        result = pd.DataFrame(result.json()["StatisticSearch"]["row"])
        result = result[["TIME", "DATA_VALUE"]]
        result.index = pd.to_datetime(result["TIME"], format=data_format)
        result = result["DATA_VALUE"].replace("", np.nan).astype("float64")
        result.rename({"DATA_VALUE":"DATA_VALUE ({})".format(unit)})
        return result

