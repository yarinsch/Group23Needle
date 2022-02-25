class User:
    def __init__(self, game_data):
        self.match_id = game_data['metadata']['matchId']
        self.user_team =  self._get_user_team_data(game_data)

    def _get_user_team_data(self, game_data):
        return None
