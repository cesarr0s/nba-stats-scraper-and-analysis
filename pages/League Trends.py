import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="League Trends", layout="wide")
st.title("NBA League Trends Over Time")

from utils.data_loader import load_data


@st.cache_data
def get_data():
    return load_data()

data = get_data()

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
              'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']

@st.cache_data
def build_change_df(data):
    change_df = data.groupby('season_start_year')[total_cols].sum().reset_index()#df to calculate change in stats
    change_df['POSS_est'] = change_df['FGA'] - change_df['OREB'] + change_df['TOV'] + 0.44 * change_df['FTA']#create poss using KENPOM formula
    change_df['FG%']      = change_df['FGM'] / change_df['FGA']#create new stats from previous ones collected
    change_df['3PT%']     = change_df['FG3M'] / change_df['FG3A']
    change_df['FT%']      = change_df['FTM'] / change_df['FTA']
    change_df['AST%']     = change_df['AST'] / change_df['FGM']
    change_df['FG3A%']    = change_df['FG3A'] / change_df['FGA']
    change_df['PTS/FGA']  = change_df['PTS'] / change_df['FGA']
    change_df['FG3M/FGM'] = change_df['FG3M'] / change_df['FGM']
    change_df['FTA/FGA']  = change_df['FTA'] / change_df['FGA']
    change_df['TRU%']     = 0.5 * change_df['PTS'] / (change_df['FGA'] + 0.475 * change_df['FTA'])
    change_df['AST_TOV']  = change_df['AST'] / change_df['TOV']
    return change_df

change_df = build_change_df(data)

# Per 48 minutes
tab1, tab2 = st.tabs(["Per 48 Minutes", "Per 100 Possessions"])#2 different tables will be displayed

with tab1:
    per48 = change_df.copy()
    for col in per48.columns[2:18]:
        per48[col] = (per48[col] / per48['MIN']) * 48 * 5 # (total stats/total minutes) * 48 for a full game * 5 for a full team
    per48.drop(columns='MIN', inplace=True)

    selected_stats = st.multiselect("Select stats to display",  #create dropdown
                                     options=list(per48.columns[1:]),
                                     default=['PTS', 'AST', 'FG3A'])
    fig = go.Figure()
    for col in selected_stats:#display selected stats above
        fig.add_trace(go.Scatter(x=per48['season_start_year'], y=per48[col], name=col))
    fig.update_layout(title='NBA League Stats Per 48 Minutes Over Time',
                      xaxis_title='Season Starting Year', yaxis_title='Stat Per 48 Minutes', height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    per100 = change_df.copy()
    for col in per100.columns[3:18]:
        per100[col] = (per100[col] / per100['POSS_est']) * 100 #same thing, but (totoal stats/estimated possession) * 100 posessions
    per100.drop(columns=['MIN', 'POSS_est'], inplace=True)

    selected_stats2 = st.multiselect("Select stats to display",#create variables for dropdown
                                      options=list(per100.columns[1:]),
                                      default=['PTS', 'AST', 'FG3A'],
                                      key='per100')
    fig2 = go.Figure()
    for col in selected_stats2:
        fig2.add_trace(go.Scatter(x=per100['season_start_year'], y=per100[col], name=col))#display selected values over 100 poss in chart
    fig2.update_layout(title='NBA League Stats Per 100 Possessions Over Time',
                       xaxis_title='Season Starting Year', yaxis_title='Stat Per 100 Possessions', height=500)
    st.plotly_chart(fig2, use_container_width=True)