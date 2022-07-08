import json

import requests as rq

from API_KEY import API_KEY


def get_raw_game_data(game_id):
    response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id +
                      "?api_key=" + API_KEY)

    if response.status_code == 200:
        raw_game_data = json.loads(json.dumps(response.json()))
    else:
        raw_game_data = None

    response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id +
                      "/timeline?api_key=" + API_KEY)

    if response.status_code == 200:
        raw_game_timeline_data = json.loads(json.dumps(response.json()))
    else:
        raw_game_timeline_data = None

    return raw_game_data, raw_game_timeline_data
