import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
from utils.data_loader import load_data


@st.cache_data
def get_data():
    return load_data()

data = get_data()
rs_df = data[data['Season_type'] == 'Regular Season']

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
              'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']
st.title("Player Similarity")

mode = st.radio("Compare by", ["Career (All Seasons)", "Single Season"])
if mode == "Single Season":
    all_years = sorted(rs_df['Year'].unique())
    selected_year = st.selectbox("Select season", all_years)
    filtered_df = rs_df[rs_df['Year'] == selected_year]
else:
    selected_year = None
    filtered_df = rs_df

@st.cache_data
def build_per_min(df, min_threshold):
    per_min = df.groupby(['PLAYER', 'PLAYER_ID'])[total_cols].sum().reset_index()
    per_min = per_min[per_min['MIN'] >= min_threshold]
    for col in total_cols[1:]:
        per_min[col] = per_min[col] / per_min['MIN']
    per_min['FG%']      = per_min['FGM'] / per_min['FGA']
    per_min['3PT%']     = per_min['FG3M'] / per_min['FG3A']
    per_min['FT%']      = per_min['FTM'] / per_min['FTA']
    per_min['FG3A%']    = per_min['FG3A'] / per_min['FGA']
    per_min['FG3M/FGM'] = per_min['FG3M'] / per_min['FGM']
    per_min['FTA/FGM']  = per_min['FTA'] / per_min['FGM']
    per_min['TRU%']     = 0.5 * per_min['PTS'] / (per_min['FGA'] + 0.475 * per_min['FTA'])
    per_min['AST_TOV']  = per_min['AST'] / per_min['TOV']
    per_min = per_min.replace([np.inf, -np.inf], np.nan)
    per_min = per_min.fillna(0)
    return per_min

min_threshold = 500 if mode == "Career (All Seasons)" else 300
per_min = build_per_min(filtered_df, min_threshold)

feature_cols = ['PTS', 'AST', 'OREB', 'DREB', 'STL', 'BLK', 'TOV',
                'FG%', '3PT%', 'FT%', 'FG3A%', 'TRU%', 'AST_TOV']

def get_similar_players(player_name, n=10):
    features = per_min[feature_cols].copy()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    sim_matrix = cosine_similarity(scaled)
    sim_df = pd.DataFrame(sim_matrix, index=per_min['PLAYER'], columns=per_min['PLAYER'])
    scores = sim_df[player_name].drop(player_name).sort_values(ascending=False).head(n)
    return scores

all_players = sorted(per_min['PLAYER'].unique())
selected_player = st.selectbox("Select a Player", all_players)
n_similar = st.slider("Number of similar players", 5, 20, 10)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Most Similar to {selected_player}")
    similar = get_similar_players(selected_player, n_similar)
    result_df = similar.reset_index()
    result_df.columns = ['Player', 'Similarity Score']
    result_df['Similarity Score'] = (result_df['Similarity Score'] * 100).round(1).astype(str) + '%'  
    st.dataframe(result_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Stat Comparison (per minute)")
    compare_players = [selected_player] + similar.index[:4].tolist()
    compare_df = per_min[per_min['PLAYER'].isin(compare_players)].set_index('PLAYER')
    radar_cols = ['PTS', 'AST', 'OREB', 'DREB', 'STL', 'BLK', 'FG%', 'TRU%']
    fig = go.Figure()
    for player in compare_players:
        if player in compare_df.index:
            vals = compare_df.loc[player, radar_cols].tolist()
            vals += vals[:1]
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=radar_cols + [radar_cols[0]],
                fill='toself', name=player, opacity=0.6
            ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=450)
    st.plotly_chart(fig, use_container_width=True)

label = "Career Per-Game Stats" if mode == "Career (All Seasons)" else f"{selected_year} Per-Game Stats"
st.subheader(f"{selected_player} — {label}")
player_mins = filtered_df[filtered_df['PLAYER'] == selected_player]['MIN'].sum()
player_gp = filtered_df[filtered_df['PLAYER'] == selected_player]['GP'].sum()
mpg = player_mins / player_gp

player_row = per_min[per_min['PLAYER'] == selected_player][feature_cols].copy()
counting_stats = ['PTS', 'AST', 'OREB', 'DREB', 'STL', 'BLK', 'TOV']
player_row[counting_stats] = player_row[counting_stats] * mpg
percent_stats = ['FG%', '3PT%', 'FT%', 'FG3A%', 'TRU%']
player_row[percent_stats] = player_row[percent_stats] * 100
player_row = player_row.rename(columns={
    'PTS': 'Points', 'AST': 'Assists', 'OREB': 'Offensive Rebounds',
    'DREB': 'Defensive Rebounds', 'STL': 'Steals', 'BLK': 'Blocks',
    'TOV': 'Turnovers', 'FG%': 'FG%', 'FG3A%': '3PA Rate',
    'TRU%': 'True Shooting%', 'AST_TOV': 'AST/TOV'
})
st.dataframe(player_row.round(2), use_container_width=True, hide_index=True)