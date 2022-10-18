#!/usr/local/bin/python3
"""
    Run the following in the terminal in the LeagueSimulator directory.
    for i in {1..50}; do python3 gameReal.py; done
"""
import itertools
import random
import math
import pandas as pd
from pprint import pprint as pp
from time import sleep
import gameRun as gr
import numpy as np
from itertools import chain, zip_longest
from operator import itemgetter

list_of_teams = gr.teams
number_of_teams = len(list_of_teams)


def home_teams(list_of_teams):
    all_games = []
    for i in range(number_of_teams - 1):
        home = list_of_teams[:1] + list_of_teams[
            number_of_teams -i:] + list_of_teams[1:number_of_teams - i]
        all_games.append(home)
    return all_games


def first_round_fixtures(list_of_teams):
    half = int(len(list_of_teams) / 2)
    all_games = []
    for item in home_teams(list_of_teams):
        all_games.append(list(zip(item[:half], reversed(item[half:]))))

    a = [np.array(i) for i in all_games[::2]]
    b = [(y, x) for item in all_games[1::2] for x, y in item]
    c = np.array_split(b, int(len(b) / half))
    return list(filter(None.__ne__, chain.from_iterable(zip_longest(a, c))))


def reverse_round_fixtures(list_of_teams):
    all_games = first_round_fixtures(list_of_teams)
    for item in all_games:
        for pair in item:
            pair[0], pair[1] = pair[1], pair[0]
    return all_games


start = "\033[1m"
end = "\033[0;0m"

higher = 1.24768698355
lower = 1.004768698355

# higher = 1.24768698355
# lower = 1.004768698355



# RANDOM SYSTEM FOR HOME GOALS
def home_score(home, away):
    homeSkill = home.skill * 0.16666 + 0.09999*home.attack + 0.07499*home.attack
    awaySkill = away.skill * 0.16666 + 0.09999*away.attack + 0.07499*away.attack

    if homeSkill == awaySkill:
        raise ValueError

    if homeSkill > awaySkill:
        homeGoals = 0
        lambHome = higher ** (homeSkill - awaySkill)
        z = random.random()
        while z > 0:
            z = z - (((lambHome ** homeGoals) * math.exp(-1 * lambHome)) /
                     math.factorial(homeGoals))
            homeGoals += 1
        return (homeGoals - 1)

    if homeSkill < awaySkill:
        homeGoals = 0
        lambHome = higher ** (homeSkill - awaySkill)
        z = random.random()
        while z > 0:
            z = z - (((lambHome ** homeGoals) * math.exp(-1 * lambHome)) /
                     math.factorial(homeGoals))
            homeGoals += 1

        return (homeGoals - 1)


# RANDOM SYSTEM FOR AWAY GOALS
def away_score(home, away):
    homeSkill = home.skill / 3
    awaySkill = away.skill / 3

    if homeSkill == awaySkill:
        return "Teams cannot play themselves!!!"

    if awaySkill > homeSkill:
        awayGoals = 0
        lambAway = lower ** (homeSkill - awaySkill)
        x = random.random()
        while x > 0:
            x = x - (((lambAway ** awayGoals) * math.exp(-1 * lambAway)) /
                     math.factorial(awayGoals))
            awayGoals += 1
        return (awayGoals - 1)

    if awaySkill < homeSkill:
        awayGoals = 0
        lambAway = lower ** (homeSkill - awaySkill)
        x = random.random()
        while x > 0:
            x = x - (((lambAway ** awayGoals) * math.exp(-1 * lambAway)) /
                     math.factorial(awayGoals))
            awayGoals += 1
        return (awayGoals - 1)


def gameweeks(list_of_teams):
    number_of_games = 2 * len(list_of_teams) - 2
    complete_fixtures = reverse_round_fixtures(
        list_of_teams) + first_round_fixtures(list_of_teams)
    for game in range(number_of_games):
        print('_____________________________________________________________')
        print(f'              {start} Gameweek: {game + 1}  {end} ')
        print('_____________________________________________________________')
        log = []
        for item in complete_fixtures[game]:
            a = home_score(item[0], item[1])
            b = away_score(item[0], item[1])
            gr.match(item[0], item[1], (a, b))
            print(f'{item[0].name:>23}: {a}--{b} :{item[1].name}')
            # Sleep is used to make the simuation move slower.
            # sleep(0.1)
            log.append([item[0].name, item[0].played, item[0].wins, item[0].draws,
                        item[0].losses, item[0].scored, item[0].conceeded,
                        item[0].scored - item[0].conceeded, item[0].points])
            log.append([item[1].name, item[1].played, item[1].wins, item[1].draws,
                        item[1].losses, item[1].scored, item[1].conceeded,
                        item[1].scored - item[1].conceeded, item[1].points])
        # sleep(0.5)
        sorted_log = np.array(sorted(log, key=itemgetter(8, 7, 5), reverse=1))
        print('_____________________________________________________________')
        print(
            f'              {start} Gameweek: {game + 1}  Log Standing {end} ')
        print('_____________________________________________________________')
        gameweeks.final_log = pd.DataFrame(
            sorted_log, columns=['Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])
        gameweeks.final_log.index += 1
        print(gameweeks.final_log)
        # sleep(0.05)


def main():
    gameweeks(list_of_teams)
    """
        The code below stores the past years statistics on .txt files
    """
    with open('/Users/mac/PycharmProjects/LeagueSimulator/Records/league.txt',
              'a') as the_file:
        the_file.write(
            f'{gameweeks.final_log.iloc[0][0]:>20} : {gameweeks.final_log.iloc[0][8]:<15}\n')

    with open('/Users/mac/PycharmProjects/LeagueSimulator/Records/top_four.txt', 'a') as the_file:
        the_file.write(f'{gameweeks.final_log.iloc[0:4, 0:9]}\n')
        the_file.write('\n')

    with open('/Users/mac/PycharmProjects/LeagueSimulator/Records/league.txt', 
              'r') as a, open("/Users/mac/PycharmProjects/LeagueSimulator/Records/champions.txt", "w") as b:
        index = 1882
        for line in a:
            b.write("{:4d}: {}\n".format(index, line.rstrip()))
            index += 1
    print('')
    print('Winners')
    champions = pd.read_csv('/Users/mac/PycharmProjects/LeagueSimulator/Records/champions.txt',
                            sep=":", names=['Year', 'Winner', 'Points'], skipinitialspace=True)
    champions.index += 1
    champions['Occ_Number'] = champions.groupby("Winner").cumcount() + 1
    champions['Avg Pts'] = champions['Points'].expanding(1).mean().round(2)
    # more options can be specified also
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(champions)
    # champions.to_csv('/Users/mac/PycharmProjects/LeagueSimulator/Records/champions1.txt',sep="\t", columns=['Year', 'Winner', 'Points','Occ_Number','Avg Pts'])
    with open('/Users/mac/PycharmProjects/LeagueSimulator/Records/champions1.txt', 'w') as f:
        f.write(champions.__repr__())
    print('')
    print('Honours Log')
    print('____________________________')
    print(champions['Winner'].value_counts())
    with open('/Users/mac/PycharmProjects/LeagueSimulator/Records/winners1.txt', 'w') as f:
        f.write(champions['Winner'].value_counts().__repr__())
    s = champions.loc[champions['Points'].idxmax()]
    t = champions.loc[champions['Points'].idxmin()]
    # wins = gameweeks.final_log.loc[gameweeks.final_log['W'].idxmin()]

    print('')
    print(
        f"The highest points attained by the champions is {s['Points']} by {s['Winner']} in year {s['Year']}")
    print(
        f"The lowest points attained by the champions is {t['Points']} by {t['Winner']} in year {t['Year']}")


if __name__ == '__main__':
    main()
