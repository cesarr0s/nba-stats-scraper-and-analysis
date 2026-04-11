import streamlit as st

st.set_page_config(page_title="NBA Stats Dashboard", layout="wide")

def home():
    st.title("NBA Stats Dashboard")

    st.markdown("""
    Welcome to the NBA Stats Dashboard. Use the sidebar to navigate between pages. Data goes back to the 1996-97 season and up to the 2025-26 season.

    - **Player Similarity** — Find players most similar to any player in the dataset
    - **League Trends** — Track how the league has changed over time
    - **Player Stats** — Explore individual player career stats
    - **Distributions** — Minutes played distributions across the league
    - **Correlation** — Heatmap of stat correlations

    ## Links
    - GitHub: https://github.com/cesarr0s
    - LinkedIn: https://www.linkedin.com/in/demetriorosales
    - Website: https://nbastatsdashboard.streamlit.app
    """)

home_page = st.Page(home, title="Home")

similarity = st.Page("pages/Similarity.py", title="Similarity")
trends = st.Page("pages/League_Trends.py", title="League Trends")
stats = st.Page("pages/Player_Stats.py", title="Player Stats")
dist = st.Page("pages/Distributions.py", title="Distributions")
corr = st.Page("pages/Correlations.py", title="Correlation")

pg = st.navigation([
    home_page,
    similarity,
    trends,
    stats,
    dist,
    corr
])

pg.run()