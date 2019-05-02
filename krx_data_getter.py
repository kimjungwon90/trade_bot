import requests
from bs4 import BeautifulSoup
import pandas as pd


class krx_indus_index():
    
    base_url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?name=fileDown&filetype=csv&url=MKD/13/1301/13010102/mkd13010102&type=2&ind_type={}&period_strt_dd={}&period_end_dd={}&pagePath=%2Fcontents%2FMKD%2F13%2F1301%2F13010102%2FMKD13010102.jsp"
    df_columns = ["date", "close", "chg", "%chg", "open", "high", "low", "vol", "vol_won", "mkt_cap"]
    
    codes_list = pd.read_csv("./krx_core/krx_index_indexno_csv.csv", header="infer")
    
    def __init__(self):
        pass
    
    def get_index(self, start="19000101", end="30000101", code="5300"):
        url = self.base_url.format(code, start, end)
        response = requests.get(url)
        download_url = "http://file.krx.co.kr/download.jspx"
        json_data = {"code": response.content}
        headers_json = {"Referer": "http://marketdata.krx.co.kr/contents/MKD/99/MKD9900001.jspx"}
        data = requests.post(download_url, data=json_data, headers=headers_json)
        parsing = BeautifulSoup(data.text)
        parsing = parsing.text.split("\n")
        parsing = [line.replace(",", "").strip('"') for line in parsing]
        parsing = [x.split('""') for x in parsing]
        parsing = pd.DataFrame(parsing[1:], columns=self.df_columns)
        parsing.index = pd.to_datetime(parsing["date"], format="%Y/%m/%d")
        parsing.drop("date", axis=1, inplace=True)
        self.data = parsing.astype("float64")
        return self.data
    
    def get_all_index(self, start="19000101", end="30000101"):
        pass

class krx_vkospi():

    def __init__(self):
        self.base_url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?name=fileDown&filetype=csv&url=MKD/13/1301/13010302/mkd13010302&type=6&ind_type=1300&period_strt_dd={}&period_end_dd={}&pagePath=%2Fcontents%2FMKD%2F13%2F1301%2F13010302%2FMKD13010302.jsp"
        self.df_columns = ["date", "close", "chg", "%chg", "open", "high", "low"]
        pass

    def get_index(self, start, end):
        url = self.base_url.format(start, end)
        response = requests.get(url)
        download_url = "http://file.krx.co.kr/download.jspx"
        json_data = {"code": response.content}
        headers_json = {"Referer": "http://marketdata.krx.co.kr/contents/MKD/99/MKD9900001.jspx"}
        data = requests.post(download_url, data=json_data, headers=headers_json)
        parsing = BeautifulSoup(data.text)
        parsing = parsing.text.split("\n")
        parsing = [line.replace(",", "").strip('"') for line in parsing]
        parsing = [x.split('""') for x in parsing]
        parsing = pd.DataFrame(parsing[1:], columns=self.df_columns)
        parsing.index = pd.to_datetime(parsing["date"], format="%Y/%m/%d")
        parsing.drop("date", axis=1, inplace=True)
        self.data = parsing.astype("float64")
        return self.data
