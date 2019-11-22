#%%
import pandas as pd
import matplotlib.pyplot as plt

#%%
meta = pd.read_csv('meta_stats_test.csv')
player = pd.read_csv('yearly_player_stats_test.csv')

#%%
meta.info()
meta.head()

#%%
plt.hist(meta['height'], bins='auto')
plt.title('Historgram of player heights')
plt.show()

#%%
plt.hist(meta['weight'], bins='auto')
plt.title('Histogram of player weights')
plt.show()

#%%
player.info()
player.head()