# NBA Data Dashboard

## Overview

This project explores NBA player performance and league evolution using advanced statistical metrics and machine learning techniques.

It transforms raw NBA play-by-play data into interactive insights, including player archetype similarity, efficiency trends, and historical league-wide changes in style of play.

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
* Visualizes league-wide trends across multiple metrics

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

# Key Insights

* Three-point attempt rate have increased significantly over time, reflecting modern basketballs focus on spacing
* True Shooting % is a better indicator at determining a player's offensive efficiency

# Analytical Methods

* Per-48 minute normalization
* Per-100 Possession scaling
* True Shooting %
* Assist / Turnover Ratio
* Cosine similarity to find closest players
* Z score standardization for feature scaling

# Data  
* Data sourced from NBA stats API
* Collected both regular season and playoffs data

# Tech Stack
* Python
* Streamlit
* Pandas / Numpy
* Scikit-learn
* Plotly
