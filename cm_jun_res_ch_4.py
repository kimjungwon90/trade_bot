#%%
import naver_crawler
import matplotlib.pyplot as plt
import technicals
import sklearn
import seaborn as sns

sns.set_style("white")

test_api = naver_crawler.naver_stock_crawler()
test_data = test_api.get_stock("069500").loc["2016-01-01":, :]

#%%
ichi_moku = technicals.ichimoku(test_data["hv"], test_data["lv"], test_data["ncv"])

#%%
plt.figure(figsize=(12, 8))
plt.plot(test_data["ncv"], label="Close")
plt.plot(ichi_moku[0].shift(-26), ls="--", label="kenkansen")
plt.plot(ichi_moku[1].shift(-26), ls="--", label="kijunsen")
plt.plot(ichi_moku[2].shift(26), ls="--", label="leading_a")
plt.plot(ichi_moku[3].shift(26), ls="--", label="leading_b")
plt.fill_between(test_data["ncv"].index, ichi_moku[2], ichi_moku[3], ichi_moku[2] > ichi_moku[3], color="green", alpha=0.333)
plt.fill_between(test_data["ncv"].index, ichi_moku[2], ichi_moku[3], ichi_moku[2] < ichi_moku[3], color="red", alpha=0.333)
plt.plot(ichi_moku[4].shift(-26), ls="--", label="chikou")
plt.legend()
plt.show()

#%%
