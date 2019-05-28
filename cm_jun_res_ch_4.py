#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import naver_crawler
import technicals

sns.set_style("white")

test_api = naver_crawler.naver_stock_crawler()
test_data = test_api.get_stock("069500").loc["2010-06-01":, :]

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
