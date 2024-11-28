import numpy as np
import os
import json

import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from utilities import *

# get impact factors for each indicator (weights)
# input: {"league_name": string, "team_name": string, "team_id": int}
# output: {"team_info": {"team_type": string, "win": int, "draw": int, "lose": int, "match_num": int, "win_rate": float, "draw_rate": float, "lose_rate": float, "avg_score": float},
# "all_indicators_impact": [{"indicator": string, "indicator_type": string, "average_indicator_value": float, "max_indicator_value": float, "impact_to_offensive": float, "impact_to_defensive": float, "impact_to_net": float}],
# "all_opponents_impact": [{"efficiency_type": string, "impact_to_offensive": float, "impact_to_defensive": float, "impact_to_net": float}]}
# league names: ['england', 'france', 'germany', 'italy', 'spain', 'euro']
def get_impact_factors(frontend_data):

    # input and output
    league_name = frontend_data.get('LeagueName')
    team_name = frontend_data.get('TeamName')
    team_id = frontend_data.get('TeamId')

    all_indicators_impact_info = {}

    # load files
    match_file_path = './frontend-data/' + league_name + '.json'
    all_matches = load_json_data_cn(match_file_path)

    efficiency_file_path = './frontend-data/average-efficiency.json'
    all_efficiency_by_league = load_json_data(efficiency_file_path)

    # flag
    flag = 0 if team_id == 0 else 1

    # indicators
    # indicators = ['goal_nums', 'concede_nums', 'shot_nums', 'shot_on_target_nums', 'shot_on_frame_nums', 'breakthrough_pass_nums',
    #               'offside_nums', 'tackle_nums', 'freekick_nums', 'foul_nums', 'corner_nums', 'long_pass_nums',
    #               'pass_success_rates', 'cross_success_rates', 'tackle_success_rates', 'possession_rates']
    indicators = ['breakthrough_pass_nums', 'offside_nums', 'tackle_nums', 'freekick_nums', 'foul_nums', 'corner_nums', 'long_pass_nums',
                  'pass_success_rates', 'cross_success_rates', 'tackle_success_rates', 'possession_rates']
    offensive_indicators = ['breakthrough_pass_nums', 'freekick_nums', 'corner_nums', 'long_pass_nums', 'pass_success_rates', 'cross_success_rates', 'possession_rates']
    defensive_indicators = ['offside_nums', 'tackle_nums', 'foul_nums', 'tackle_success_rates']

    # efficiency types
    efficiency_types = ['offensive_efficiency', 'defensive_efficiency', 'net_efficiency']

    all_efficiency_in_league = all_efficiency_by_league[league_name]

    average_indicator_values = [0] * len(indicators)
    max_indicator_values = [0] * len(indicators)

    # train prediction model
    all_features = []
    all_offensive_efficiency = []
    all_defensive_efficiency = []
    all_net_efficiency = []

    for match in all_matches:

        if flag == 1 and match['team_id'] != team_id:
            continue

        current_feature = []

        for indicator in indicators:
            current_feature.append(match[indicator])

        for i in range(len(indicators)):
            average_indicator_values[i] = average_indicator_values[i] + match[indicators[i]]

        _, opponent_team_id = get_opponent_team(all_matches, match['team_id'], match['match_id'])

        for efficiency in all_efficiency_in_league:

            if efficiency['team_id'] == opponent_team_id:

                for efficiency_type in efficiency_types:
                    current_feature.append(efficiency[efficiency_type])

                break

        all_features.append(current_feature.copy())

        all_offensive_efficiency.append(match['offensive_efficiency'])
        all_defensive_efficiency.append(match['defensive_efficiency'])
        all_net_efficiency.append(match['net_efficiency'])

    for match in all_matches:

        for i in range(len(indicators)):
            max_indicator_values[i] = max(max_indicator_values[i], match[indicators[i]])

    all_features = np.array(all_features)
    all_offensive_efficiency = np.array(all_offensive_efficiency)
    all_defensive_efficiency = np.array(all_defensive_efficiency)
    all_net_efficiency = np.array(all_net_efficiency)

    # offensive efficiency
    offensive_regr = RandomForestRegressor(max_depth=5, random_state=0)
    offensive_regr.fit(all_features, all_offensive_efficiency)

    offensive_accuracy = offensive_regr.score(all_features, all_offensive_efficiency)
    print(offensive_accuracy)

    # defensive efficiency
    defensive_regr = RandomForestRegressor(max_depth=5, random_state=0)
    defensive_regr.fit(all_features, all_defensive_efficiency)

    defensive_accuracy = defensive_regr.score(all_features, all_defensive_efficiency)
    print(defensive_accuracy)

    # net efficiency
    net_regr = RandomForestRegressor(max_depth=5, random_state=0)
    net_regr.fit(all_features, all_net_efficiency)

    net_accuracy = net_regr.score(all_features, all_net_efficiency)
    print(net_accuracy)

    # weights
    offensive_impact = offensive_regr.feature_importances_
    defensive_impact = defensive_regr.feature_importances_
    net_impact = net_regr.feature_importances_

    # output collection
    all_indicators_impact = []

    for i in range(len(average_indicator_values)):
        average_indicator_values[i] = average_indicator_values[i] / len(all_features)

    for i in range(len(indicators)):

        indicator_info = {}

        indicator_info['indicator'] = indicators[i]
        
        if indicators[i] in offensive_indicators:
            indicator_info['type'] = 'offensive'
        else:
            indicator_info['type'] = 'defensive'

        indicator_info['average_indicator_value'] = average_indicator_values[i]
        indicator_info['max_indicator_value'] = max_indicator_values[i]
        indicator_info['impact_to_offensive'] = offensive_impact[i]
        indicator_info['impact_to_defensive'] = defensive_impact[i]
        indicator_info['impact_to_net'] = net_impact[i]

        all_indicators_impact.append(indicator_info)

    print(len(all_indicators_impact))

    all_opponents_impact = []

    for i in range(len(efficiency_types)):

        efficiency_info = {}

        efficiency_info['efficiency_type'] = efficiency_types[i]
        efficiency_info['impact_to_offensive'] = offensive_impact[len(indicators) + i]
        efficiency_info['impact_to_defensive'] = defensive_impact[len(indicators) + i]
        efficiency_info['impact_to_net'] = net_impact[len(indicators) + i]

        all_opponents_impact.append(efficiency_info)

    print(len(all_opponents_impact))

    # team info collection
    team_info = {}

    average_offensive_efficiency, average_defensive_efficiency = get_average_efficiency_values(league_name, all_efficiency_by_league)

    for efficiency in all_efficiency_in_league:

        if efficiency['team_id'] == team_id:

            if efficiency['offensive_efficiency'] > average_offensive_efficiency and efficiency['defensive_efficiency'] < average_defensive_efficiency:
                team_info['team_type'] = 'offensive_and_defensive'
            elif efficiency['offensive_efficiency'] > average_offensive_efficiency and efficiency['defensive_efficiency'] >= average_defensive_efficiency:
                team_info['team_type'] = 'offensive'
            elif efficiency['offensive_efficiency'] <= average_offensive_efficiency and efficiency['defensive_efficiency'] < average_defensive_efficiency:
                team_info['team_type'] = 'defensive'
            else:
                team_info['team_type'] = 'no_offensive_and_no_defensive'

    team_info['win'] = 0
    team_info['draw'] = 0
    team_info['lose'] = 0

    for match in all_matches:

        if flag == 1 and match['team_id'] != team_id:
            continue

        if match['goal_nums'] > match['concede_nums']:
            team_info['win'] = team_info['win'] + 1
        elif match['goal_nums'] == match['concede_nums']:
            team_info['draw'] = team_info['draw'] + 1
        else:
            team_info['lose'] = team_info['lose'] + 1

    team_info['match_num'] = len(all_features)
    team_info['win_rate'] = team_info['win'] / team_info['match_num']
    team_info['draw_rate'] = team_info['draw'] / team_info['match_num']
    team_info['lose_rate'] = team_info['lose'] / team_info['match_num']
    team_info['avg_score'] = (team_info['win'] * 3 + team_info['draw'] * 1) / team_info['match_num']

    # output data
    all_indicators_impact_info['all_indicators_impact'] = all_indicators_impact.copy()
    all_indicators_impact_info['team_info'] = team_info.copy()
    all_indicators_impact_info['all_opponents_impact'] = all_opponents_impact.copy()

    all_indicators_impact_info = json.dumps(all_indicators_impact_info)

    return all_indicators_impact_info

if __name__ == '__main__':

    frontend_data = {'LeagueName': 'england', 'TeamName': 'Manchester City', 'TeamId': 1625}

    all_indicators_impact_info = get_impact_factors(frontend_data)

    print(all_indicators_impact_info)