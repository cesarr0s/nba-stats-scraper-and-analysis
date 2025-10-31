import pandas as pd
import requests
import time
import numpy as np
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

pio.renderers.default = "browser"

# Pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 50)

# Initialize empty DataFrame
table_headers = None
df_cols = None
df = pd.DataFrame()

data = pd.read_excel('nba_stats.xlsx')

data.drop(columns=['RANK', 'EFF'], inplace=True)#drop unneeded columns
data['season_start_year'] = data['Year'].str[:4].astype(int)#extract starting year as int
#print(data.TEAM.unique())
data['Season_type'] = data['Season_type'].replace('Regular%20Season', 'Regular Season')#clean season type names
rs_df = data[data['Season_type'] == 'Regular Season']#get regular season data
playoffs_df = data[data['Season_type'] == 'Playoffs']#geta playoffs data
#print(data.columns)
total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 
              'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']#columns to sum and calculate per minute stats
#print(data.corr())

data_per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum().reset_index()
for col in data_per_min.columns[4:]:
    data_per_min[col] = data_per_min[col] / data_per_min['MIN']
    
#create detailed per min stats
data_per_min['FG%'] = data_per_min['FGM'] / data_per_min['FGA']
data_per_min['3PT%'] = data_per_min['FG3M'] / data_per_min['FG3A']
data_per_min['FT%'] = data_per_min['FTM'] / data_per_min['FTA']
data_per_min['FG3A%'] = data_per_min['FG3M'] / data_per_min['FGA']
data_per_min['PTS/FGA'] = data_per_min['PTS'] / data_per_min['FGA']
data_per_min['FG3M/FGM'] = data_per_min['FG3M'] / data_per_min['FGM']
data_per_min['FTA/FGM'] = data_per_min['FTA'] / data_per_min['FGM']
data_per_min['TRU%'] = .5*data_per_min['PTS'] / (data_per_min['FGA'] + .475*data_per_min['FTA'])
data_per_min['AST_TOV'] = data_per_min['AST'] / data_per_min['TOV']

data_per_min.drop(columns=['PLAYER_ID', 'Year', 'PLAYER' ], inplace=True)#drop unneeded columns
data_per_min = data_per_min[data_per_min['MIN'] >= 50]#filter players with less than 50 minutes played


# #Create a heatmap
# plt.figure(figsize=(12,10))
# sns.heatmap(data_per_min.corr(), annot=True, fmt=".2f", cmap='coolwarm', square=True)
# plt.title("Correlation Matrix of Per Minute Stats")
# plt.show()

# fig = px.histogram(x=rs_df['MIN'], histnorm = 'percent') #minutes played in season vs percent of players
# fig.update_layout(bargap=0.1, xaxis_title_text='Minutes Played in Season', yaxis_title_text='Percent of Players',)
# fig.show()

# def hist_data(df=rs_df, min_MIN=0, min_GP=0):#function to get histogram data with min minutes and min games played filters
#     return df.loc[(df['MIN']>=min_MIN) & (df['GP']>=min_GP), 'MIN']/\
#     df.loc[(df['MIN']>=min_MIN) & (df['GP']>=min_GP), 'GP']
# fig = go.Figure()

# fig.add_trace(go.Histogram(x=hist_data(rs_df,50,5), histnorm='percent', name='Regular Season',
#                            xbins={'start':0,'end':46,'size':1}))
# fig.add_trace(go.Histogram(x=hist_data(playoffs_df,5,1), histnorm='percent',
#                            name='Playoffs', xbins={'start':0,'end':46,'size':1}))
# fig.update_layout(barmode='overlay', xaxis_title_text='Minutes Per Game', yaxis_title_text='Percent of Players',)
# fig.update_traces(opacity=0.5)
# fig.show()

change_df = data.groupby('season_start_year')[total_cols].sum().reset_index()
change_df['POSS_est'] = change_df['FGA']-change_df['OREB']+change_df['TOV']+0.44*change_df['FTA']
change_df = change_df[list(change_df.columns[0:2])+['POSS_est']+list(change_df.columns[2:-1])]

change_df['FG%'] = change_df['FGM']/change_df['FGA']
change_df['3PT%'] = change_df['FG3M']/change_df['FG3A']
change_df['FT%'] = change_df['FTM']/change_df['FTA']
change_df['AST%'] = change_df['AST']/change_df['FGM']
change_df['FG3A%'] = change_df['FG3A']/change_df['FGA']
change_df['PTS/FGA'] = change_df['PTS']/change_df['FGA']
change_df['FG3M/FGM'] = change_df['FG3M']/change_df['FGM']
change_df['FTA/FGA'] = change_df['FTA']/change_df['FGA']
change_df['TRU%'] = 0.5*change_df['PTS']/(change_df['FGA']+0.475*change_df['FTA'])
change_df['AST_TOV'] = change_df['AST']/change_df['TOV']

#print(change_df)

change_per_48_df = change_df.copy()
for col in change_per_48_df.columns[2:18]:
    change_per_48_df[col] = (change_per_48_df[col] / change_per_48_df['MIN']) * 48 * 5
change_per_48_df.drop(columns='MIN', inplace=True)

fig = go.Figure()
for col in change_per_48_df.columns[1:]:
    fig.add_trace(go.Scatter(x=change_per_48_df['season_start_year'], y=change_per_48_df[col], name=col))
fig.update_layout(title='NBA League Stats Per 48 Minutes Over Time', xaxis_title='Season Starting Year', yaxis_title='Stat Per 48 Minutes')
fig.show()

change_per_100_df = change_df.copy()
for col in change_per_100_df.columns[3:18]:
    change_per_100_df[col] = (change_per_100_df[col] / change_per_100_df['POSS_est']) * 100
change_per_100_df.drop(columns=['MIN', 'POSS_est'], inplace=True)

fig = go.Figure()
for col in change_per_100_df.columns[1:]:
    fig.add_trace(go.Scatter(x=change_per_100_df['season_start_year'], y=change_per_100_df[col], name=col))
fig.update_layout(title='NBA League Stats Per 100 Possessions Over Time', xaxis_title='Season Starting Year', yaxis_title='Stat Per 100 Possessions')
fig.show()

# print(change_per_48_df)
# print(change_per_100_df)d