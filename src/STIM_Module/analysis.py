# import forehead as you
import numpy as np
import pandas as pd
import random
from itertools import groupby, count



df = pd.read_csv("data/bEANS47_NA1_4386437748.csv")

# data = {
#   "Minute": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
#   "Total Gold": [50, 40, 45],
#   "Total Exp": [100, 90, 95, 75, 80, 85],
#   "Gold Diff": [10, 20, 30, 40, 50, 60],
# }

# # load data into a DataFrame object:
# df = pd.DataFrame(data)


# TODO: Compare USER against PRO
# TODO: Ignore games with -1 values for gold differential stats

# Gold analysis
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


# XP analysis
def xp_analysis(df): # Pass in dataframe after gold_analysis is done
    xppm = [0] * len(df)
    df['xppm'] = xppm

    for i in range(1, len(df)):
        df.iloc[i, 6] = df.iloc[i, 2] - df.iloc[i-1, 2] # XP per minute
    
    avg_xppm = round(df["xppm"].mean())
    xp_below_300 = df[df["xppm"] < 300]['Minute'][1:-1].tolist()
    
    return df, avg_xppm, xp_below_300




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





life_tips = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "If you don't know where you are, you might as well be lost.",
    "The only thing worse than being blind is having a good idea.",
    "The only thing we have to fear is fear itself.",
    "I'm not a great programmer; I'm just a good programmer with bad habits.",
    "A good programmer is someone who always looks both ways before crossing a one-way street.",
    "If you're not willing to risk the usual, you're not a good programmer.",
    "Bootstrap is not a framework, it's a toolkit.",
    "Life is like a box of chocolates. There are no right or wrong ways to eat them.",
    "League of Legends is a lot like life. You can't win it all, but you can learn how to play it.",
    "The best way to predict the future is to invent it.",
    "The best way to keep your secrets is to keep them from other people.",
    "The best way to find yourself is to lose yourself in the service of others.",
    "The best way to turn a problem into a solution is to make it a problem for yourself.",
    "Turn off the lights. It's easier to see than to be able to see.",
    "Turn off your computer. Go outside and play.",
    "Turn off your cell phone. Go outside and play.",
    "Turn off your TV. Go outside and play.",
    "Turn off your water heater. Go outside and play.",
    "Play the game. It's fun. It's fun if it works.",
    "Play Pokemon Go. Catch a lot of Pokemon.",
    "Home is where the heart is.",
    "Homebrew is where the code is.",
]


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


gold_tips = [
    "",
]


exp_tips = [
    "",
]


lol_tips = [
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


def just_the_tips(df):
    # Do data processing
    dev_print = False
    
    df, avg_gpm, gpm_below_300 = gold_analysis(df)
    df, avg_xppm, xp_below_300 = xp_analysis(df)
    
    
    if dev_print:
        print(df)
        print(gpm_below_300)
        print(xp_below_300)
        print("\nEND DEV\n")
    
    tips = []
    
    tips.append("For this game, you averaged around {:d} gold and {:d} xp per minute\n".format(avg_gpm, avg_xppm))
    
    # Print gold info
    if len(gpm_below_300) > 0:
        tips.append("You were below 300 gold per minute during these minutes: " + str(display_range(gpm_below_300)))
        tips.append("The silver tier is generally around 351 gpm.")
    else:
        tips.append("Hey! Your GPM is above 300! You should be proud of yourself!")
    
    # Print xp info
    if len(xp_below_300) > 0:
        tips.append("You were below 300 XP per minute during these minutes: " + str(display_range(xp_below_300)))
        tips.append("You should try to improve your XP per minute by playing more games.")
    else:
        tips.append("Hey! Your XP per minute is above 300! You should be proud of yourself!")
    
    
    # Print tips
    tips.append("\nHere are some tips to help you improve:")
    
    
    # Based on conditions, return a list of tips
    tips.append("Life Tip: " + random.choice(life_tips))
    tips.append("Gold Tip: " + random.choice(support_gold_tips))
    tips.append("Exp Tip: " + random.choice(jungler_gold_tips))
    
    # Tiny chance for a snarky tip
    if random.random() < 0.01:
        tips.append("LOL Tip: " + random.choice(lol_tips))
    
    return tips











print(*just_the_tips(df), sep = "\n")


