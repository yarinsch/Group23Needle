from typing import List

import requests
import pickle


key = "RGAPI-67801da8-4379-447d-ad01-1ef8f0c4916e"

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
    return load_data_from_pkl("summoners_bronze.pkl")


def load_grandmaster_players_data() -> List[List[str]]:
    return load_data_from_pkl("summoners_grandmaster.pkl")


def load_bronze_match_ids() -> List[str]:
    return list(dict.fromkeys(load_data_from_pkl("matches_bronze.pkl")))

def load_grandmaster_match_ids() -> List[str]:
    return list(dict.fromkeys(load_data_from_pkl("matches_grandmaster.pkl")))


def get_games_ids_of_player(player_name: str, region: str, num_of_matches: int = 20) -> List[str]:
    """
    returns a list of match id's of the given player_name.
    :param num_of_matches:
    :param region: ...
    :param player_name: ...
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
    request_url = f"https://{ROUTING[match_id.split('_')[0]]}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    response = requests.get(url=request_url, headers=headers)
    return response.json()


def create_bronze_match_ids_pkl(matches_to_save: int = 100, matches_per_player: int = 20):
    match_ids = []
    bronze_players = load_bronze_players_data()
    for i in range(matches_to_save):
        print(i)
        match_ids += get_games_ids_of_player(bronze_players[i][0], bronze_players[i][1],
                                             num_of_matches=matches_per_player)
    with open("matches_bronze.pkl", 'wb') as f:
        pickle.dump(match_ids, f)


def create_grandmaster_match_ids_pkl(matches_to_save: int = 100, matches_per_player: int = 20):
    match_ids = []
    grandmaster_players = load_grandmaster_players_data()
    for i in range(matches_to_save):
        print(i)
        match_ids += get_games_ids_of_player(grandmaster_players[i][0], grandmaster_players[i][1],
                                             num_of_matches=matches_per_player)
    with open("matches_grandmaster.pkl", 'wb') as f:
        pickle.dump(match_ids, f)


def create_bronze_timelines():
    matches = load_bronze_match_ids()
    timelines = []
    for i in range(len(matches)):
        print(i)
        # if i % 100 == 0:
        #     with open("timelines_bronze.pkl", 'wb') as f:
        #         pickle.dump(timelines, f)
        timelines.append(get_timeline_of_match(matches[i]))
    with open("timelines_bronze.pkl", 'wb') as f:
        pickle.dump(timelines, f)


def create_grandmaster_timelines():
    matches = load_grandmaster_match_ids()
    timelines = []
    for i in range(1000):
        print(i)
        # if i % 100 == 0:
        #     with open("timelines_grandmaster.pkl", 'wb') as f:
        #         pickle.dump(timelines, f)
        timelines.append(get_timeline_of_match(matches[i]))
    with open("timelines_grandmaster.pkl", 'wb') as f:
        pickle.dump(timelines, f)


if __name__ == '__main__':
    # create_bronze_match_ids_pkl()
    # create_grandmaster_match_ids_pkl()
    # create_bronze_timelines()
    create_grandmaster_timelines()


