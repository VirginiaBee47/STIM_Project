import requests as rq

from API_KEY import API_KEY


def check_summoner_exists(summoner_name):
    response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + API_KEY)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
