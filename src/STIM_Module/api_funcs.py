import asyncio
import csv
import json
import os
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime as dt

import requests as rq

from STIM_Module.API_KEY import API_KEY
from STIM_Module.new_exceptions import *

QUEUE = []


def respect_rate_limit(url):
    # print(f'call made: {str(url)[:-51]}')
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


def call_api_for_gamedata(game_id, timeline=False):
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

    return data, game_id, timeline


def get_raw_game_data(game_ids):
    data_return = []
    threads = []
    for game_id in game_ids:
        data_return.append((None, None, None))
        data_return.append((None, None, None))

    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(len(game_ids)):
            threads.append(executor.submit(call_api_for_gamedata, game_ids[i]))
            threads.append(executor.submit(call_api_for_gamedata, game_ids[i], True))

        i = 0
        for future in as_completed(threads):
            try:
                data, game_id, is_timeline = future.result()
                data_return[i] = (data, game_id, is_timeline)
            except Exception as e:
                print(e)
            i += 1

    return data_return


def collect_data_for_rank(queue="RANKED_SOLO_5x5", tier="DIAMOND", division="I", summoner_name_return=[]):
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
        summoner_name = data[7]['summonerName']
        create_sqlite_db(summoner_name)  # Creates a table in the database
        game_ids = get_recent_game_ids(get_summoner(summoner_name)[0], num_games=20)
        add_data_to_db(summoner_name, num_games=3, recent_game_ids=game_ids, is_pro=True)
        summoner_name_return.append(summoner_name)
    else:
        print("Error code" + str(response.status_code))


def get_recent_game_ids(puuid, num_games=1):
    response = respect_rate_limit("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) +
                                  "/ids?start=0&count=" + str(num_games) + "&api_key=" + API_KEY)

    if response.status_code == 200:
        return json.loads(json.dumps(response.json()))
    else:
        raise APICallResponseException(response.status_code)


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


def get_summoner_scores(raw_game_data, puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    creep_score = raw_game_data['info']['participants'][summoner_index]['totalMinionsKilled']
    cc_score = raw_game_data['info']['participants'][summoner_index]['timeCCingOthers']
    vision_score = raw_game_data['info']['participants'][summoner_index]['visionScore']

    return creep_score, cc_score, vision_score


def get_summoner_kda_stats(raw_game_data, raw_game_timeline_data, puuid):
    summoner_index = raw_game_data['metadata']['participants'].index(puuid)

    kills = raw_game_data['info']['participants'][summoner_index]['kills']
    deaths = raw_game_data['info']['participants'][summoner_index]['deaths']
    assists = raw_game_data['info']['participants'][summoner_index]['assists']

    kill_timestamps = []
    death_timestamps = []
    assist_timestamps = []

    for i in range(len(list(raw_game_timeline_data['info']['frames']))):
        events_this_min = list(raw_game_timeline_data['info']['frames'][i]['events'])

        kills_this_min = []
        deaths_this_min = []
        assists_this_min = []
        default_value = [-1]

        for j in range(len(events_this_min)):
            if dict(events_this_min[j])['type'] == "CHAMPION_KILL":
                if int(dict(events_this_min[j])["killerId"]) == summoner_index + 1:
                    kills_this_min.append(dict(events_this_min[j]))
                elif int(dict(events_this_min[j])["victimId"]) == summoner_index + 1:
                    deaths_this_min.append(dict(events_this_min[j]))
                else:
                    assist_ids_this_kill = dict(events_this_min[j]).get('assistingParticipantIds', default_value)
                    if int(summoner_index + 1) in list(assist_ids_this_kill):
                        assists_this_min.append(dict(events_this_min[j]))

        for event in kills_this_min:
            kill_timestamps.append(event['timestamp'])
        for event in deaths_this_min:
            death_timestamps.append(event['timestamp'])
        for event in assists_this_min:
            assist_timestamps.append(event['timestamp'])

    return kills, deaths, assists, kill_timestamps, death_timestamps, assist_timestamps


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


def create_sqlite_db(summoner_name):
    if not os.path.exists("./data"):
        os.makedirs("./data")

    connection = sqlite3.connect("./data/game_data.db")
    cursor = connection.cursor()

    try:
        query = f'''CREATE TABLE {"GAMEDATA_" + "".join(summoner_name.split())} 
        (ID INT PRIMARY KEY,
        REGION CHAR(5) NOT NULL,
        VICTORY INTEGER NOT NULL,
        CHAMPION_PLAYED CHAR(25) NOT NULL,
        POSITION_PLAYED CHAR(7),
        GAMEMODE CHAR(7),
        ENDED_IN_SURRENDER INTEGER,
        CC_SCORE INTEGER,
        VISION_SCORE INTEGER,
        CREEP_SCORE INTEGER,
        KILLS INTEGER,
        DEATHS INTEGER,
        ASSISTS INTEGER,
        KILLTL CHAR(300),
        DEATHTL CHAR(300),
        ASSISTTL CHAR(300),
        GOLDTL CHAR(300) NOT NULL,
        XPTL CHAR(300) NOT NULL,
        GLDDIFTL CHAR(300) NOT NULL);'''
        cursor.execute(query)
        connection.commit()
    except sqlite3.OperationalError as e:
        print(e, ": Assuming that .db file exists without error. Continuing", sep="")

    connection.close()


def add_data_to_db(summoner_name, summoner_puuid=None, num_games=3, recent_game_ids=None, is_pro=False):
    connection = sqlite3.connect("data/game_data.db")
    cursor = connection.cursor()

    if summoner_puuid is None:
        summoner_puuid = get_summoner(summoner_name)[0]

    if recent_game_ids is None:
        recent_game_ids = get_recent_game_ids(summoner_puuid, num_games)

    recent_game_ids_useable = [None] * len(recent_game_ids)

    i = 0
    for val in recent_game_ids:
        recent_game_ids_useable[i] = val
        i += 1

    pattern = re.compile(r'([A-Z]{2}1)_(\d{10})')

    # check if games are already present and if they are remove them from needed calls

    query = f'''SELECT ID, REGION FROM {"GAMEDATA_" + "".join(summoner_name.split())};'''
    cursor.execute(query)
    existing_ids = cursor.fetchall()

    added_games = 0

    for id_tup in existing_ids:
        numeric = id_tup[0]
        region = id_tup[1]
        try:
            recent_game_ids_useable.remove(region + "_" + str(numeric))
            added_games += 1
        except Exception:
            pass

    loop_index = 0

    print(f'games already in db for {summoner_name}: {added_games}')
    while added_games < num_games:
        # collect all of the data (in no particular order)
        games_of_focus = recent_game_ids_useable[num_games * loop_index:num_games * (loop_index+1)]
        data = get_raw_game_data(games_of_focus)

        for game_id in games_of_focus:
            for api_return in data:
                if api_return[1] == game_id:
                    if api_return[2]:
                        raw_game_timeline_data = api_return[0]
                    else:
                        raw_game_data = api_return[0]

            game_len = len(list(raw_game_timeline_data['info']['frames']))

            if game_len <= 10 and is_pro:
                print("game skipped because too short")
            else:
                match = re.match(pattern, str(game_id))

                db_id = int(match.group(2))
                region_id = match.group(1)

                champ, position, victory = get_general_summoner_stats(raw_game_data, summoner_puuid)
                gamemode, gamemap, datetime, surrender = get_game_stats(raw_game_data)
                gold_timeline = str(get_summoner_gold_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[2])
                xp_timeline = str(get_summoner_exp_stats(raw_game_data, raw_game_timeline_data, summoner_puuid)[1])
                gold_diff_timeline = str(get_gold_diff_timeline(raw_game_data, raw_game_timeline_data, summoner_puuid))

                creep_score, cc_score, vision_score = get_summoner_scores(raw_game_data, summoner_puuid)
                kills, deaths, assists, kill_timestamps, death_timestamps, assist_timestamps = get_summoner_kda_stats(
                    raw_game_data, raw_game_timeline_data, summoner_puuid)

                params = [db_id, region_id, victory, champ, position, gamemode, surrender, cc_score, vision_score,
                          creep_score,
                          kills, deaths, assists, str(kill_timestamps), str(death_timestamps), str(assist_timestamps),
                          gold_timeline, xp_timeline, gold_diff_timeline]

                try:
                    query = f'''INSERT INTO {"GAMEDATA_" + "".join(summoner_name.split())} 
                                            (ID,REGION,VICTORY,CHAMPION_PLAYED,POSITION_PLAYED,GAMEMODE,ENDED_IN_SURRENDER,CC_SCORE,
                                            VISION_SCORE,CREEP_SCORE,KILLS,DEATHS,ASSISTS,KILLTL,DEATHTL,ASSISTTL,GOLDTL,XPTL,GLDDIFTL) 
                                            VALUES
                                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                    cursor.execute(query, params)
                    added_games += 1
                except sqlite3.IntegrityError as e:
                    print(e, ": Skipping entry and continuing", sep="")
                connection.commit()
            loop_index += 1
    connection.close()


def filter_games(summoner_name, filter_attr=None, filter_val=None):
    filter_attributes = ["VICTORY", "CHAMPION_PLAYED", "POSITION_PLAYED", "GAMEMODE", "ENDED_IN_SURRENDER"]
    champions = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Ashe', 'AurelionSol', 'Azir',
                 'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki',
                 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'FiddleSticks',
                 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Hecarim', 'Heimerdinger',
                 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kalista', 'Karma',
                 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc',
                 'LeeSin', 'Leona', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi',
                 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Nidalee',
                 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Pantheon', 'Poppy', 'Quinn', 'Rammus', 'RekSai', 'Renekton',
                 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Sejuani', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir',
                 'Skarner', 'Sona', 'Soraka', 'Swain', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo',
                 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus',
                 'Vayne', 'Veigar', 'Velkoz', 'Vi', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xerath', 'XinZhao',
                 'Yasuo', 'Yorick', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zyra']
    positions = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
    game_modes = ['CLASSIC', 'ARAM', 'ULTBOOK']
    game_maps = []

    connection = sqlite3.connect("data/game_data.db")
    cursor = connection.cursor()

    if filter_attr not in filter_attributes:
        if filter_attr is None and filter_val is None:
            cursor.execute(f'SELECT REGION, ID, VICTORY FROM {"GAMEDATA_" + "".join(summoner_name.split())}')
            return cursor.fetchall()
        raise InvalidParamException("filter_attr")
    elif filter_attr == 'CHAMPION_PLAYED' and filter_val not in champions:
        raise InvalidParamException("filter_val", "Champion not implemented yet")
    elif filter_attr == 'VICTORY':
        if filter_val is True:
            filter_val = 1
        elif filter_val is False:
            filter_val = 0
        elif filter_val == 0 or filter_val == 1:
            filter_val = filter_val
        else:
            raise InvalidParamException("filter_val", "Value could not be converted to boolean")
    elif filter_attr == 'POSITION_PLAYED' and filter_val not in positions:
        raise InvalidParamException("filter_val", "Position does not exist")
    elif filter_attr == 'GAMEMODE' and filter_val not in game_modes:
        raise InvalidParamException("filter_val", "Invalid game mode")
    elif filter_attr == 'ENDED_IN_SURRENDER':
        try:
            if bool(filter_val):
                filter_val = 1
            else:
                filter_val = 0
        except Exception:
            raise InvalidParamException("filter_val", "Value could not be converted to boolean")
    elif filter_attr == 'GAME_MAP' and filter_val not in game_maps:
        raise InvalidParamException("filter_val", "Invalid game map")

    if type(filter_val) == str:
        filter_val = '\"' + filter_val + '\"'

    query = f'SELECT ID FROM {"GAMEDATA_" + "".join(summoner_name.split())} WHERE {filter_attr}={filter_val}'

    cursor.execute(query)
    entries = cursor.fetchall()
    return [entry[0] for entry in entries]


# The below functions are old/unused and may break things


def filter_games_json(summoner_name, filter_attr, filter_val):
    # NOTE: filter_games_json has been deprecated due to the performance enhancement provided by sqlite3 therefore it might
    # break upon use in the future
    filter_attributes = ["victory", "champion_played", "position_played", "game_mode", "ended_in_surrender"]
    champions = ['MasterYi', 'Garen', 'Lucian']
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


def make_game_csv(summoner_name, summoner_puuid=None, num_games=3, recent_game_ids=None):
    # NOTE: this function is going to be deprecated shortly because of the efficiencies afforded by writing to a sqlite3
    # database. Program may break upon use in the future

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
                         'game_time': str(game_datetime), 'game_map': game_map,
                         'ended_in_surrender': ended_in_surrender}

            json.dump(data_dict, outfile)

    return filenames


def collect_data_for_rank_oldver(queue="RANKED_SOLO_5x5", tier="DIAMOND", division="I"):
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
        make_game_csv(summoner_name, num_games=3)
    else:
        print("Error code" + str(response.status_code))
