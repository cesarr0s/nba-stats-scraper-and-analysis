import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Player Stats", layout="wide")
st.title("Player Career Stats")

from utils.data_loader import load_data


@st.cache_data
def get_data():
    return load_data()

data = get_data()
rs_df = data[data['Season_type'] == 'Regular Season']

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
              'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']

all_players = sorted(rs_df['PLAYER'].unique())

col1, col2 = st.columns([1, 3])
with col1:
    default_players = ['LeBron James', 'Kevin Durant', 'Stephen Curry', 'Kobe Bryant', 'Dwyane Wade']
    selected_players = st.multiselect(
        "Select players",
        options=all_players,
        default=[p for p in default_players if p in all_players]
    )
    selected_stats = st.multiselect("Select stats", total_cols, default=['PTS'])

with col2:
    if selected_players and selected_stats:
        fig = go.Figure()
        for player in selected_players:
            ps = rs_df[rs_df['PLAYER'] == player].sort_values('season_start_year')
            for stat in selected_stats:
                fig.add_trace(go.Scatter(
                    x=ps['season_start_year'], y=ps[stat],
                    name=f'{player} — {stat}',
                    mode='lines+markers',
                    hovertemplate=f'<b>{player}</b><br>{stat}: %{{y}}<br>Season: %{{x}}<extra></extra>'#so stat doesnt get cut off
                ))
        fig.update_layout(title='Player Stats Over Seasons',
                            xaxis_title='Season', 
                            yaxis_title='Stat', 
                            height=500,
                            xaxis=dict(
                                tickmode='linear',
                                tick0=rs_df['season_start_year'].min(),
                                dtick=1#so no 2024.5 pops up
                            )
                ) 
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one player and one stat.")