import streamlit as st

st.set_page_config(page_title="NBA Stats Dashboard", layout="wide")
st.title("NBA Stats Dashboard")
st.markdown("""
Welcome to the NBA Stats Dashboard. Use the sidebar to navigate between pages. Data goes back to the 1996-97 season and up to the 2025-26 season.

- **Player Similarity** — Find players most similar to any player in the dataset
- **League Trends** — Track how the league has changed over time
- **Player Stats** — Explore individual player career stats
- **Distributions** — Minutes played distributions across the league
- **Correlation** — Heatmap of stat correlations
""")