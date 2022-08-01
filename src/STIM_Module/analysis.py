# import forehead as you
import numpy as np
import pandas as pd
import sqlite3 as sq
import ast
import random
from itertools import groupby, count



jungler_gold_tips = [
    "As Jungler, a mix of farming and going for high percentage ganks is what will get you large amounts of gold.",
    "Keep your jungle cleared and don't try to force things when clearing objectives lends more pressure.",
    "Farm farm farm. Don't wait in bushes, don't go bot/top if a gank/counter isn't a high probability.",
    "If the enemy jungler is bot and you're topside go take their camps and place wards.",
    "Taking the enemy jungler's camps denies him gold and forces him to gank / waste time, in which case your wards will spot him.",
    "Tax lanes after a successful gank (a way of not being behind in gold and experience).",
    "Don't tax a lane that can carry, and don't shove a wave that wants to be frozen (top lane especially).",
    "Search for a route where you can maximize your clear speed therefore your gold generation.",
    "If you're low ELO, farm more instead of ganking.",
]


# Snarky, Sarcastic, and downright Toxic comments
toxic_lol_tips = [
    "Please stop playing. You might think you're good but you're a bad person.",
    "Stop playing League of Legends. It's not fun.",
    "League of Legends is a lot like life. You can't win it all, but you can learn how to play it.",
    "League is cancer. It's not a game, it's a disease.",
    "You can't win if you're not playing.",
    "Do better forehead.",
    "The best synergy you'll have is during a surrender vote.",
    "The difference between your Yasuo and Moses is that Moses didn't overextend to clear the wave.",
    "Unless you're smurfing\nyou're all trash\nbut that doesn't mean you should give up\nor lose hope\nit's called garbage can\nnot garbage can not",
    "It's nice to see the Red Cross opening a food bank down there in bot lane.",
    "I know you're doing your best but please stop your team wants to win a game.",
    "You have as much impact in lane as that thing over there *proceeds to ping scuttle crab*",
    "Kayle Can Do It",
    "https://www.youtube.com/watch?v=664VCs3c1HU",
    "hey yas you been to the beach a lot this summer? cuz ur looking bronze as hell",
]




# GET USER DATA FROM SQLITE DB
def get_data(name, game_id, is_pro=False):
    # Weird name logic
    name = name[0] if is_pro else name
    
    game_id_digits = int(game_id[4:])
    connection = sq.connect("./data/game_data.db")
    cursor = connection.cursor()
    
    # Get Total Gold
    query = f'SELECT GOLDTL FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    total_gold = ast.literal_eval(str(cursor.fetchone())[2:-3])
    
    # Get Total XP
    query = f'SELECT XPTL FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    total_xp = ast.literal_eval(str(cursor.fetchone())[2:-3])
    
    # Get Gold Diff
    query = f'SELECT GLDDIFTL FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    gold_diff = ast.literal_eval(str(cursor.fetchone())[2:-3])
    
    list_of_mins = [i for i in range(len(total_gold))]

    df = pd.DataFrame(list(zip(list_of_mins, total_gold, total_xp, gold_diff)), columns=["Minute", "Total Gold", "Total Exp", "Gold Diff"])
    
    # Get Game Data
    query = f'SELECT CHAMPION_PLAYED FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    champion_played = str(cursor.fetchone())[2:-3]
    
    query = f'SELECT POSITION_PLAYED FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    position_played = str(cursor.fetchone())[2:-3]
    
    query = f'SELECT GAMEMODE FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    game_mode = str(cursor.fetchone())[2:-3]
    
    query = f'SELECT CC_SCORE FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    cc_score = cursor.fetchone()
    
    query = f'SELECT VISION_SCORE FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    vision_score = cursor.fetchone()
    
    query = f'SELECT CREEP_SCORE FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    creep_score = cursor.fetchone()
    
    # Get KDA
    query = f'SELECT KILLS FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    num_kills = cursor.fetchone()
    
    query = f'SELECT DEATHS FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    num_deaths = cursor.fetchone()
    
    query = f'SELECT ASSISTS FROM {"GAMEDATA_" + "".join(name.split())} WHERE ID={game_id_digits}'
    cursor.execute(query)
    num_assists = cursor.fetchone()
    
    
    game_data = [champion_played, position_played, game_mode, cc_score[0], vision_score[0], creep_score[0], num_kills[0], num_deaths[0], num_assists[0]]
    
    return df, game_data




# Gold analysis sub method
def gold_analysis(df): # Pass in raw dataframe
    gold_net = [500] * len(df)
    df['Gold Net'] = gold_net

    # Remove 20.4 gold per 10 seconds from gold data starting at 110 seconds
    for i in range(0, len(df)):
        gold_passive = 20.4 * (i*6 - 12)
        if gold_passive > 0:
            df.iloc[i, 4] = df.iloc[i, 1] - gold_passive
        else:
            df.iloc[i, 4] = df.iloc[i, 1]

    gpm = [0] * len(df)
    df['gpm'] = gpm

    for i in range(1, len(df)):
        df.iloc[i, 5] = df.iloc[i, 1] - df.iloc[i-1, 1] # Gold per minute
    
    avg_gpm = round(df["gpm"].mean())
    gpm_below_300 = df[df["gpm"] < 300]['Minute'][2:len(df)-2].tolist()
    
    return df, avg_gpm, gpm_below_300


# XP analysis sub method
def xp_analysis(df): # Pass in dataframe after gold_analysis is done
    xppm = [0] * len(df)
    df['xppm'] = xppm

    for i in range(1, len(df)):
        df.iloc[i, 6] = df.iloc[i, 2] - df.iloc[i-1, 2] # XP per minute
    
    avg_xppm = round(df["xppm"].mean())
    xp_below_300 = df[df["xppm"] < 300]['Minute'][2:len(df)-2].tolist()
    
    return df, avg_xppm, xp_below_300


# Combine gold and xp analysis
def do_analysis(df):
    df, avg_gpm, gpm_below_300 = gold_analysis(df)
    df, avg_xppm, xp_below_300 = xp_analysis(df)
    return df, avg_gpm, gpm_below_300, avg_xppm, xp_below_300



# Make range prints pretty
def format_group(group):
    group = [str(v) for v in group]
    if len(group) == 1:
        return group[0]
    elif len(group) == 2:
        return ', '.join(group)
    else:
        return f'{group[0]}-{group[-1]}'
    
def display_range(lst):
    idx = count()
    groups = [list(group) for key, group in groupby(lst, key=lambda item: item - next(idx))]
    return ', '.join(map(format_group, groups))


# IMPROVEMENT AREAS   
#  1        2      3     4       5        6      7       8    9
# GOLD, GOLD_DIFF, XP, KILLS, DEATHS, ASSISTS, VISION, CREEP, CC
    
    
# GOLD
def gold_improvement(avg_gpm, gpm_below_300):
    tips = []
    
    gold_tips = [
        "Kill some minions for gold: Melee = 22 gold, Caster = 17 gold, Siege = 45 gold, Super = 40 gold.",
        "At the start of the game, a wave of last-hit minions grants an average of 125 gold.",
        "Look to improve your kills count. Kills provide a lot of gold. Go for assists too.",
        "Lt hitting minions is the best way to get gold. Keep killing waves of them!",
        "Steal some jungle camps from your jungler for gold and xp.",
        "The outer turret is worth 100 gold with 250 additional gold for participating.",
        "The inner turret is worth 125 gold with 175 additional gold for participating.",
        "The inhibitor turret is worth 150 gold with 50 additional gold for participating.",
        "Destroying the nexus grants you 50 gold! This is important to get!",
        "If you cannot abuse your starting item for gold generation, then buy Ancient Coin instead.",
        "If your ADC is dead, hold the minion wave and last hit to get gold and cs.",
        "Practice first tower lane swapping to open up the map and get more gold",
        "If you've nearly completed your next item, but still need a little bit of gold, go to a side lane and farm until you've completed that item.",
    ]
    
    if (avg_gpm > 365):
        "The excellency you demonstrate! You're securely in DIAMOND level! Keep working hard!"
    elif (avg_gpm > 360):
        "Very well done! You're in PLATINUM level! DIAMOND is at 365. Keep at it!"
    elif (avg_gpm > 356):
        "Hey well done! You're in GOLD level! PLATINUM is at 360. You've got this!"
    elif (avg_gpm > 351):
        "You're in SILVER level! GOLD is at 356. Do your best!"
    else:
        "SILVER is at 351 gpm. To improve your rank improve your farm"
            
    if len(gpm_below_300) > 0:
        tips.append("You were below 300 gold per minute during these minutes: " + str(display_range(gpm_below_300)))
        tips.append(random.choice(gold_tips))
    
    return tips


# GOLD DIFF
def gold_diff_improvement(sum_df):
    tips = []
    
    gold_diff_tips = [
        "Farm farm farm. Don't wait in bushes, don't go bot/top if a gank/counter isn't a high probability.",
    ]
    
    avg_gold_diff = sum_df['Gold Diff'].mean()
    if avg_gold_diff > 2000:
        tips.append(f"Your oppenent across from you in the game had a serious gold advantage over you with an average difference of {avg_gold_diff}!")
        tips.append(random.choice(gold_diff_tips))
    elif avg_gold_diff > 1000:
        tips.append(f"Your oppenent across from you in the game had a strong gold advantage over you with an average difference of {avg_gold_diff}!")
        tips.append(random.choice(gold_diff_tips))
    elif avg_gold_diff > 500:
        tips.append(f"Your oppenent across from you in the game had a small gold advantage over you with an average difference of {avg_gold_diff}.")
        tips.append(random.choice(gold_diff_tips))
    elif avg_gold_diff < 0:
        tips.append("Congratulations! You had the gold advantage over your opponent! Use gold leads to put pressure on your opponent.")
    
    return tips



# XP
def xp_improvement(xp_below_300):
    tips = []
    
    xp_tips = [
        "You should try to farm more and level. Your teammates need your help!",
        "Farm farm farm. Don't wait in bushes, don't go bot/top if a gank/counter isn't a high probability.",
        "Last hitting minions is the best way to get experience.",
        "Hold the minion wave and last hit to get experience and cs.",
        "Steal some jungle camps from your jungler for gold and xp.",
    ]
    
    if len(xp_below_300) > 0:
        tips.append("You were below 300 XP per minute during these minutes: " + str(display_range(xp_below_300)))
        tips.append(random.choice(xp_tips))
    else:
        tips.append("Hey! Your XP per minute is above 300 across the board! You leveled quickly!")
    
    return tips



# KILLS
def kills_improvement(num_kills, kill_fail):
    tips = []
    
    kills_tips = [
        "If you see a deep ward in the bottom side of the map and the enemy are overextended, ping your team and try to teleport bot to help them. If you can get a kill or 2 in the bottom lane, you will be ahead, and so will your allies.",
        "Forcing the enemy bot lane out of their lane will mean they will fall behind in gold and XP as they will not secure any minions. Furthermore, their death timers allow your team to secure tower plates or take the Dragon afterwards.",
        "If you're a utility Support and someone is in base and is teleporting back to lane, give them a heal or a shield at the last possible second. If they decide to fight when they get back to lane, you will get an assist and free gold.",
        "Playing around your Ultimate is a very underrated strat. If you have an excellent Ultimate, make sure you're using it. Learn what your power spikes are.",
        "Grouping with your team is an essential thing to do. Even if you're a split pusher, you should be grouping with your team when they need you.",
        "If youve nearly completed your next item, but still need a little bit of gold, go to a side lane and farm until you've completed that item: especially if it's going to be very impactful in the upcoming fight.",
        "Making TP plays in any lane is very impactful. Just make sure that before you teleport, your allies are in a position to follow up.",
        "If you have a lead, try and snowball the lane to push your lead further."
        "Gank gank gank. Don't wait in bushes, don't go bot/top if a gank/counter isn't a high probability.",
    ]
    
    if num_kills < 5:
        if kill_fail:
            tips.append("To beat the PRO: " + random.choice(kills_tips))
        else:
            tips.append(random.choice(kills_tips))
    else:
        tips.append("You're a pro! You killed " + str(num_kills) + " enemies!")
    
    return tips



# DEATHS
def deaths_improvement(num_deaths, death_fail):
    tips = []
    
    death_tips = [
        "Learn and practice better poking strategies with your preferred champion.",
        "Study your teammates' skills and synergize with them in teamfights.",
        "Study what items pro players choose for your champion and practice with them.",
        "If you're playing a squishier champion, avoid going for risky fights. You'll come worse off.",
        "Study your opponents. By knowing their skills and more optimal stratgies you can form counterplays.",
        "Pick your fights carefully. Live to fight another day! If behind, stop fighting and focus on farming.",
    ]
    
    death_tips_b = [
        "To reduce your risk of death, optimize your combos.",
        "To reduce your risk of death, do not ward along in the later parts of the game.",
        "To reduce your risk of death, respect the enemies' power spkes.",
        "To reduce your risk of death, avoid constantly pushing the minion wave.",
        "To reduce your risk of death, check the minimap before initiating a fight.",
    ]
    
    if num_deaths > 10:
        tips.append("You died way too much. Try to avoid dying unnecessarily. It gives the enemy team a huge advantage.")
        
        if death_fail:
            tips.append("To beat the PRO: " + random.choice(death_tips))
        else:
            tips.append(random.choice(death_tips))
        tips.append(random.choice(death_tips_b))
    elif num_deaths > 5:
        tips.append("You died a good bit. Each death gives the enemy team an advantage over you.")
        if death_fail:
            tips.append("To beat the PRO: " + random.choice(death_tips))
        else:
            tips.append(random.choice(death_tips))
    
    return tips


    
# ASSISTS
def assists_improvement(num_assists, assist_fail):
    tips = []
    
    assist_tips = [
        "Maximize your abiliies to get the most assists.",
        "Focus on team fights to get gold from assists.",
        "Don't necessarily use your ultimate to get 1 assist, save it for a bigger impact.",
        "When you are in base, use an ability on a teleporting ally for a chance of getting an assist!",
    ]
    
    if num_assists > 10:
        if assist_fail:
            tips.append("To beat the PRO: " + random.choice(assist_tips))
        else:
            tips.append(random.choice(assist_tips))
    else:
        tips.append("You had a good amount of assists. Keep it up!")
    
    return tips



# VISION SCORE
def vision_improvement(game_time, vision_score):
    tips = []
    
    vision_tips = [
        "You obtain one Vision Score for each minute that your ward survives, so it's key to please at least two.",
        "Consider the distance between your wards and your base, the distance between them, and the time it passes between enemy champion discoveries from them.",
        "Increase your vision by placing control wards.",
        "Increase your vision by finding invisible enemy champions and epic monsters.",
        "Increase your vision by revealing enemy wards and destroying them.",
    ]
    
    if vision_score < 1.5 * game_time:
        tips.append(random.choice(vision_tips))
    else:
        tips.append("You have a good vision score. Keep it up!")
    
    return tips



# CREEP SCORE
def creep_improvement(game_time, creep_score):
    tips = []
    
    creep_tips = [
        "In 10 mins around 108 Minions spawn. Aim to get at least 65+. A Pro amount would be: 80+ and Godlike is: 100.",
        "Last hitting is extremely important. Try not to miss more than 2 last hits in a wave. Blow some cd's to reduce that number to 0 if able.",
        "Farming and not feeding wins games but you also have to know when to separate yourself from your farming to help the team.",
        "If your ADC is dead, hold the minion wave and last hit to get gold and cs.",
        "Hold the minion wave and last hit to get experience and cs.",
    ]
    
    if creep_score < 100 * game_time / 10:
        tips.append("You're not getting enough creep score. Practice last hitting.")
        tips.append(random.choice(creep_tips))
    else:
        tips.append("Your creep score is over 100 per 10 mins. You're godlike!")
    
    return tips



# CROWD CONTROL # TODO: Add more tips
def cc_improvement(cc_score):
    tips = []
    
    cc_tips = [
        
    ]
    
    if cc_score < 0:
        tips.append("You're not getting enough crowd control score. Practice your teamfights.")
    else:
        tips.append("Your crowd control score is over 0. You're godlike!")
    
    return tips





def just_the_tips(sum_name, sum_game_id, pro_name, pro_game_id):
    # Do data processing
    sum_df, sum_game_data = get_data(sum_name, sum_game_id)
    pro_df, pro_game_data = get_data(pro_name, pro_game_id, is_pro=True)
    
    sum_df, avg_gpm, gpm_below_300, avg_xppm, xp_below_300 = do_analysis(sum_df)
    pro_df, pro_avg_gpm, _, pro_avg_xppm, _ = do_analysis(pro_df)
    
    game_time = len(sum_df)
    
    
    #       0               1             2         3            4           5           6           7           8
    champion_played, position_played, game_mode, cc_score, vision_score, creep_score, num_kills, num_deaths, num_assists = sum_game_data
    pro_champion_played, pro_position_played, pro_game_mode, pro_cc_score, pro_vision_score, pro_creep_score, pro_num_kills, pro_num_deaths, pro_num_assists = pro_game_data
    
    # THE TIPS!
    tips = []
    
    
    # DISPLAY STATS
    tips.append(f'{sum_name} played {champion_played} in {position_played} position in {game_mode} mode.')
    tips.append(f'Your KDA is {num_kills}/{num_deaths}/{num_assists} with Vision: {vision_score} | Creep: {creep_score} | CC: {cc_score} | Avg. GPM: {avg_gpm} | Avg. XP/min: {avg_xppm}')
    tips.append("")
    
    
    # COMPARE TO PRO PLAYER
    tips.append("Compared to your PRO player:")
    
    # GOLD AND XP COMPARISION
    avg_gpm_diff =  pro_avg_gpm - avg_gpm
    avg_xppm_diff = pro_avg_xppm - avg_xppm
    
    if (avg_gpm_diff > 0) and (avg_xppm_diff > 0):
        tips.append(f"The PRO had {avg_gpm_diff} more gold and {avg_xppm_diff} more xp per minute than you. Focus on last hits, farm routes, and timers.")
    elif (avg_gpm_diff > 0):
        tips.append(f"The PRO had {avg_gpm_diff} more gold per minute than you. Focus on last hits, farm routes, and timers.")
    elif (avg_xppm_diff > 0):
        tips.append(f"The PRO had {avg_xppm_diff} more xp per minute than you. Focus on last hits, farm routes, and timers.")
    else:
        tips.append("You performed better than the PRO. Try to repeat your last hits, farm routes, and timers like this game.")
    
    
    # KDA COMPARISON
    if (num_deaths != 0): 
        player_ratio = (num_kills + num_assists) / num_deaths
    else: # if player never dies
        player_ratio = (num_kills + num_assists) / 1
        
    if (pro_num_deaths != 0):
        pro_ratio = (pro_num_kills + pro_num_assists) / pro_num_deaths
    else: # if pro player never dies
        pro_ratio = (pro_num_kills + pro_num_assists) / 1
    
    kill_fail, death_fail, assist_fail = False, False, False
    
    if (player_ratio > pro_ratio):
        tips.append(f"You had a better KDA than the PRO. Try to repeat your last hits, farm routes, and timers like this game.")
    else:
        tips.append(f"The PRO had a better KDA than you. Focus on the mentioned issues below to see where you can improve.")
        if (pro_num_kills > num_kills):
            kill_fail = True
            tips.append(f"You had fewer kills than the PRO. In a vacuum this is ok, however, if you're playing a damage oriented character, this may be an issue to address.")
        if (pro_num_assists > num_assists):
            assist_fail = True
            tips.append(f"You had fewer assists than the PRO. Unless you were getting the majority of the kills, you need to participate more in team fights and improve your kill participation.")
        if (num_deaths > pro_num_deaths):
            death_fail = True
            tips.append(f"You had more deaths than the PRO. This can be ok, but if you're not playing a support character, you may need to adjust your positioning in teamfights and increase your ward vision.")
    
    
    # VISION, CREEP, CC COMPARISION
    if (vision_score > pro_vision_score):
        tips.append("Your vision, creep, and crowd control scores were better than the PRO. Well done!")
    else:
        scores_pro = []
        if (pro_vision_score > vision_score):
            scores_pro.append(f"Vision was {pro_vision_score - vision_score} more")
        elif (pro_vision_score < vision_score):
            scores_pro.append(f"Vision was {vision_score - pro_vision_score} less")
        
        if (pro_creep_score > creep_score):
            scores_pro.append(f"Creep was {pro_creep_score - creep_score} more")
        elif (pro_creep_score < creep_score):
            scores_pro.append(f"Creep was {creep_score - pro_creep_score} less")
        
        if (pro_cc_score > cc_score):
            scores_pro.append(f"CC was {pro_cc_score - cc_score} more")
        elif (pro_cc_score < cc_score):
            scores_pro.append(f"CC was {cc_score - pro_cc_score} less")
        
        tips.append("The PRO's: " + " | ".join(scores_pro))
    
    
    
    tips.append("")
    tips.append("Tips for Improvement:")
    
    
    # DISPLAY TWO AREAS OF IMPROVEMENT AT RANDOM
    improvement_areas = ["GOLD", "GOLD_DIFF", "XP", "KILLS", "DEATHS", "ASSISTS", "VISION", "CREEP"] # , "CC"
    improvements = random.sample(improvement_areas, 2)
    
    for idx, improvement in enumerate(improvements):
        match improvement:
            case 'GOLD' | 1:
                tips += gold_improvement(avg_gpm, gpm_below_300)
            case 'GOLD_DIFF' | 2:
                tips += gold_diff_improvement(sum_df)
            case 'XP' | 3:
                tips += xp_improvement(xp_below_300)
            case 'KILLS' | 4:
                tips += kills_improvement(num_kills, kill_fail)
            case 'DEATHS' | 5:
                tips += deaths_improvement(num_deaths, death_fail)
            case 'ASSISTS' | 6:
                tips += assists_improvement(num_assists, assist_fail)
            case 'VISION' | 7:
                tips += vision_improvement(game_time, vision_score)
            case 'CREEP' | 8:
                tips += creep_improvement(game_time, creep_score)
            case 'CC' | 9:
                tips += cc_improvement(cc_score)
        
        # if idx != len(improvements) - 1:
            # tips.append("")
    
    
    
    
    return tips # Just the tips...



