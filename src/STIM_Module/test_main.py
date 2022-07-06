from summoner import *
from user import *
from api_funcs import *
from data_processing import *


def main():
    puuid = get_summoner("bEANS47")[0]
    recent_game_id = get_recent_game_ids(puuid)[0]
    asyncio.run(get_raw_game_data(recent_game_id))


if __name__ == '__main__':
    main()
