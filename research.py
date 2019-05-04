#%%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from fisis_api import fisis_api
import fin_data_clean as dc
from naver_crawler import naver_stock_crawler as naver

sns.set()
sns.set_style("white")
#%%
naver_api = naver()
test_api = fisis_api()
accounts = pd.read_csv("./fisis_core/accounts.csv")
comps_list = pd.read_csv("./fisis_core/comps_list.csv")

#%%
res = test_api.get_data("0010927", "SA024", "Q", "200812", "201812")
df_test = pd.DataFrame(res).pivot(index="base_month", columns="account_nm", values="a")
df_test.index = pd.to_datetime(df_test.index, format="%Y%m")
df_test.index = dc.accounting_offset(df_test.index)
df_test.replace(" ", np.nan, inplace=True)
df_test = df_test.astype("float64")
naver_api.get_stock(code="105560")

#%%
df_test.columns

#%%
ax1 = naver_api.data.loc["2008-10-10":, "ncv"].astype("float64").plot()
ax2 = ax1.twinx()
df_test.astype("float64").rolling(4).sum()["총당기순이익"].plot(ax=ax2)


#%%
