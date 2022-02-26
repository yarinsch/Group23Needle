ALL_TYPES = {'ELITE_MONSTER_KILL': ["killerId", "monsterType", "monsterSubType"],
             'ITEM_PURCHASED': ["participantId", "itemId"],
             'CHAMPION_KILL': ["killerId", "victimId"],
             'ITEM_DESTROYED': ["participantId", "itemId"],
             'WARD_KILL': ["killerId", "wardType"],
             'TURRET_PLATE_DESTROYED': ["killerId", "laneType"],
             'BUILDING_KILL': ["killerId", "buildingType", "laneType", "towerType"],
             'WARD_PLACED1': ["creatorId", "wardType"],
             'ITEM_SOLD': ["participantId", "itemId"]}

DEPRECATED_TYPES = {'LEVEL_UP',
                    'DRAGON_SOUL_GIVEN',
                    'CHAMPION_TRANSFORM',
                    'PAUSE_END',
                    'SKILL_LEVEL_UP',
                    'ITEM_UNDO',
                    'GAME_END',
                    'CHAMPION_SPECIAL_KILL'}


class User:
    def __init__(self, game_data):
        self.processed_game_data = []
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
                    participantId = event[ALL_TYPES[type][0]]
                    if participantId != 0:
                        item = self.champions[participantId - 1]
                        if type == "CHAMPION_KILL":
                            item += "_" + self.champions[event[ALL_TYPES[type][1]] - 1]
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
            self.processed_game_data.append({'team_a': team_a, 'team_b': team_b})

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
