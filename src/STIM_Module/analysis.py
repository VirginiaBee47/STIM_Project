# import forehead as you
import numpy as np
import pandas as pd
import sqlite3 as sq
import ast
import random
from itertools import groupby, count




basic_gold_earn = [
    "Minions: Melee = 22 gold, Caster = 17 gold, Siege = 45 gold, Super = 40 gold.",
    "At the start of the game, a wave of last-hit minions grants an average of 125 gold"
    "The best way to get gold is by killing minions.",
    "Last hitting minions is the best way to get gold.",
    "Turrets give gold globally to the whole team.",
    "The outer turret is worth 100 gold with 250 additional gold for participating.",
    "The inner turret is worth 125 gold with 175 additional gold for participating.",
    "The inhibitor turret is worth 150 gold with 50 additional gold for participating.",
    "The nexus turret is worth 50 gold.",
    "Destroying the nexus grants you 50 gold! This is important to get!",
]


support_gold_tips = [
    "Maximize your abiliies to get the most assists.",
    "Focus on team fights to get gold from assists.",
    "Don't necessarily use your ultimate to get 1 assist, save it for a bigger impact.",
    "When you are in base, use an ability on a teleporting ally for a chance of getting an assist!",
    "If you cannot abuse your starting item for gold generation, then buy Ancient Coin instead.",
    "If your ADC is dead, hold the minion wave and last hit to get gold and cs.",
    "Practice first tower lane swapping to open up the map and get more gold"
]


jungler_gold_tips = [
    "As Jungler, a mix of farming and going for high percentage ganks is what will get you large amounts of gold.",
    "Keep your jungle cleared and don't try to force things when clearing objectives lends more pressure.",
    "Farm farm farm. Don't wait in bushes, don't go bot/top if a gank/counter isn't a high probability.",
    "If the enemy jungle is bot and you're topside go take their camps and place wards.",
    "Taking those camps denies him gold and forces him to gank / waste time, in which case your wards will spot him.",
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
    name = name[0] if is_pro else name.get()
    
    game_id_digits = int(game_id[4:])
    connection = sq.connect("data/game_data.db")
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
    gpm_below_300 = df[df["gpm"] < 300]['Minute'][1:-1].tolist()
    
    return df, avg_gpm, gpm_below_300


# XP analysis sub method
def xp_analysis(df): # Pass in dataframe after gold_analysis is done
    xppm = [0] * len(df)
    df['xppm'] = xppm

    for i in range(1, len(df)):
        df.iloc[i, 6] = df.iloc[i, 2] - df.iloc[i-1, 2] # XP per minute
    
    avg_xppm = round(df["xppm"].mean())
    xp_below_300 = df[df["xppm"] < 300]['Minute'][1:-1].tolist()
    
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
def gold_improvement(tips, avg_gpm, gpm_below_300):
    if (avg_gpm > 365):
        "The excellency you demonstrate! You're securely in DIAMOND level! Keep working hard!"
    elif (avg_gpm > 360):
        "Very well done! You're in PLATINUM level! DIAMOND is at 365. Keep at it!"
    elif (avg_gpm > 356):
        "Hey well done! You're in GOLD level! PLATINUM is at 360. You've got this!"
    elif (avg_gpm > 351):
        "You're in SILVER level! GOLD is at 356. Do your best!"
    else:
        "SILVER is at 351 gpm. Work hard!"
            
    if len(gpm_below_300) > 0:
        tips.append("You were below 300 gold per minute during these minutes: " + str(display_range(gpm_below_300)))



# GOLD DIFF
def gold_diff_improvement(tips, sum_df):
    avg_gold_diff = sum_df['GOLD'].mean()
    if avg_gold_diff > 2000:
        tips.append(f"But your oppenent across from you in the game had a serious gold advantage over you with an average difference of {avg_gold_diff}!")
    elif avg_gold_diff > 1000:
        tips.append(f"But your oppenent across from you in the game had a strong gold advantage over you with an average difference of {avg_gold_diff}!")
    elif avg_gold_diff > 500:
        tips.append(f"But your oppenent across from you in the game had a small gold advantage over you with an average difference of {avg_gold_diff}.")





# XP
def xp_improvement(tips, avg_xppm, xp_below_300):
    if len(xp_below_300) > 0:
        tips.append("You were below 300 XP per minute during these minutes: " + str(display_range(xp_below_300)))
        tips.append("You should try to farm more and level. Your teammates need your help!")
    else:
        tips.append("Hey! Your XP per minute is above 300 across the board! You leveled quickly!")
    
    
    
# KILLS
def kills_improvement(tips, num_kills):
    pass
    
    
    
    
    
# DEATHS
def deaths_improvement(tips, num_deaths):
    death_tips = [
        "Learn and practice better poking strategies with your preferred champion.",
        "Study your teammates' skills and synergize with them in teamfights.",
        "Study what items pro players choose for your champion and practice with them.",
        "If you're playing a squishier champion, avoid going for risky fights. You'll come worse off."
        "Study your opponents. By knowing their skills and more optimal stratgies you can form counterplays."
    ]
    
    death_tips_b = [
        "To reduce your risk of death, optimize your combos.",
        "To reduce your risk of death, do not ward alonge in the later parts of the game.",
        "To reduce your risk of death, respect the enemies' power spkes.",
        "To reduce your risk of death, avoid constantly pushing the minion wave.",
        "To reduce your risk of death, check the minimap before initiating a fight.",
    ]
    
    death_tips_c = [
        "Please stop dying so much. Practice more to improve your skills and champion handling.",
    ]
    
    if num_deaths > 10:
        tips.append("You died way too much. Try to avoid dying unnecessarily. It gives the enemy team a huge advantage.")
        tips.append(random.choice(death_tips))
        tips.append(random.choice(death_tips_b))
        tips.append(random.choice(death_tips_c))
    elif num_deaths > 5:
        tips.append("You died a lot. Try to avoid dying unnecessarily. It gives the enemy team an advantage.")
        tips.append(random.choice(death_tips))
        tips.append(random.choice(death_tips_b))
    

    
# ASSISTS
def assists_improvement(tips, num_assists):
    pass
    
    
    
    
# VISION
def vision_improvement(tips, vision_score):
    pass
    
    
    
# CREEP
def creep_improvement(tips, creep_score):
    pass
    
    
    
# CC
def cc_improvement(tips, cc_score):
    pass





def just_the_tips(sum_name, sum_game_id, pro_name, pro_game_id):
    # Do data processing
    sum_df, sum_game_data = get_data(sum_name, sum_game_id)
    pro_df, _ = get_data(pro_name, pro_game_id, is_pro=True)
    
    sum_df, avg_gpm, gpm_below_300, avg_xppm, xp_below_300 = do_analysis(sum_df)
    pro_df, pro_avg_gpm, _, pro_avg_xppm, _ = do_analysis(pro_df)
    
    print(sum_df) # TODO: Remove dev print
    print(sum_game_data) # TODO: Remove dev print
    
    
    #       0               1             2         3            4           5           6           7           8
    champion_played, position_played, game_mode, cc_score, vision_score, creep_score, num_kills, num_deaths, num_assists = sum_game_data
    
    
    # THE TIPS!
    tips = []
    
    
    # DISPLAY STATS
    tips.append(f'{sum_name} played {champion_played} in {position_played} position in {game_mode} mode.')
    tips.append(f'Your KDA is {num_kills}/{num_deaths}/{num_assists} with Vision: {vision_score} | Creep: {creep_score} | CC: {cc_score}.')
    tips.append(f'Your average gold per minute is {avg_gpm} | Your average XP per minute is {avg_xppm}')
    tips.append("")
    
    
    
    # DISPLAY TWO AREAS OF IMPROVEMENT AT RANDOM
    improvement_areas = ["GOLD", "GOLD_DIFF", "XP", "KILLS", "DEATHS", "ASSISTS", "VISION", "CREEP", "CC"]
    
    for _ in range(2):
        improvement_area = random.sample(improvement_areas)
        
        match improvement_area:
            case 'GOLD' | 1:
                tips = gold_improvement(tips, avg_gpm, gpm_below_300)
            case 'GOLD_DIFF' | 2:
                tips = gold_diff_improvement(tips, sum_df)
            case 'XP' | 3:
                tips = xp_improvement(tips, avg_xppm, xp_below_300)
            case 'KILLS' | 4:
                tips = kills_improvement(tips, num_kills)
            case 'DEATHS' | 5:
                tips = deaths_improvement(tips, num_deaths)
            case 'ASSISTS' | 6:
                tips = assists_improvement(tips, num_assists)
            case 'VISION' | 7:
                tips = vision_improvement(tips, vision_score)
            case 'CREEP' | 8:
                tips = creep_improvement(tips, creep_score)
            case 'CC' | 9:
                tips = cc_improvement(tips, cc_score)
    
    
    
    # DISPLAY COMPARISON TO PRO PLAYER
    avg_gpm_diff = avg_gpm - pro_avg_gpm
    avg_xppm_diff = avg_xppm - pro_avg_xppm
    
    tips.append("Compared to your pro player:")
    
    if (avg_gpm_diff < 0) and (avg_xppm_diff < 0):
        tips.append(f"The PRO had {avg_gpm_diff} more gold and {avg_xppm_diff} more xp per minute than you. Work harder!")
    elif (avg_gpm_diff < 0):
        tips.append(f"The PRO had {avg_gpm_diff} more gold per minute than you. Work harder!")
    elif (avg_xppm_diff < 0):
        tips.append(f"The PRO had {avg_xppm_diff} more xp per minute than you. Work harder!")
    else:
        tips.append("You performed better than the PRO. Keep it up!")
    
    
    
    
    
    return tips # Just the tips...



