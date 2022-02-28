import time
from typing import List

import requests
import pickle
from data_types import *

key = "RGAPI-51b1dd6b-78f1-435a-8f00-322006af9450"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": key
}

ROUTING = {'NA1': 'americas',
           'BR1': 'americas',
           'LA1': 'americas',
           'LA2': 'americas',
           'OC1': 'americas',
           'KR': 'asia',
           'JP1': 'asia',
           'EUN1': 'europe',
           'EUW1': 'europe',
           'TR1': 'europe',
           'RU': 'europe'}


def load_data_from_pkl(pkl_file_path: str = "summoners_bronze.pkl"):
    """
    Loads players data from given pkl file path.
    :param pkl_file_path: the path to the pkl file.
    :return: List of Lists (inner list of size 2)
    """
    with open(pkl_file_path, 'rb') as f:
        players_data = pickle.load(f)
    return players_data


def load_bronze_players_data() -> List[List[str]]:
    """
    loads data from summoners_bronze.pkl file.
    :return: the data from summoners_bronze.pkl
    """
    return load_data_from_pkl("summoners_bronze.pkl")


def load_grandmaster_players_data() -> List[List[str]]:
    """
    loads data from summoners_grandmaster.pkl file.
    :return: the data from summoners_grandmaster.pkl
    """
    return load_data_from_pkl("summoners_grandmaster.pkl")


def load_bronze_match_ids() -> List[str]:
    """
    loads data from matches_bronze.pkl file.
    :return: the data from matches_bronze.pkl as a list
    """
    return list(dict.fromkeys(load_data_from_pkl("matches_bronze.pkl")))


def load_grandmaster_match_ids() -> List[str]:
    """
    loads data from matches_grandmaster.pkl file.
    :return: the data from matches_grandmaster.pkl as a list
    """
    return list(dict.fromkeys(load_data_from_pkl("matches_grandmaster.pkl")))


def get_games_ids_of_player(player_name: str, region: str, num_of_matches: int = 20) -> List[str]:
    """
    returns a list of match id's of the given player_name.
    :param num_of_matches: num of matches of the given player to get
    :param region: the region of the given player
    :param player_name: the name of the given player
    :return: List of match id's
    """

    # This part gets info about the given player (the puuid is necessary to pull the matches)
    request_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}"
    player_details = requests.get(url=request_url, headers=headers).json()
    puuid = player_details.get("puuid", None)
    if puuid is None:
        return []
    request_url = f"https://{ROUTING[region.upper()]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num_of_matches}"
    matches = requests.get(url=request_url, headers=headers).json()
    return matches


def get_timeline_of_match(match_id: str):
    """
    Requests the timeline of the given match id.
    :param match_id: match id
    :return: the timeline of the given match id
    """
    request_url = f"https://{ROUTING[match_id.split('_')[0]]}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    response = requests.get(url=request_url, headers=headers)
    return response.json()


def create_bronze_match_ids_pkl(num_of_players: int = 2000, matches_per_player: int = 1):
    """
    Save match_id's of the saved bronze players.
    :param num_of_players: the number of players to get matches from
    :param matches_per_player: the number of matches to get for each player
    :return:
    """
    match_ids = []
    bronze_players = load_bronze_players_data()
    for i in range(num_of_players):
        print(i)
        match_ids += get_games_ids_of_player(bronze_players[i][0], bronze_players[i][1],
                                             num_of_matches=matches_per_player)
    with open("matches_bronze.pkl", 'wb') as f:
        pickle.dump(match_ids, f)


def create_grandmaster_match_ids_pkl(num_of_players: int = 15000, matches_per_player: int = 1):
    """
    Save grandmaster match id's.
    :param num_of_players: the number of player to save match id's from.
    :param matches_per_player: the number of matches to save for each player.
    :return:
    """
    match_ids = []
    grandmaster_players = load_grandmaster_players_data()
    for i in range(num_of_players):
        try:
            print(i)
            match_ids += get_games_ids_of_player(grandmaster_players[i][0], grandmaster_players[i][1],
                                                 num_of_matches=matches_per_player)
            if i % 100 == 0:
                with open("matches_grandmaster.pkl", 'wb') as f:
                    pickle.dump(match_ids, f)
        except:
            print("Error: sleeping..")
            time.sleep(10)
    with open("matches_grandmaster.pkl", 'wb') as f:
        pickle.dump(match_ids, f)


def create_bronze_timelines():
    """
    Save bronze timelines from the saved match id's.
    :return:
    """
    matches = load_bronze_match_ids()
    timelines = []
    for i in range(len(matches)):
        print(i)
        timelines.append(get_timeline_of_match(matches[i]))
    with open("timelines_bronze.pkl", 'wb') as f:
        pickle.dump(timelines, f)


def create_grandmaster_timelines():
    """
    Save grandmaster timelines from the save match id's.
    :return:
    """
    matches = load_grandmaster_match_ids()
    timelines = []
    for i in range(2000, 5000):
        print(i)
        if i % 100 == 0:
            with open("timelines_grandmaster2.pkl", 'wb') as f:
                pickle.dump(timelines, f)
        try:
            timelines.append(get_timeline_of_match(matches[i]))
        except:
            print("Error: sleeping..")
            time.sleep(10)
    with open("timelines_grandmaster2.pkl", 'wb') as f:
        pickle.dump(timelines, f)


def extract_and_save_teams():
    with open('timelines_bronze.pkl', 'rb') as f:
        bronze_data = pickle.load(f)

    with open('timelines_grandmaster.pkl', 'rb') as f:
        grand_data0 = pickle.load(f)

    with open('timelines_grandmaster1.pkl', 'rb') as f:
        grand_data1 = pickle.load(f)

    with open('timelines_grandmaster2.pkl', 'rb') as f:
        grand_data2 = pickle.load(f)

    tests = []
    g_teams = []

    for i, match in enumerate(bronze_data):
        temp_bronze_match = Match(match)
        if temp_bronze_match.valid_data:
            if temp_bronze_match.champions_a_valid:
                tests.append(Team(temp_bronze_match, 'A'))
            if temp_bronze_match.champions_b_valid:
                tests.append(Team(temp_bronze_match, 'B'))

    for match in grand_data0:
        temp_grand_match = Match(match)
        if temp_grand_match.valid_data:
            if temp_grand_match.champions_a_valid:
                g_teams.append(Team(temp_grand_match, 'A'))
            if temp_grand_match.champions_b_valid:
                g_teams.append(Team(temp_grand_match, 'B'))

    for match in grand_data1:
        temp_grand_match = Match(match)
        if temp_grand_match.valid_data:
            if temp_grand_match.champions_a_valid:
                g_teams.append(Team(temp_grand_match, 'A'))
            if temp_grand_match.champions_b_valid:
                g_teams.append(Team(temp_grand_match, 'B'))

    for match in grand_data2:
        temp_grand_match = Match(match)
        if temp_grand_match.valid_data:
            if temp_grand_match.champions_a_valid:
                g_teams.append(Team(temp_grand_match, 'A'))
            if temp_grand_match.champions_b_valid:
                g_teams.append(Team(temp_grand_match, 'B'))

    save_teams(tests, "test_bronze_teams.pkl")
    save_teams(g_teams, "grand_teams.pkl")


def save_teams(teams: list, file_name: str):
    """
    Saves the given Teams list in the given file_name.
    :param teams: the teams to save
    :param file_name: the file_name to save as
    :return:
    """
    with open(file_name, 'wb') as f:
        pickle.dump(teams, f)
