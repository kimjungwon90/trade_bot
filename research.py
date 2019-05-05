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
plt.figure(figsize=(30,30))
df_growth = df_test.dropna(how="any", axis=1).pct_change()
df_growth.loc["2011-05-15"] = df_growth.mean(axis=0)
sns.clustermap(df_growth.dropna(axis=0).corr(), annot=False, method="complete")
plt.show()

#%%
df_growth
#%%
ax1 = df_test["총당기순이익"].plot(c="red", marker="*")
ax2 = ax1.twinx()
ax2 = df_test["법인세비용차감전순이익"].plot(c="blue", marker="+")
plt.legend()
plt.show()

ax1 = df_test.pct_change()["총당기순이익"].plot(c="red", marker="*")
plt.ylabel("net_profit")
ax2 = ax1.twinx()
ax2 = df_test.pct_change()["법인세비용차감전순이익"].plot(c="blue", marker="+")
plt.ylabel("pre_tax_profit")
plt.legend()
plt.show()
#%%

banks_names = comps_list[comps_list["cate_1"] == "국내은행"]["finance_cd"]

#%%
banks_data = dict()
for name in banks_names:
    print(name)
    try:
        data = test_api.get_data(name, "SA023", "Q", "200812", "201812")
        data = pd.DataFrame(data)
        new_df = data.pivot(index="base_month", columns="account_nm", values="a")
        new_df.index = pd.to_datetime(new_df.index, format="%Y%m")
        new_df.index = dc.accounting_offset(new_df.index)
        new_df.replace(" ", np.nan, inplace=True)
        new_df = new_df.astype("float64")
        banks_data[name][stat] = new_df
    except Exception as e:
        print(e)
        pass


#%%
df_concat = pd.concat(banks_data, axis=1, names=["comp", "stat", "acc"])

#%%
plt.figure(figsize=(20, 16))
df_concat.sum(level="acc", axis=1).pct_change().corr().to_csv("./test.xlsx")



#%%
stats_df = pd.read_csv("./fisis_core/stats_list.csv")

#%%
stats = stats_df[stats_df["lrg_div_nm"] == "국내은행"]["list_no"]
#%%
len(banks_names)

#%%
df_concat

#%%
banks_data

#%%
banks_data

#%%
