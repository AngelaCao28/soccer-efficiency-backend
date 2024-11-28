import json
import numpy as np

import pandas as pd
import csv

# load json data
def load_json_data(file_path):

    f = open(file_path, 'r')
    all_data = json.load(f)
    f.close()

    return all_data

# load json data with utf-8
def load_json_data_cn(file_path):

    f = open(file_path, 'r', encoding='utf-8')
    all_data = json.load(f)
    f.close()

    return all_data

# get opponent team for each match
def get_opponent_team(all_matches, team_id, match_id):

    for match in all_matches:
        if match['match_id'] == match_id and match['team_id'] != team_id:
            return match['team_name'], match['team_id']
        
# get average efficiency values for the league
def get_average_efficiency_values(league_name, all_efficiency_by_league):

    all_efficiency_in_league = all_efficiency_by_league[league_name]

    average_offensive_efficiency = 0
    average_defensive_efficiency = 0

    team_num = 0

    for team_average_efficiency in all_efficiency_in_league:

        average_offensive_efficiency = average_offensive_efficiency + team_average_efficiency['offensive_efficiency']
        average_defensive_efficiency = average_defensive_efficiency + team_average_efficiency['defensive_efficiency']

        team_num = team_num + 1

    average_offensive_efficiency = average_offensive_efficiency / team_num
    average_defensive_efficiency = average_defensive_efficiency / team_num

    return average_offensive_efficiency, average_defensive_efficiency