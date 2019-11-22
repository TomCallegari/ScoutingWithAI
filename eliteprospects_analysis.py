#%%
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np

#%%
meta = pd.read_csv('meta_stats_test.csv')
player = pd.read_csv('yearly_player_stats_test.csv')

#%%
meta.info()
meta.head()

#%%
player.info()
player.head()

#%%
x = meta['height']
y = meta['weight']
plt.scatter(x, y)
plt.show()

#%%
player = player.replace('-', np.NaN)

#%%
player['games_played'] = player.fillna(player['games_played'].mean(), inplace=True)

#%%
x = player['games_played']
y = player['goals']
player.head()

#%%
plt.scatter(x, y)
plt.show()