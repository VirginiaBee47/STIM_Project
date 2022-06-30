from summoner import Summoner
from game import Game


def main():
    test_summoner = Summoner("bEANS47")
    test_game = Game(*test_summoner.get_recent_game_ids(1))
    print(test_game.raw_game_data)


if __name__ == '__main__':
    main()
