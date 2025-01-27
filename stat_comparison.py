# Import neccesary moduls
import pandas as pd
from data_processing import players

# Load data of players to compare with ML prediction
full_players_data = pd.read_csv('./Data Files/player_stats.csv')
actual_data = pd.read_csv('./Data Files/actual_data.csv')

predicted_data = pd.read_csv('./Data Files/predictions.csv')
pivoted_predicted_data = predicted_data.pivot(index='PLAYER_NAME',columns='STAT', values='PREDICTED_VALUE')

compared_data = pd.merge(actual_data, pivoted_predicted_data, on='PLAYER_NAME', suffixes=('_ACTUAL','_PREDICTED'))
# compared_data.to_excel('stats_for_comparison.xlsx',index=False)
# print('Data successfully saved to "stats_for_comparison.xlsx" file!')


def preds_to_list(player,df):
    player_data = df[df['PLAYER_NAME'] == player]
    stat_order = ['PTS','REB','AST','MIN']
    stats_list = [
        player_data[player_data["STAT"] == stat]["PREDICTED_VALUE"].iloc[0]
        for stat in stat_order
    ]
    return stats_list

def actuals_to_list(player,df):
    player_data = df[df['PLAYER_NAME'] == player]
    stats = player_data[['PTS','REB','AST','MIN']].iloc[0].tolist()

    return stats

def compare_stats(player,stat,predicted,actual,predicted_min,actual_min):
    min_diff = predicted_min - actual_min
    diff = predicted - actual
    stat_diff = abs(predicted - actual)
    abs_min_diff = abs(min_diff)
    if stat == 'Points':
        if diff > 1:
            if min_diff > 1:
                if predicted_min > actual_min:
                    message = f'{player} predicted({predicted}) {stat} average is {stat_diff:.2f} higher than real({actual}) average,but it may due because the predicted min average({predicted_min}) is higher({abs_min_diff:.2f}) than the real min average({actual_min})'
            elif 1 >= min_diff >= -1:
                message = f"{player}'s predicted {stat} average ({predicted}) is {stat_diff:.2f} higher than the actual value ({actual}). This might indicate a potential inconsistency in performance metrics or a situational factor affecting play. Although the predicted minutes ({predicted_min}) closely align with the actual minutes ({actual_min}), reviewing recent gameplay or lineup adjustments could provide valuable insights into this disparity."
            elif min_diff < -1:
                message = f"{player}'s predicted {stat} average ({predicted}) is {stat_diff:.2f} higher than the actual average ({actual}). However, the actual minutes average ({actual_min}) exceeds the predicted average ({predicted_min}) by {abs_min_diff:.2f}, which might indicate adjustments in the team lineup or a shift in the player's playstyle."
        elif  -1 <= diff <= 1:
            message = f'{player} predicted {stat} average {predicted} is almost the same as the actual value {actual}.It was a good prediction!'
        elif diff < -1:
            if min_diff > 1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is {abs_min_diff:.2f} higher than actual min averages.The player improved in {stat} segment!'
            elif -1 < min_diff < 1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is almost the same as the actual min averages.The player improved in {stat} segment!'
            elif min_diff < -1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is {abs_min_diff:.2f} lower than actual min averages.So the player played more minutes it my be the reason for the higher {stat} average.'
    elif stat == 'Rebounds' or stat =='Assist':
        if diff > 0.5:
            if min_diff > 1:
                if predicted_min > actual_min:
                    message = f'{player} predicted({predicted}) {stat} average is {stat_diff:.2f} higher than real({actual}) average,but it may due because the predicted min average({predicted_min}) is higher({abs_min_diff:.2f}) than the real min average({actual_min})'
            elif 1 >= min_diff >= -1:
                message = f"{player}'s predicted {stat} average ({predicted}) is {stat_diff:.2f} higher than the actual value ({actual}). This might indicate a potential inconsistency in performance metrics or a situational factor affecting play. Although the predicted minutes ({predicted_min}) closely align with the actual minutes ({actual_min}), reviewing recent gameplay or lineup adjustments could provide valuable insights into this disparity."
            elif min_diff < -1:
                message = f"{player}'s predicted {stat} average ({predicted}) is {stat_diff:.2f} higher than the actual average ({actual}). However, the actual minutes average ({actual_min}) exceeds the predicted average ({predicted_min}) by {abs_min_diff:.2f}, which might indicate adjustments in the team lineup or a shift in the player's playstyle."
        elif  -0.5 <= diff <= 0.5:
            message = f'{player} predicted {stat} average {predicted} is almost the same as the actual value {actual}.It was a good prediction!'
        elif diff < -0.5:
            if min_diff > 1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is {abs_min_diff:.2f} higher than actual min averages.The player improved in {stat} segment!'
            elif -1 < min_diff < 1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is almost the same as the actual min averages.The player improved in {stat} segment!'
            elif min_diff < -1:
                message = f'{player} actual {stat} average is higher,but predicted minute average is {abs_min_diff:.2f} lower than actual min averages.So the player played more minutes it my be the reason for the higher {stat} average.'
    return message




def generate_messages(players, predicted_data, actual_data):
    messages = {}

    for player in players:
        pred_values = preds_to_list(player, predicted_data)
        actual_values = actuals_to_list(player, actual_data)

        pred_points, pred_rebs, pred_ast, pred_mins = pred_values
        actual_points, actual_rebs, actual_ast, actual_mins = actual_values

        
        point_msg = compare_stats(player, 'Points', pred_points, actual_points, pred_mins, actual_mins)
        reb_msg = compare_stats(player, 'Rebounds', pred_rebs, actual_rebs, pred_mins, actual_mins)
        ast_msg = compare_stats(player, 'Assist', pred_ast, actual_ast, pred_mins, actual_mins)

        
        messages[player] = {
            'Points': point_msg,
            'Rebounds': reb_msg,
            'Assist': ast_msg,
        }

    return messages


messages = generate_messages(players, predicted_data, actual_data)


for player, stats in messages.items():
    print(f"Messages for {player}:")
    for stat, msg in stats.items():
        print(f"  {stat}: {msg}")


with open("comparison_results.txt", "w") as file:
    for player, stats in messages.items():
        file.write(f"Messages for {player}:\n")
        for stat, msg in stats.items():
            file.write(f"  {stat}: {msg}\n")
        file.write("\n")  
