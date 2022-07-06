import csv
import json
import asyncio

from new_exceptions import *
from summoner import *
from data_processing import *
from API_KEY import API_KEY


def check_summoner_exists(summoner_name):
    response = rq.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                      "?api_key=" + API_KEY)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False


def make_game_csv(summoner_name, summoner_puuid=None, num_games=5, recent_game_ids=None):
    if summoner_puuid is None:
        summoner_puuid = get_summoner("bEANS47")[0]

    if recent_game_ids is None:
        recent_game_ids = get_recent_game_ids(summoner_puuid, num_games)

    for game_id in recent_game_ids:
        raw_game_data, raw_game_timeline_data = asyncio.run(get_raw_game_data(game_id))
        with open("data\\%s_%s.csv" % (summoner_name, game_id), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Minute", "Total Gold", "Total Exp", "Gold Diff"])

            gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[2]
            xp_timeline = get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[1]
            gold_diff_timeline = get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, summoner_puuid)

            for minute in range(len(gold_timeline)):
                writer.writerow([minute, gold_timeline[minute], xp_timeline[minute], gold_diff_timeline[minute]])


async def get_data(game_id, timeline=False):
    if timeline:
        timeline_string = "/timeline"
    else:
        timeline_string = ""

    response = rq.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id +
                      timeline_string + "?api_key=" + API_KEY)

    if response.status_code == 200:
        data = json.loads(json.dumps(response.json()))
    else:
        raise NullGameException

    return data, timeline


async def get_raw_game_data(game_id):
    raw_game_data, raw_game_timeline_data = None, None
    tasks = [get_data(game_id), get_data(game_id, True)]
    for data, is_timeline in await asyncio.gather(*tasks):
        try:
            if is_timeline:
                raw_game_timeline_data = data
            else:
                raw_game_data = data
        except Exception as error:
            print("Exception found:", error)

    if raw_game_data is not None and raw_game_timeline_data is not None:
        return raw_game_data, raw_game_timeline_data
    else:
        raise NullGameException
