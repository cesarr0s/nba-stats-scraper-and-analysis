import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.data_loader import load_data


@st.cache_data
def get_data():
    return load_data()

data = get_data()

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
              'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']

def build_per_min(data):
    per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum().reset_index()
    for col in per_min.columns[4:]:
        per_min[col] = per_min[col] / per_min['MIN'] #normalize each stat to per minute
    per_min['FG%']      = per_min['FGM'] / per_min['FGA'] #create new stats using previous ones
    per_min['3PT%']     = per_min['FG3M'] / per_min['FG3A']
    per_min['FT%']      = per_min['FTM'] / per_min['FTA']
    per_min['FG3A%']    = per_min['FG3M'] / per_min['FGA']
    per_min['PTS/FGA']  = per_min['PTS'] / per_min['FGA']
    per_min['FG3M/FGM'] = per_min['FG3M'] / per_min['FGM']
    per_min['FTA/FGM']  = per_min['FTA'] / per_min['FGM']
    per_min['TRU%']     = 0.5 * per_min['PTS'] / (per_min['FGA'] + 0.475 * per_min['FTA']) #use true shooting% formula, .5P / FG + .475*FTA
    per_min['AST_TOV']  = per_min['AST'] / per_min['TOV']
    per_min = per_min[per_min['MIN'] >= 50].drop(columns=['PLAYER_ID', 'Year', 'PLAYER'])#remove players that dont play
    return per_min.dropna()

per_min = build_per_min(data)
corr = per_min.corr()

fig = go.Figure(data=go.Heatmap(#create interactive correlation heatmap
    z=corr.values,
    x=corr.columns.tolist(),
    y=corr.columns.tolist(),
    colorscale='RdBu',
    zmid=0,
    text=np.round(corr.values, 2),
    texttemplate="%{text}",
    textfont={"size": 9},
))
fig.update_layout(title="Correlation Matrix", height=700, width=700)
st.plotly_chart(fig, use_container_width=True)