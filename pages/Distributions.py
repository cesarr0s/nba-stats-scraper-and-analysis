import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data


@st.cache_data
def get_data():
    return load_data()

data = get_data()


rs_df = data[data['Season_type'] == 'Regular Season'] #create tables for each season type
playoffs_df = data[data['Season_type'] == 'Playoffs']

st.subheader("Total Minutes Played in a Season")
fig1 = go.Figure()#create histogram of minutes played vs percent of players
fig1.add_trace(go.Histogram(x=rs_df['MIN'], histnorm='percent'))
fig1.update_layout(bargap=0.1, xaxis_title='Minutes Played in Season',
                   yaxis_title='Percent of Players', height=400)
st.plotly_chart(fig1, use_container_width=True)#shows that few players exceed 3000 minutes. many g league or short term players in league

st.subheader("Minutes Per Game — Regular Season vs Playoffs")
min_MIN = st.slider("Min total minutes played filter", 0, 200, 50) #sliders to remove short contract/2 way players
min_GP  = st.slider("Min games played filter", 0, 20, 5)    

def hist_data(df, min_MIN, min_GP):
    mask = (df['MIN'] >= min_MIN) & (df['GP'] >= min_GP)#prepare table for new histogram, clean up and remove 2 way players
    return df.loc[mask, 'MIN'] / df.loc[mask, 'GP']

#overlay playoffs and regular season minutes per game to show how rotations change
#sliders to differentiate between 2 way and consistent players and remove bulk of cut/low quality players
#sliders on high showcase starter caliber player minutes, dist skews left rather than right
fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=hist_data(rs_df, min_MIN, min_GP), histnorm='percent',
                             name='Regular Season', xbins={'start': 0, 'end': 46, 'size': 1}))
fig2.add_trace(go.Histogram(x=hist_data(playoffs_df, min_MIN, min_GP), histnorm='percent',
                             name='Playoffs', xbins={'start': 0, 'end': 46, 'size': 1}))
fig2.update_layout(barmode='overlay', xaxis_title='Minutes Per Game', 
                   yaxis_title='Percent of Players', height=450)
fig2.update_traces(opacity=0.5)
st.plotly_chart(fig2, use_container_width=True)