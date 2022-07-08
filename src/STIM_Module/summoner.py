import json

import requests as rq

from API_KEY import API_KEY


def get_recent_game_ids(puuid, num_games):
    response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) +
                      "/ids?start=0&count=" + str(num_games) + "&api_key=" + API_KEY)

    if response.status_code == 200:
        return json.loads(json.dumps(response.json()))
    else:
        print("ERROR FOUND --- CODE: " + str(response.status_code))
        return []


def get_opponent_puuid(raw_game_data, user_puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(user_puuid)
    summoner_position = raw_game_data['info']['participants'][summoner_index]['teamPosition']

    if summoner_position == "":
        return None
    else:
        (possible_opponent_indices := [i for i in range(0, 9)]).remove(summoner_index)
        for i in possible_opponent_indices:
            if raw_game_data['info']['participants'][i]['teamPosition'] == summoner_position:
                return raw_game_data['metadata']['participants'][i]
        return None


def get_summoner(summoner_name):
    response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                      "?api_key=" + API_KEY)

    if response.status_code == 200:
        response_data = json.loads(json.dumps(response.json()))
        return response_data['puuid'], int(response_data['summonerLevel'])
    else:
        print("ERROR FOUND --- CODE: " + str(response.status_code))

