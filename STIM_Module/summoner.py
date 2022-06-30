import json

import requests as rq

from API_KEY import API_KEY


def get_recent_game_ids(puuid, num_games):
    response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid +
                      "/ids?start=0&count=" + str(num_games) + "&api_key=" + API_KEY)

    if response.status_code == 200:
        return json.loads(json.dumps(response.json()))
    else:
        print("ERROR FOUND --- CODE: " + str(response.status_code))
        return []


class Summoner:
    def __init__(self, summoner_name):
        self.API_KEY = API_KEY
        self.summoner_name = summoner_name
        self.puuid = self.get_summoner()[0]
        self.level = self.get_summoner()[1]

    def get_summoner(self):
        response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.summoner_name +
                          "?api_key=" + self.API_KEY)

        if response.status_code == 200:
            response_data = json.loads(json.dumps(response.json()))
            summoner_data = [response_data['puuid'], int(response_data['summonerLevel'])]
            return summoner_data
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))

    def get_recent_game_ids(self, num_games):
        response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + self.puuid +
                          "/ids?start=0&count=" + str(num_games) + "&api_key=" + self.API_KEY)

        if response.status_code == 200:
            recent_game_ids = json.loads(json.dumps(response.json()))
            return recent_game_ids
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))
            return []

    def get_specific_game_id(self, index_game):
        response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + self.puuid +
                          "/ids?start=" + str(index_game) + "&count=1&api_key=" + self.API_KEY)

        if response.status_code == 200:
            specific_game_id = json.loads(json.dumps(response.json()))
            return specific_game_id[0]
        else:
            print("ERROR FOUND --- CODE: " + str(response.status_code))
            return []
