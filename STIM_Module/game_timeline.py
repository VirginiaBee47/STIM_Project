import requests as rq

from json import loads, dumps, load
from API_KEY import API_KEY


class GameTimeline:
    def __init__(self, game_id):
        self.game_id = game_id
        self.API_KEY = API_KEY
        self.rawJSON = self.get_raw_game_timeline_data()

    def get_raw_game_timeline_data(self):
        response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + self.gameid +
                          "/timeline?api_key=" + self.API_KEY)

        if response.status_code == 200:
            response_data = loads(dumps(response.json()))
            return response_data
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))
            return "XXX"
