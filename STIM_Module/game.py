import json

import requests as rq

from os import getcwd
from API_KEY import API_KEY


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.API_KEY = API_KEY
        self.raw_game_data = self.get_raw_game_data()
        self.participants = self.raw_game_data['metadata']['participants']
        self.game_length = self.raw_game_data['info']['gameDuration']

    def get_raw_game_data(self):
        response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + self.game_id +
                          "?api_key=" + self.API_KEY)

        if response.status_code == 200:
            response_data = json.loads(json.dumps(response.json()))
            return response_data
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))
            return "XXX"

    def load_json(self):
        with open(self.json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
        return json_data
