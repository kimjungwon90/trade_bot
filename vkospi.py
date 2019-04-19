import requests
from bs4 import BeautifulSoup
import pandas as pd

url_1 = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?name=fileDown&filetype=csv&url=MKD/13/1301/13010302/mkd13010302&type=6&ind_type=1300&period_strt_dd=20000101&period_end_dd=20190416&pagePath=%2Fcontents%2FMKD%2F13%2F1301%2F13010302%2FMKD13010302.jsp"
response = requests.get(url_1)

url_2 = "http://file.krx.co.kr/download.jspx"
json_data = {
    "code" : response.content
}
headers_json = {
    "Referer": "http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx"
}
columns = ["dt", "close", "change", "rate", "open", "high", "low"]
data = requests.post(url_2, data=json_data, headers=headers_json)
parsing = BeautifulSoup(data.text)
parsing_df = parsing.text.split("\n")
parsing_df = [x.split(",") for x in parsing_df]

parsing = BeautifulSoup(data.text)
parsing_df = parsing.text.split("\n")
parsing_df = [x.split(",") for x in parsing_df]
parsing_df = pd.DataFrame(parsing_df[1:], columns=columns)
parsing_df.index = parsing_df["dt"]
parsing_df.drop("dt", axis=1, inplace=True)

def to_float(element):
    if (type(element) == str) and (len(element) != 0):
        res = element.replace('\"', "")
        return float(res)

for column in parsing_df.columns:
    parsing_df[column] = parsing_df[column].apply(to_float).astype("float32")
    
parsing_df["rate"] /= 100
parsing_df.index = pd.to_datetime(parsing_df.index, format='"%Y/%m/%d"')
parsing_df.to_csv("./krx_web/vkospi_d.csv")