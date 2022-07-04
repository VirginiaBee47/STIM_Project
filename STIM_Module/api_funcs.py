import json

import requests as rq

from game import get_raw_game_data
from summoner import get_recent_game_ids
from API_KEY import API_KEY


def check_summoner_exists(summoner_name):
    response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                      "?api_key=" + API_KEY)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False


def make_game_csv(summoner_name, num_games=1):
    response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                      "?api_key=" + API_KEY)

    summoner_puuid = json.loads(json.dumps(response.json()))['puuid']
    recent_game_ids = get_recent_game_ids(summoner_puuid, num_games)

    for game_id in recent_game_ids:
        raw_game_data, raw_game_timeline_data = get_raw_game_data(game_id)
        