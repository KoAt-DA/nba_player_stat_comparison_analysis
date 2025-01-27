# import neccessary moduls

import pandas as pd
from sqlalchemy import create_engine
from decouple import config

# SQL connection,data loading and filter to players
db_url = config('DB_URL')
engine = create_engine(db_url)

query = """
    SELECT 
        "player_name",
        "pts",
        "reb",
        "ast",
        "season"
    FROM "nba_dataset"
    WHERE "player_name" IN ('LeBron James', 'Stephen Curry', 'Shai Gilgeous-Alexander', 'Giannis Antetokounmpo', 'Luka Doncic','Kevin Durant','Jayson Tatum','Chris Paul')
"""

players_filtered_data = pd.read_sql(query,engine)

players_full_data = pd.read_csv('./Data Files/player_stats.csv')
actual_data = players_full_data[players_full_data['SEASON'] == '2023-24']
filtered_actual_data = actual_data[['PLAYER_NAME','PTS','REB','AST','MIN']]
filtered_actual_data.to_csv('actual_data.csv',index=False)


# data filtering for to analysis and ML

players = ['LeBron James', 
           'Stephen Curry', 
           'Shai Gilgeous-Alexander', 
           'Giannis Antetokounmpo', 
           'Luka Doncic',
           'Kevin Durant',
           'Jayson Tatum',
           'Chris Paul']


players_data = {player: players_filtered_data[players_filtered_data['player_name'] == player] for player in players}
player_mins = {player: players_full_data[players_full_data['PLAYER_NAME'] == player] for player in players}

players_points = {
    'LeBron James' : players_data['LeBron James']['pts'].tolist(),
    'Stephen Curry' : players_data['Stephen Curry']['pts'].tolist(),
    'Shai Gilgeous-Alexander' : players_data['Shai Gilgeous-Alexander']['pts'].tolist(),
    'Giannis Antetokounmpo' : players_data['Giannis Antetokounmpo']['pts'].tolist(),
    'Luka Doncic' : players_data['Luka Doncic']['pts'].tolist(),
    'Kevin Durant' : players_data['Kevin Durant']['pts'].tolist(),
    'Jayson Tatum' : players_data['Jayson Tatum']['pts'].tolist(),
    'Chris Paul' : players_data['Chris Paul']['pts'].tolist()
}

players_rebounds = {
    'LeBron James' : players_data['LeBron James']['reb'].tolist(),
    'Stephen Curry' : players_data['Stephen Curry']['reb'].tolist(),
    'Shai Gilgeous-Alexander' : players_data['Shai Gilgeous-Alexander']['reb'].tolist(),
    'Giannis Antetokounmpo' : players_data['Giannis Antetokounmpo']['reb'].tolist(),
    'Luka Doncic' : players_data['Luka Doncic']['reb'].tolist(),
    'Kevin Durant' : players_data['Kevin Durant']['reb'].tolist(),
    'Jayson Tatum' : players_data['Jayson Tatum']['reb'].tolist(),
    'Chris Paul' : players_data['Chris Paul']['reb'].tolist()
}

players_assists = {
    'LeBron James' : players_data['LeBron James']['ast'].tolist(),
    'Stephen Curry' : players_data['Stephen Curry']['ast'].tolist(),
    'Shai Gilgeous-Alexander' : players_data['Shai Gilgeous-Alexander']['ast'].tolist(),
    'Giannis Antetokounmpo' : players_data['Giannis Antetokounmpo']['ast'].tolist(),
    'Luka Doncic' : players_data['Luka Doncic']['ast'].tolist(),
    'Kevin Durant' : players_data['Kevin Durant']['ast'].tolist(),
    'Jayson Tatum' : players_data['Jayson Tatum']['ast'].tolist(),
    'Chris Paul' : players_data['Chris Paul']['ast'].tolist()
}

players_mins = {
    'LeBron James' : player_mins['LeBron James']['MIN'].tolist()[0:-1],
    'Stephen Curry' : player_mins['Stephen Curry']['MIN'].tolist()[0:-1],
    'Shai Gilgeous-Alexander' : player_mins['Shai Gilgeous-Alexander']['MIN'].tolist()[0:-1],
    'Giannis Antetokounmpo' : player_mins['Giannis Antetokounmpo']['MIN'].tolist()[0:-1],
    'Luka Doncic' : player_mins['Luka Doncic']['MIN'].tolist()[0:-1],
    'Kevin Durant' : player_mins['Kevin Durant']['MIN'].tolist()[0:-1],
    'Jayson Tatum' : player_mins['Jayson Tatum']['MIN'].tolist()[0:-1],
    'Chris Paul' : player_mins['Chris Paul']['MIN'].tolist()[0:-1]
}

if __name__ == "__main__":
    players_points
    players_rebounds
    players_assists
    players_mins
    players
