import numpy as np
import os
import json

import pandas as pd

from utilities import *

# get team details
# input: {"league_name": string, "team_name": string, "team_id": int}
# output: {"team_details": [{"round": int, "match_result": string, "offensive_efficiency": float, "defensive_efficiency": float, "net_efficiency": float, "match_type": string, "match_info": string}]}
# league names: ['england', 'france', 'germany', 'italy', 'spain', 'euro']
def get_team_details(frontend_data):

    # input and output
    league_name = frontend_data.get('LeagueName')
    team_name = frontend_data.get('TeamName')
    team_id = frontend_data.get('TeamId')

    all_team_details = {}

    # load files
    match_file_path = './frontend-data/' + league_name + '.json'
    all_matches = load_json_data_cn(match_file_path)

    efficiency_file_path = './frontend-data/average-efficiency.json'
    all_efficiency_by_league = load_json_data(efficiency_file_path)

    # type of the match
    average_offensive_efficiency, average_defensive_efficiency = get_average_efficiency_values(league_name, all_efficiency_by_league)

    # find all matches for the team
    team_details = []

    for match in all_matches:

        if match['team_id'] == team_id:

            current_match_details = {}

            current_match_details['round'] = match['round']

            if match['goal_nums'] > match['concede_nums']:
                current_match_details['match_result'] = 'win'
            elif match['goal_nums'] == match['concede_nums']:
                current_match_details['match_result'] = 'draw'
            else:
                current_match_details['match_result'] = 'lose'

            current_match_details['offensive_efficiency'] = match['offensive_efficiency']
            current_match_details['defensive_efficiency'] = match['defensive_efficiency']
            current_match_details['net_efficiency'] = match['net_efficiency']

            if match['offensive_efficiency'] > average_offensive_efficiency and match['defensive_efficiency'] < average_defensive_efficiency:
                current_match_details['match_type'] = 'offensive_and_defensive'
            elif match['offensive_efficiency'] > average_offensive_efficiency and match['defensive_efficiency'] >= average_defensive_efficiency:
                current_match_details['match_type'] = 'offensive'
            elif match['offensive_efficiency'] <= average_offensive_efficiency and match['defensive_efficiency'] < average_defensive_efficiency:
                current_match_details['match_type'] = 'defensive'
            else:
                current_match_details['match_type'] = 'no_offensive_and_no_defensive'

            opponent_team_name, _ = get_opponent_team(all_matches, match['team_id'], match['match_id'])

            current_match_details['match_info'] = match['team_name'] + ' ' + str(match['goal_nums']) + ':' + str(match['concede_nums']) + ' ' + opponent_team_name

            team_details.append(current_match_details)

    # sort by round
    team_details = sorted(team_details, key=lambda e:e['round'])

    team_details = json.dumps(team_details)

    return team_details

if __name__ == '__main__':

    frontend_data = {'LeagueName': 'england', 'TeamName': 'Manchester City', 'TeamId': 1625}

    team_details = get_team_details(frontend_data)

    print(len(team_details))