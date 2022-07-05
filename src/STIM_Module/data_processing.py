from datetime import datetime as dt

from summoner import get_opponent_puuid


def get_game_stats(raw_game_data):
    game_mode = raw_game_data['info']['gameMode']
    game_map = raw_game_data['info']['mapId']
    game_date_time = dt.fromtimestamp(round(float(raw_game_data['info']['gameStartTimestamp']) / 1000, 0))
    ended_in_surrender = bool(raw_game_data['info']['participants'][0]['gameEndedInSurrender']) and bool(
        raw_game_data['info']['participants'][5]['gameEndedInSurrender'])

    return game_mode, game_map, game_date_time, ended_in_surrender


def get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, puuid):
    if puuid is None:
        return None, None, None
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    gold_earned = raw_game_data['info']['participants'][summoner_index]['goldEarned']
    gold_spent = raw_game_data['info']['participants'][summoner_index]['goldSpent']

    timeline_index = str(summoner_index + 1)

    gold_timeline = []
    for i in range(0, len(list(raw_game_timeline_data['info']['frames']))):
        gold_timeline.append(
            raw_game_timeline_data['info']['frames'][i]['participantFrames'][timeline_index]['totalGold'])

    return gold_earned, gold_spent, gold_timeline


def get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    timeline_index = str(summoner_index + 1)

    xp_timeline = []
    for i in range(0, len(list(raw_game_timeline_data['info']['frames']))):
        xp_timeline.append(raw_game_timeline_data['info']['frames'][i]['participantFrames'][timeline_index]['xp'])

    return xp_timeline[-1], xp_timeline


def get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, puuid, opponent_puuid=None):
    user_gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, puuid)[2]
    if opponent_puuid is None:
        if get_opponent_puuid(raw_game_data, puuid) is not None:
            opponent_gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data,
                                                             get_opponent_puuid(raw_game_data, puuid))[2]
        else:
            return [-1 for i in range(len(user_gold_timeline))]
    else:
        opponent_gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, opponent_puuid)[2]

    return [user_gold_timeline[i] - opponent_gold_timeline[i] for i in range(len(user_gold_timeline))]
