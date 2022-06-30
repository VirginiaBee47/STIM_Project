import requests as rq
import os
import json

API_KEY = "RGAPI-89916bde-63e6-4900-a1e6-df36bc44345e"


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.API_KEY = API_KEY
        self.json_file_path = os.getcwd() + "\\games\\" + self.gameid + ".json"
        self.raw_json = self.get_raw_json()
        self.participants = self.raw_json['metadata']['participants']
        self.game_length = self.raw_json['info']['gameDuration']

    def get_raw_json(self):
        response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + self.game_id +
                          "?api_key=" + self.API_KEY)

        if response.status_code == 200:
            response_data = json.loads(json.dumps(response.json()))
            with open(self.json_file_path, 'w') as outfile:
                json.dump(response_data, outfile)
                outfile.close()
            return response_data
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))
            return "XXX"

    def load_json(self):
        with open(self.json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
        return json_data

    def del_file(self):
        os.remove(self.json_file_path)
