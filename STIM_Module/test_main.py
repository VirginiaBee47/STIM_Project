from summoner import Summoner
from game import Game
from api_funcs import *
from data_processing import *


def main():
    puuid = Summoner("bEANS47").puuid
    game_id = get_recent_game_ids(puuid, 1)[0]
    raw_game_data, raw_game_timeline_data = get_raw_game_data(game_id)
    get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, puuid)


if __name__ == '__main__':
    main()
