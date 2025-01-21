# import neccessary modules
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from data_processing import players_points,players_rebounds,players_assists,players_mins,players


predictions = []

# Data processing and Model training

for player in players:
    for stat_type,stat_data in {"PTS" : players_points, "REBS" : players_rebounds, "AST" : players_assists, "MIN" : players_mins}.items():
        y = np.array(stat_data[player])
        X = np.arange(1, len(y) + 1).reshape(-1, 1)


        # Train model

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train,y_train)

        y_pred = model.predict(X_test)
        
        next_season = [[X[-1][0] + 1]] 
        next_season_prediction = model.predict(next_season)

        predictions.append({
            "PLAYER_NAME" : player,
            "STAT" : stat_type,
            "PREDICTED_VALUE" : round(next_season_prediction[0], 2)
        })

predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv('predictions.csv',index=False)

print('The "predictions.csv" file created succesfully!')




