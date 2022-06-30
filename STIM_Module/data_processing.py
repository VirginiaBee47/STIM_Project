from datetime import datetime as dt


def get_game_stats(raw_game_data, raw_game_timeline_data):
    game_mode = raw_game_data['info']['gameMode']
    game_map = raw_game_data['info']['mapId']
    game_date_time = dt.fromtimestamp(round(float(raw_game_data['info']['gameStartTimestamp']) / 1000, 0))
    ended_in_surrender = bool(raw_game_data['info']['participants'][0]['gameEndedInSurrender']) and bool(
        raw_game_data['info']['participants'][5]['gameEndedInSurrender'])

    return game_mode, game_map, game_date_time, ended_in_surrender


def get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    gold_earned = raw_game_data['info']['participants'][summoner_index]['goldEarned']
    gold_spent = raw_game_data['info']['participants'][summoner_index]['goldSpent']

    timeline_index = str(summoner_index + 1)

    gold_timeline = []
    for i in range(0, len(list(raw_game_timeline_data['info']['frames']))):
        gold_timeline.append(raw_game_timeline_data['info']['frames'][i]['participantFrames'][timeline_index]['totalGold'])

    print(gold_timeline)

    return gold_earned, gold_spent, gold_timeline
