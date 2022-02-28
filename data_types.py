# ALL_TYPES holds the event types we take into account in our data processing
ALL_TYPES = {'ELITE_MONSTER_KILL': ["killerId","type","monsterType", "monsterSubType"],
             'ITEM_PURCHASED': ["participantId","type", "itemId"],
             'CHAMPION_KILL': ["killerId", "victimId"],
             'ITEM_DESTROYED': ["participantId","type", "itemId"],
             'WARD_KILL': ["killerId","type", "wardType"],
             'TURRET_PLATE_DESTROYED': ["killerId","type", "laneType"],
             'BUILDING_KILL': ["killerId", "buildingType","type", "laneType", "towerType"],
             'WARD_PLACED1': ["creatorId","type", "wardType"],
             'ITEM_SOLD': ["participantId","type", "itemId"],
             'GAME_END': []}

# DEPRECATED_TYPES are the event types we ignore
DEPRECATED_TYPES = {'LEVEL_UP',
                    'DRAGON_SOUL_GIVEN',
                    'CHAMPION_TRANSFORM',
                    'PAUSE_END',
                    'SKILL_LEVEL_UP',
                    'ITEM_UNDO',
                    'CHAMPION_SPECIAL_KILL'}


class Match:
    """
    A match is an object that parses and holds events occurrences in a given timeline.
    """
    def __init__(self, game_data):
        """
        Match constructor.
        :param game_data: a game timeline (not necessarily valid data)
        """
        self.winning_team = None  # which team won: 'A' or 'B'
        self.processed_game_data = {"A": [], "B": []}  # The events count relative to team 'A' and 'B'
        self.valid_data = True  # indication whether the data is valid for process or not
        if 'info' not in game_data:  # we get our data from game_data['info'], if it's not ther the data is invalid
            self.valid_data = False
            return
        self.game_data = game_data['info']['frames']
        self.match_id = game_data['metadata']['matchId']
        self.champions = {'A': set(), 'B': set()}  # the champions of team 'A' and 'B'
        self.champions_a_valid = False  # if there are less than 5 champions in 'A', 'A' data is invalid
        self.champions_b_valid = False  # if there are less than 5 champions in 'A', 'A' data is invalid
        self.__get_team_champions()
        self.__pre_process_data()
        if self.winning_team is None:  # if there is no winning team we cannot use the data
            self.valid_data = False

    def get_event_types(self):
        """
        Extracts all event types exist in the given timeline.
        :return:
        """
        types = set()
        for minute in self.game_data:
            for event in minute['events']:
                if 'type' in event:
                    types.add(event['type'])
        return types

    def __pre_process_data(self):
        """
        For each team ('A' and 'B') and for each minute in the given timeline, extracts the number of appearances of
        each relevant event (relevant event means that it appears in the ALL_TYPE dictionary).
        :return:
        """
        for minute in self.game_data:
            team_a = {}
            team_b = {}
            for event in minute['events']:
                type = event['type']
                if type in ALL_TYPES:
                    if type == "GAME_END":
                        if event['winningTeam'] == 100:
                            self.winning_team = 'A'
                        else:
                            self.winning_team = 'B'
                    else:
                        participantId = event[ALL_TYPES[type][0]]
                        if participantId != 0:
                            # item = self.champions[participantId - 1]
                            item = ""
                            if type == "CHAMPION_KILL":
                                # item += "_" + self.champions[event[ALL_TYPES[type][1]] - 1]
                                item = "champ_kill"
                            else:
                                for attribute in ALL_TYPES[type][1:]:
                                    if attribute in event:
                                        item += "_"
                                        item += str(event[attribute])
                            if participantId <= 5:
                                if item in team_a:
                                    team_a[item] += 1
                                else:
                                    team_a[item] = 1
                            else:
                                if item in team_b:
                                    team_b[item] += 1
                                else:
                                    team_b[item] = 1
            self.processed_game_data["A"].append(team_a)
            self.processed_game_data["B"].append(team_b)

    def __get_team_champions(self):
        """
        Extracts the champions for each team ('A' and 'B')
        :return:
        """
        for minute in self.game_data:
            for event in minute['events']:
                if ('type' in event) and (event['type'] == 'CHAMPION_KILL'):
                    if 'victimDamageDealt' in event:
                        if 0 < event['victimId'] <= 5:
                            self.champions['A'].add(event['victimDamageDealt'][0]['name'])
                        elif event['victimId'] > 5:
                            self.champions['B'].add(event['victimDamageDealt'][0]['name'])
                    if 'victimDamageReceived' in event:
                        for enemy_champion in event['victimDamageReceived']:
                            champion_id = enemy_champion['participantId']
                            if 0 < champion_id <= 5:
                                self.champions['A'].add(enemy_champion['name'])
                            elif champion_id > 5:
                                self.champions['B'].add(enemy_champion['name'])
                if len(self.champions['A']) == 5 and len(self.champions['B']) == 5:
                    self.champions_a_valid = True
                    self.champions_b_valid = True
                    return
        if len(self.champions['A']) == 5:
            self.champions_a_valid = True
        if len(self.champions['B']) == 5:
            self.champions_b_valid = True


class Team:
    """
    This class takes Match object and transforms it in a way that we will take into account only one side
    of each game.
    """
    KNOWN_TEAMS = {'A', 'B'}

    def __init__(self, match: Match, team_a_or_b: str = 'A'):
        """
        Team constructor
        :param match: the match to construct a team from
        :param team_a_or_b: the team to construct from the given match
        """
        self.items = match.processed_game_data[team_a_or_b]
        self.champions = match.champions[team_a_or_b]
        self.rivals = match.champions[list(Team.KNOWN_TEAMS.difference(team_a_or_b))[0]]
        self.winners = (match.winning_team == team_a_or_b)
        self.valid_data = (len(self.champions) == 5)

