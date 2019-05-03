#%%
import requests
import pandas as pd


class fisis_api:

    key = "3b7633c9e5d1e65d67a4831fd0592293"
    base_url = "http://fisis.fss.or.kr/openapi/"

    def __init__(self):
        pass

    def get_stats(self, large_div, small_div):
        url = self.base_url + "statisticsListSearch.json?lang=kr&auth={}&lrgDiv={}&smlDiv={}"
        req_url = url.format(self.key, large_div, small_div)
        response = requests.get(req_url)
        response = pd.DataFrame(response.json()["result"]["list"])
        return response

    def get_comps(self, div="A"):
        url_ext = "companySearch.json?lang=kr&auth={}&partDiv={}"
        url = self.base_url + url_ext.format(self.key, div)
        response = requests.get(url)
        response = pd.DataFrame(response.json()["result"]["list"])
        return response

    def get_accnts(self, list_no="SA001"):
        url_ext = "accountListSearch.json?lang=kr&auth={}&listNo={}"
        url = self.base_url + url_ext.format(self.key, list_no)
        response = requests.get(url)
        response = pd.DataFrame(response.json()["result"]["list"])
        return response


#%%
test_api = fisis_api()


#%%
df_stats = pd.read_csv("./fisis_core/stats_list.csv", index_col=0)

#%%
list_nos = df_stats["list_no"]

#%%
df_stats = pd.DataFrame()
div = ["A", "J", "H", "I", "F", "W", "G", "X", "D", "C", "K", "T", "N", "E", "O", "Q", "P", "S", "M", "L", "B", "R"]
stats = ["A", "B", "C", "D", "P"] 
for div in divs:
    for stat in stats:
        try:
            test = test_api.get_stats(div, stat)
            df_stats = df_stats.append(test, ignore_index=True)
        except Exception as e:
            print(e)

#%%
df_stats.to_csv("./fisis_core/stats_list.csv", index=False)
#%%
