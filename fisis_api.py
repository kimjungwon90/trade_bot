#%%
import requests
import pandas as pd


class fisis_api:

    key = "3b7633c9e5d1e65d67a4831fd0592293"

    def __init__(self):
        pass

    def get_stats(self, large_div, small_div):
        url = "http://fisis.fss.or.kr/openapi/statisticsListSearch.json?lang=kr&auth={}&lrgDiv={}&smlDiv={}"
        req_url = url.format(self.key, large_div, small_div)
        response = requests.get(req_url)
        return response

#%%
test_api = fisis_api()

#%%
test = test_api.get_stats("L", "B")


#%%
pd.DataFrame(test.json()["result"]["list"])

#%%
