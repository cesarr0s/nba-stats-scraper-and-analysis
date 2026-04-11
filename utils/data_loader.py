from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "nba_stats.csv"

def load_data():
    data = pd.read_csv(DATA_PATH, low_memory=False)

    # clean once, everywhere
    data.drop(columns=['RANK', 'EFF'], inplace=True, errors='ignore')
    data['season_start_year'] = data['Year'].str[:4].astype(int)
    data['Season_type'] = data['Season_type'].replace('Regular%20Season', 'Regular Season')

    return data