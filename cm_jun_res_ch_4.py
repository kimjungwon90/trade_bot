#%%
import os
import warnings

os.chdir("/home/chanmin/trade_bot")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import FinanceDataReader as fdr

import naver_crawler
import technicals

kospi_200 = pd.read_csv("./kospi_200_list/kospi_200_list.csv", header=None)


warnings.filterwarnings("ignore")

sns.set_style("white")

test_api = naver_crawler.naver_stock_crawler()
test_data = test_api.get_stock("069500").loc["2010-06-01":, :]

krx_list = fdr.StockListing("KRX")

#%%
money_index = technicals.money_flow_index(test_data["high"], test_data["low"], test_data["close"], test_data["vol"], period=21)
test_data["mfi"] = money_index
test_data["signal"] = np.nan
test_data["signal"][money_index < 10] = -1
test_data["signal"][money_index > 90] = +1
test_data.ffill(inplace=True)

backtest_rtn = np.log(1+(test_data["signal"] * test_data["chg%"].shift(-2))).rolling(5).mean()
backtest_rtn.cumsum().plot()
#%%
rsi_index = technicals.rsi(test_data["close"])
test_data["rsi"] = rsi_index
test_data["signal"] = np.nan
test_data["signal"][rsi_index < 20] = 1
test_data["signal"][rsi_index > 80] = -1
test_data["signal"].ffill(inplace=True)
test_data["test_rtn"] = test_data["signal"] * test_data["chg%"].shift(-2)
test_data["cumul"] = (1 + test_data["test_rtn"]).cumprod()
test_data["cumul"].plot()

#%%
stochastic_i = technicals.stochastic(test_data["close"], test_data["high"], test_data["low"])
test_data["stochastic_k"] = stochastic_i[0]
test_data["stochastic_d"] = stochastic_i[1]
test_data["stochastic_d_3"] = stochastic_i[2]
test_data["signal"] = np.nan
test_data["signal"][test_data["stochastic_d"] > 80] = -1
test_data["signal"][test_data["stochastic_d"] < 20] = + 1
test_data["signal"].ffill(inplace=True)
test_data["test_rtn"] = test_data["signal"] * test_data["chg%"].shift(-2)
test_data["cumul"] = (1 + test_data["test_rtn"]).cumprod()
test_data["cumul"].plot()
#%%
ichi_moku = technicals.ichimoku(test_data["hv"], test_data["lv"], test_data["ncv"])

df_test = pd.DataFrame()
df_test["close"] = test_data["ncv"]
df_test["kenkansen"] = ichi_moku[0] / df_test["close"]
df_test["kijunsen"] = ichi_moku[1] / df_test["close"]
df_test["leading_a"] = ichi_moku[2] / df_test["close"]
df_test["leading_b"] = ichi_moku[3] / df_test["close"]
df_test["cloud"] = (ichi_moku[2] > ichi_moku[3]).astype("int8")
# df_test["chikou"] = ichi_moku[4] / df_test["close"]
df_test["return"] = (df_test["close"] / df_test["close"].shift(1)).apply(np.log)
df_test["class"] = (df_test["return"] > 0).astype("int8").shift(-1)
df_test["close"] = df_test["close"] / df_test["close"]

df_test.dropna(inplace=True)

df_X = df_test.drop(["return", "class"], axis=1)
df_y = df_test["class"]

tree = RandomForestClassifier(max_depth=5, n_estimators=100)
tree.fit(df_X.loc[:"2016-12-31"], df_y[:"2016-12-31"])

y_hat = tree.predict_proba(df_X)
df_test["pos"] = tree.predict(df_X)
df_test.loc["2016-12-31":, "trade_return"] = df_test["pos"].shift() * df_test["return"].shift(-2)
df_test["trade_return"].cumsum().plot()




plt.figure(figsize=(12, 8))
plt.plot(test_data["ncv"], label="Close", color="black")
plt.plot(ichi_moku[0], ls="--", label="kenkansen", color="blue")
plt.plot(ichi_moku[1], ls="--", label="kijunsen")
plt.fill_between(test_data["ncv"].index, ichi_moku[2], ichi_moku[3], ichi_moku[2] > ichi_moku[3], color="green", alpha=0.333)
plt.fill_between(test_data["ncv"].index, ichi_moku[2], ichi_moku[3], ichi_moku[2] < ichi_moku[3], color="red", alpha=0.333)
plt.plot(ichi_moku[4], ls="--", label="chikou", color="purple")
plt.legend()
plt.show()

#%%
df_test.tail()
#%%
