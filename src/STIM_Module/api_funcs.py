import csv, json, asyncio, re, os


import requests as rq
from datetime import datetime as dt
from STIM_Module.new_exceptions import *
from STIM_Module.API_KEY import API_KEY


def respect_rate_limit(url):
    response = rq.get(url)
    pattern = re.compile(r'(\d+):1,(\d+):120')
    for match in pattern.finditer(response.headers['X-App-Rate-Limit-Count']):
        one_sec_progress = int(match.group(1))
        two_min_progress = int(match.group(2))

    if one_sec_progress >= 18 or two_min_progress >= 95:
        raise RateLimitException(one_sec_progress, two_min_progress)
    else:
        return response


def check_summoner_exists(summoner_name):
    response = respect_rate_limit("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                                  "?api_key=" + API_KEY)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False


async def get_data(game_id, timeline=False):
    if timeline:
        timeline_string = "/timeline"
    else:
        timeline_string = ""

    response = respect_rate_limit("https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id +
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


def collect_data_for_rank(queue="RANKED_SOLO_5x5", tier="DIAMOND", division="I"):
    valid_queues = ["RANKED_SOLO_5x5", "RANKED_FLEX_SR"]
    valid_tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    valid_divisions = ["I", "II", "III", "IV"]

    if queue not in valid_queues:
        raise InvalidParamException("queue")
    elif tier not in valid_tiers:
        raise InvalidParamException("tier")
    elif division not in valid_divisions:
        raise InvalidParamException("division")

    response = respect_rate_limit(
        "https://na1.api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier + "/" + division + "?api_key=" +
        API_KEY)

    if response.status_code == 200:
        data = response.json()  # this is a list of summoners in the given queue, tier, and division
        summoner_name = data[5]['summonerName']
        return make_game_csv(summoner_name, num_games=3)
    else:
        print("Error code" + str(response.status_code))


def get_recent_game_ids(puuid, num_games=1):
    response = respect_rate_limit("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) +
                                  "/ids?start=0&count=" + str(num_games) + "&api_key=" + API_KEY)

    if response.status_code == 200:
        return json.loads(json.dumps(response.json()))
    else:
        print("ERROR FOUND --- CODE: " + str(response.status_code))
        return []


def get_opponent_puuid(raw_game_data, user_puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(user_puuid)
    summoner_position = raw_game_data['info']['participants'][summoner_index]['teamPosition']

    if summoner_position == "":
        return None
    else:
        (possible_opponent_indices := [i for i in range(0, 9)]).remove(summoner_index)
        for i in possible_opponent_indices:
            if raw_game_data['info']['participants'][i]['teamPosition'] == summoner_position:
                return raw_game_data['metadata']['participants'][i]
        return None


def get_summoner(summoner_name):
    response = respect_rate_limit("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +
                                  "?api_key=" + API_KEY)

    if response.status_code == 200:
        response_data = json.loads(json.dumps(response.json()))
        return response_data['puuid'], int(response_data['summonerLevel'])
    else:
        print("ERROR FOUND --- CODE: " + str(response.status_code))


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


def get_general_summoner_stats(raw_game_data, puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    champion = raw_game_data['info']['participants'][summoner_index]['championName']
    position = raw_game_data['info']['participants'][summoner_index]['teamPosition']
    victory = raw_game_data['info']['participants'][summoner_index]['win']

    return champion, position, victory


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


def make_game_csv(summoner_name, summoner_puuid=None, num_games=3, recent_game_ids=None):
    if not os.path.exists("./data"):
        # print("PATH DOES NOT EXIST")
        os.makedirs("./data")

    if summoner_puuid is None:
        summoner_puuid = get_summoner(summoner_name)[0]

    if recent_game_ids is None:
        recent_game_ids = get_recent_game_ids(summoner_puuid, num_games)

    filenames = []

    for game_id in recent_game_ids:
        raw_game_data, raw_game_timeline_data = asyncio.run(get_raw_game_data(game_id))
        with open("data/%s_%s.csv" % (summoner_name, game_id), 'w', newline='') as outfile:
            filenames.append("data/%s_%s.csv" % (summoner_name, game_id))
            writer = csv.writer(outfile)
            writer.writerow(["Minute", "Total Gold", "Total Exp", "Gold Diff"])

            gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[2]
            xp_timeline = get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[1]
            gold_diff_timeline = get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, summoner_puuid)

            for minute in range(len(gold_timeline)):
                writer.writerow([minute, gold_timeline[minute], xp_timeline[minute], gold_diff_timeline[minute]])

        with open("data/%s_%s.json" % (summoner_name, game_id), 'w') as outfile:
            # gold_timeline = get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[2]
            # xp_timeline = get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[1]
            # gold_diff_timeline = get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, summoner_puuid)

            champ, position, victory = get_general_summoner_stats(raw_game_data, summoner_puuid)
            game_mode, game_map, game_datetime, ended_in_surrender = get_game_stats(raw_game_data)

            data_dict = {'victory': victory, 'position': position, 'champion': champ, 'game_mode': game_mode,
                         'game_time': str(game_datetime), 'game_map': game_map, 'ended_in_surrender': ended_in_surrender}

            json.dump(data_dict, outfile)

    return filenames


def filter_games(summoner_name, filter_attr, filter_val):
    filter_attributes = ["victory", "champion_played", "position_played", "game_mode", "ended_in_surrender"]
    champions = ['MasterYi', 'Garen', 'Lucian']
    # TODO: add in every champion id as it is stored in the json (not always intuitive)
    positions = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT']
    game_modes = ['CLASSIC', 'ARAM']
    game_maps = []

    if filter_attr not in filter_attributes:
        raise InvalidParamException("filter_attr")
    elif filter_attr == 'champion_played' and filter_val not in champions:
        raise InvalidParamException("filter_val", "Champion not implemented yet")
    elif filter_attr == 'victory':
        try:
            filter_val = bool(filter_val)
        except Exception:
            raise InvalidParamException("filter_val", "Value could not be converted to boolean")
    elif filter_attr == 'position_played' and filter_val not in positions:
        raise InvalidParamException("filter_val", "Position does not exist")
    elif filter_attr == 'game_mode' and filter_val not in game_modes:
        raise InvalidParamException("filter_val", "Invalid game mode")
    elif filter_attr == 'ended_in_surrender':
        try:
            filter_val = bool(filter_val)
        except Exception:
            raise InvalidParamException("filter_val", "Value could not be converted to boolean")
    elif filter_attr == 'game_map' and filter_val not in game_maps:
        raise InvalidParamException("filter_val", "Invalid game map")

    filtered_files = []

    for game_file in os.listdir('./data'):
        if game_file[-5:] == ".json":
            if game_file[:len(summoner_name)] == summoner_name:
                with open("data/" + game_file, 'r') as file:
                    game_data = json.load(file)
                    if filter_attr == 'champion_played':
                        if game_data['champion'] == filter_val:
                            filtered_files.append(game_file)
                    elif filter_attr == 'victory':
                        if bool(game_data['victory']) == filter_val:
                            filtered_files.append(game_file)
                    elif filter_attr == 'position_played':
                        if game_data['position'] == filter_val:
                            filtered_files.append(game_file)
                    elif filter_attr == 'game_mode':
                        if game_data['game_mode'] == filter_val:
                            filtered_files.append(game_file)
                    elif filter_attr == 'ended_in_surrender':
                        if bool(game_data['ended_in_surrender']) == filter_val:
                            filtered_files.append(game_file)
                    elif filter_attr == 'game_map':
                        if game_data['game_map'] == filter_val:
                            filtered_files.append(game_file)

    pattern = re.compile(r'\S+([A-Z]{2}1_\d{10})[.]json')

    filtered_game_ids = []
    for file_path_str in filtered_files:
        for match in pattern.finditer(file_path_str):
            filtered_game_ids.append(match.group(1))
    return filtered_game_ids
