#%%
import requests
import pandas as pd


class fisis_api:

    key = input("insert fisis api key : ")
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

    def get_data(self, company_code, stat_code, period, start, end):
        url_ext = "statisticsInfoSearch.json?lang=kr&auth={}&financeCd={}&listNo={}&term={}&startBaseMm={}&endBaseMm={}"
        url = self.base_url + url_ext.format(self.key, company_code, stat_code, period, start, end)
        response = requests.get(url).json()["result"]
        if response["err_cd"] != "000":
            raise ValueError(response["err_msg"])
        else:
            self.unit = response["unit"]
            response = response["list"]
        return response


#%%

