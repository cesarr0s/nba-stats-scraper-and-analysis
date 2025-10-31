import pandas as pd
import requests
import time
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 50)

table_headers = None
df_cols = None
df = pd.DataFrame()

#years and season types for url
years = ['2014-15', '2015-16', '2016-17', '2017-18',
         '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
season_types = ['Regular%20Season', 'Playoffs']

#mimic browser
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

#loop through years and season types
for y in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'#url to loop through
        try:
            r = requests.get(api_url, headers=headers, timeout=10).json()
        except Exception as e:
            print(f"Request failed for {y} - {s}: {e}")
            continue

        #result set contains the data in the website
        if 'resultSet' not in r:
            print(f"Warning: 'resultSet' missing for {y} - {s}")
            continue
        if not r['resultSet']['rowSet']:
            print(f"No data for {y} - {s}")
            continue

        #copy headers from resultset data to main df, and create columns year and season type
        if table_headers is None:
            table_headers = r['resultSet']['headers']
            df_cols = ['Year', 'Season_type'] + table_headers
            df = pd.DataFrame(columns=df_cols)

        #build temp df for each request
        temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
        temp_df2 = pd.DataFrame({'Year': [y]*len(temp_df1), 'Season_type': [s]*len(temp_df1)})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)

        #append to main df
        df = pd.concat([df, temp_df3], axis=0, ignore_index=True)

        print(f"Completed data for {y} - {s}")

        #sleep random time to avoid being blocked
        lag = np.random.uniform(5, 40)
        print(f"Sleeping for {lag:.2f} seconds...")
        #time.sleep(lag)

#excel
df.to_excel('nba_stats.xlsx', index=False)
print("Process completed!")
data = pd.read_excel('nba_stats.xlsx')