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

DEPRECATED_TYPES = {'LEVEL_UP',
                    'DRAGON_SOUL_GIVEN',
                    'CHAMPION_TRANSFORM',
                    'PAUSE_END',
                    'SKILL_LEVEL_UP',
                    'ITEM_UNDO',
                    'CHAMPION_SPECIAL_KILL'}


class Match:
    def __init__(self, game_data):
        self.winning_team = None
        self.processed_game_data = {"A":[],"B":[]}
        self.valid_data = True
        if 'info' not in game_data:
            self.valid_data = False
            return
        self.game_data = game_data['info']['frames']
        self.match_id = game_data['metadata']['matchId']
        self.champions = [None] * 10
        self.num_of_champions = 0
        self.__get_team_champions()
        if self.num_of_champions < 10:
            self.valid_data = False
            return
        self.__pre_process_data()
        if self.winning_team is None:
            self.valid_data = False

    def get_event_types(self):
        """
        Return all
        :return:
        """
        types = set()
        for minute in self.game_data:
            for event in minute['events']:
                if 'type' in event:
                    types.add(event['type'])
        return types

    def __pre_process_data(self):
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
        for minute in self.game_data:
            for event in minute['events']:
                if 'type' in event and event['type'] == 'CHAMPION_KILL':
                    if 'victimDamageDealt' in event:
                        if not self.champions[event['victimId']-1]:
                            self.num_of_champions += 1
                            self.champions[event['victimId']-1] = event['victimDamageDealt'][0]['name']
                    if 'victimDamageReceived' in event:
                        for enemy_champion in event['victimDamageReceived']:
                            champion_id = enemy_champion['participantId'] - 1
                            if champion_id == -1:
                                continue
                            if not self.champions[champion_id]:
                                self.champions[champion_id] = enemy_champion['name']
                                self.num_of_champions += 1
                    if self.num_of_champions == 10:
                        return


class Team:
    """
    This class takes the users data and transforms it in a way that we will take into account only one side
    of each game
    """

    def __init__(self, match: Match, team_a_or_b: str = 'A'):
        # if len(args) == 4 and isinstance(args[0], list) and isinstance(args[1], set) and isinstance(args[1],
        #                                                                                             set) and is:
        #     self.items = args[0]
        #     self.champions = args[1]
        #     self.rivals = args[2]
        # elif len(args) == 2 and isinstance(args[0], Match) and isinstance(args[1], str) and \
        #         (args[1] == 'A' or args[1] == 'B'):
        #     self.items = args[0].processed_game_data[args[1]]
        #     self.champions = set(args[0].champions[:5])
        #     self.rivals = set(args[0].champions[5:])
        #     self.winners = True if args[0].winning_team == args[1] else False
        # else:
        #     print("Error: can't intialize Team object! Check given arguments.")
        #     self.items = []
        #     self.champions = set()
        #     self.rivals = set()
        self.items = match.processed_game_data[team_a_or_b]
        self.champions = set(match.champions[:5])
        self.rivals = set(match.champions[5:])
        self.winners = True if match.winning_team == team_a_or_b else False
