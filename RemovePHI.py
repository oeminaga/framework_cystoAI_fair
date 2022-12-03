#%%
import pandas as pd
#%%
data=pd.read_csv("../CystoNetDatabase_2019_Current/SummaryReportImages.csv")
# %%
import datetime
from collections import defaultdict 
data_ = defaultdict(list)
for rows in data.groupby("ID"):
    pass
    '''
    x = rows[0]
        k = x["ID"]
        date_b = x.DATE"].unique()

        data_[k].append(datetime.datetime.strptime(str(k[1].DATE.unique()[0]), "%m%d%Y"))
    '''

# %%
data_
# %%
