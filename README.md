# NBA Data Dashboard

This project is an interactive NBA analytics dashboard built with Streamlit, featuring player comparison tools, league-wide trend analysis, statistical visualizations, and a player similarity engine using machine learning.

It processes NBA player data from the 1996–2025 seasons and transforms it into advanced basketball metrics and insights. 

# Link
https://nbastatsdashboard.streamlit.app/

# Features
## Player Similarity

* Finds statistically similar players using cosine similarity
* Includes interactive radar charts and a customizable list of most similar players
* Uses standardized per-minute stats to determine playstyles while applying a minutes threshold

## League Trends

* Tracks how the NBA has changed over time
* Compare trends in per-48 minutes and per-100 possession metrics
* Showcases trends in multiple high level stats

## Player Stats

* View career or single season stats
* Compare multiple players over time
* Interactive visuals for each stat

## Distributions

* Minutes played distribution
* Compare rotations in regular season vs playoffs
* Filter rotation level players

## Correlations

* Shows relationships between major stats
* Identifies stat dependencies

# Analytical Methods

* Per-48 minute normalization
* Per-100 Posession scaling
* True Shooting %
* Assist / Turnover Ratio
* Cosine similarity to find closest players
* Z score standardization for feature scaling

# Data  
* Data sourced from Nba.com/stats API
* Collected both regular season and playoffs data

# Tech Stack
* Python
* Streamlit
* Pandas / Numpy
* Scikit-learn
* Plotly