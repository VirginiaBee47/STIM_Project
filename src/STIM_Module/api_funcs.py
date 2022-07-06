import csv
import json
import os

import requests as rq

from game import get_raw_game_data
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
    # TODO: Add directory existance checking, and add directory if it doesn't exists
    if not os.path.exists("./data"):
        #print("PATH DOES NOT EXIST")
        os.makedirs("./data")


    if summoner_puuid is None:
        summoner_puuid = get_summoner("bEANS47")[0]

    if recent_game_ids is None:
        recent_game_ids = get_recent_game_ids(summoner_puuid, num_games)

    for game_id in recent_game_ids:
        raw_game_data, raw_game_timeline_data = get_raw_game_data(game_id)
        with open("data/%s_%s.csv" % (summoner_name, game_id), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Minute", "Total Gold", "Total Exp", "Gold Diff"])

            gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[2]
            xp_timeline = get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[1]
            gold_diff_timeline = get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, summoner_puuid)

            for minute in range(len(gold_timeline)):
                writer.writerow([minute, gold_timeline[minute], xp_timeline[minute], gold_diff_timeline[minute]])
