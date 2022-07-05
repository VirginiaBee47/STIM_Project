from summoner import *
from game import Game
from api_funcs import *
from data_processing import *


def main():
    puuid = get_summoner("bEANS47")[0]
    game_id = get_recent_game_ids(puuid, 1)[0]
    raw_game_data, raw_game_timeline_data = get_raw_game_data(game_id)
    print(*get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, puuid), sep="\n")
    opponent_puuid = get_opponent_puuid(raw_game_data, puuid)
    print(*get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, opponent_puuid), sep="\n")
    print(get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, puuid))


if __name__ == '__main__':
    main()
