from summoner import *
from user import *
from api_funcs import *
from data_processing import *


def main():
    puuid = get_summoner("bEANS47")[0]
    recent_game_id = get_recent_game_ids(puuid)[0]
    make_game_csv("bEANS47", puuid)


if __name__ == '__main__':
    main()
