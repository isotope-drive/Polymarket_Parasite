import pandas as pd 
import matplotlib.pyplot as plt
from collector import BASE_PATH

PRICE_PLOT_KWARGS = {"xlim": (0,1)}


df = pd.read_parquet(f"{BASE_PATH}/data/dataframe.parquet")

print(df.head())
print(df.info())


event1 = df.loc[df.event_id == 0]

print(event1.head())

#event1.loc["size"].describe()



#testdf.plot.scatter(x="price", y="size", **PRICE_PLOT_KWARGS)

#testdf['mean'] = (testdf['price']*testdf['size'] / len(testdf))



#print(testdf['mean'])
 
#plt.show()