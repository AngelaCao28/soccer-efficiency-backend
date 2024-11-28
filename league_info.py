import numpy as np
import os
import json

import pandas as pd

from utilities import *

# merge league info
def generate_league_info():

    # all league names
    league_names = ['england', 'france', 'germany', 'italy', 'spain', 'euro']

    # output
    all_league_info = {}

    for league_name in league_names:

        # load files
        match_file_path = './frontend-data/' + league_name + '.json'
        all_matches = load_json_data_cn(match_file_path)

        # output for current league
        current_league_info = []

        division = [0.3, 0.2, 0.1, 0, -0.1, -0.2, -0.3]
        division_num = 9

        for i in range(division_num):

            current_division = {}

            current_division['division_id'] = i
            current_division['win'] = 0
            current_division['draw'] = 0
            current_division['lose'] = 0
            current_division['match_num'] = 0

            current_league_info.append(current_division)

        for match in all_matches:

            division_id = -1

            if match['net_efficiency'] >= division[0]:
                division_id = 0
            elif match['net_efficiency'] < division[0] and match['net_efficiency'] >= division[1]:
                division_id = 1
            elif match['net_efficiency'] < division[1] and match['net_efficiency'] >= division[2]:
                division_id = 2
            elif match['net_efficiency'] < division[2] and match['net_efficiency'] > division[3]:
                division_id = 3
            elif match['net_efficiency'] == division[3]:
                division_id = 4
            elif match['net_efficiency'] < division[3] and match['net_efficiency'] > division[4]:
                division_id = 5
            elif match['net_efficiency'] <= division[4] and match['net_efficiency'] > division[5]:
                division_id = 6
            elif match['net_efficiency'] <= division[5] and match['net_efficiency'] > division[6]:
                division_id = 7
            else:
                division_id = 8

            current_league_info[division_id]['match_num'] = current_league_info[division_id]['match_num'] + 1

            if match['goal_nums'] > match['concede_nums']:
                current_league_info[division_id]['win'] = current_league_info[division_id]['win'] + 1
            elif match['goal_nums'] == match['concede_nums']:
                current_league_info[division_id]['draw'] = current_league_info[division_id]['draw'] + 1
            else:
                current_league_info[division_id]['lose'] = current_league_info[division_id]['lose'] + 1

        for current_division in current_league_info:

            if current_division['match_num'] == 0:

                current_division['win_rate'] = 0
                current_division['draw_rate'] = 0
                current_division['lose_rate'] = 0

                current_division['avg_score'] = 0

            else:

                current_division['win_rate'] = current_division['win'] / current_division['match_num']
                current_division['draw_rate'] = current_division['draw'] / current_division['match_num']
                current_division['lose_rate'] = current_division['lose'] / current_division['match_num']

                current_division['avg_score'] = (current_division['win'] * 3 + current_division['draw'] * 1) / current_division['match_num']

        all_league_info[league_name] = current_league_info.copy()

    # write files
    print(len(all_league_info.keys()))

    all_league_info = json.dumps(all_league_info)
    result_file_path = './frontend-data/league-info.json'

    f = open(result_file_path, 'w')
    f.write(all_league_info)
    f.close()

# average efficiency values for each team
def average_efficiency_values():

    # all league names
    league_names = ['england', 'france', 'germany', 'italy', 'spain', 'euro']

    # output
    all_average_efficiency = {}

    for league_name in league_names:

        # load files
        match_file_path = './frontend-data/' + league_name + '.json'
        all_matches = load_json_data_cn(match_file_path)

        # output for current league
        current_league_average_efficiency = []
        team_list = []

        for match in all_matches:

            if match['team_name'] not in team_list:

                team_average_efficiency = {}

                team_average_efficiency['team_name'] = match['team_name']
                team_average_efficiency['team_id'] = match['team_id']
                team_average_efficiency['offensive_efficiency'] = 0
                team_average_efficiency['defensive_efficiency'] = 0
                team_average_efficiency['net_efficiency'] = 0
                team_average_efficiency['match_num'] = 0

                current_league_average_efficiency.append(team_average_efficiency.copy())
                team_list.append(match['team_name'])

            for team_average_efficiency in current_league_average_efficiency:

                if team_average_efficiency['team_name'] == match['team_name']:

                    team_average_efficiency['offensive_efficiency'] = team_average_efficiency['offensive_efficiency'] + match['offensive_efficiency']
                    team_average_efficiency['defensive_efficiency'] = team_average_efficiency['defensive_efficiency'] + match['defensive_efficiency']
                    team_average_efficiency['net_efficiency'] = team_average_efficiency['net_efficiency'] + match['net_efficiency']
                    team_average_efficiency['match_num'] = team_average_efficiency['match_num'] + 1

                    break

        for team_average_efficiency in current_league_average_efficiency:

            team_average_efficiency['offensive_efficiency'] = team_average_efficiency['offensive_efficiency'] / team_average_efficiency['match_num']
            team_average_efficiency['defensive_efficiency'] = team_average_efficiency['defensive_efficiency'] / team_average_efficiency['match_num']
            team_average_efficiency['net_efficiency'] = team_average_efficiency['net_efficiency'] / team_average_efficiency['match_num']

        all_average_efficiency[league_name] = current_league_average_efficiency.copy()

    # write files
    print(len(all_average_efficiency.keys()))

    all_average_efficiency = json.dumps(all_average_efficiency)
    result_file_path = './frontend-data/average-efficiency.json'

    f = open(result_file_path, 'w')
    f.write(all_average_efficiency)
    f.close()

if __name__ == '__main__':

    average_efficiency_values()