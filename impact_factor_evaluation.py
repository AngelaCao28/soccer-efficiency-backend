import numpy as np
import os
import json

import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from utilities import *

# get impact factors for each indicator (weights)
# input: {"league_name": string, "team_name": string, "team_id": int}
def get_impact_factors(frontend_data, all_efficiency_by_league):

    # input and output
    league_name = frontend_data.get('LeagueName')
    team_name = frontend_data.get('TeamName')
    team_id = frontend_data.get('TeamId')

    # load files
    match_file_path = './frontend-data/' + league_name + '.json'
    all_matches = load_json_data_cn(match_file_path)

    # flag
    flag = 0 if team_id == 0 else 1

    # indicators
    # indicators = ['goal_nums', 'concede_nums', 'shot_nums', 'shot_on_target_nums', 'shot_on_frame_nums', 'breakthrough_pass_nums',
    #               'offside_nums', 'tackle_nums', 'freekick_nums', 'foul_nums', 'corner_nums', 'long_pass_nums',
    #               'pass_success_rates', 'cross_success_rates', 'tackle_success_rates', 'possession_rates']
    indicators = ['breakthrough_pass_nums', 'offside_nums', 'tackle_nums', 'freekick_nums', 'foul_nums', 'corner_nums', 'long_pass_nums',
                  'pass_success_rates', 'cross_success_rates', 'tackle_success_rates', 'possession_rates']

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
    # print(offensive_accuracy)

    # defensive efficiency
    defensive_regr = RandomForestRegressor(max_depth=5, random_state=0)
    defensive_regr.fit(all_features, all_defensive_efficiency)

    defensive_accuracy = defensive_regr.score(all_features, all_defensive_efficiency)
    # print(defensive_accuracy)

    # net efficiency
    net_regr = RandomForestRegressor(max_depth=5, random_state=0)
    net_regr.fit(all_features, all_net_efficiency)

    net_accuracy = net_regr.score(all_features, all_net_efficiency)
    # print(net_accuracy)

    return offensive_accuracy, defensive_accuracy, net_accuracy

# get evaluation results of impact factors
def impact_factors_evaluation():

    # load files
    efficiency_file_path = './frontend-data/average-efficiency-cn.json'
    all_efficiency_by_league = load_json_data_cn(efficiency_file_path)

    # output
    impact_factors_results = []

    league_name_dict = {'england': '英超', 'france': '法甲', 'germany': '德甲', 'italy': '意甲', 'spain': '西甲', 'euro': '欧洲杯'}

    for league_name in all_efficiency_by_league.keys():

        for team_info in all_efficiency_by_league[league_name]:

            frontend_data = {'LeagueName': league_name, 'TeamName': team_info['team_name'], 'TeamId': team_info['team_id']}

            offensive_accuracy, defensive_accuracy, net_accuracy = get_impact_factors(frontend_data, all_efficiency_by_league)

            impact_factors_result = {}

            impact_factors_result['联赛'] = league_name_dict[league_name]
            impact_factors_result['球队'] = team_info['team_name_cn']
            impact_factors_result['球队（英文）'] = team_info['team_name']
            impact_factors_result['进攻效率决定系数'] = offensive_accuracy
            impact_factors_result['防守效率决定系数'] = defensive_accuracy
            impact_factors_result['净效率决定系数'] = net_accuracy

            impact_factors_results.append(impact_factors_result)

    # write files 
    print(len(impact_factors_results))

    df = pd.DataFrame(impact_factors_results)
    impact_factor_file_path_excel = 'impact-factor.xlsx'

    df.to_excel(impact_factor_file_path_excel, index=False)

if __name__ == '__main__':

    impact_factors_evaluation()