import pandas as pd

# Open the csv file
path = 'F:/scores_of_allseason.csv'
csv_data = pd.read_csv(path)
teams = csv_data['team1'].unique()

# Transform the dataframe
winner_before = csv_data[csv_data.result_score1 == 1]
winner_before = winner_before[winner_before.result_score2 == 0]
winner_after = csv_data[csv_data.result_score1 == 0]
winner_after = winner_after[winner_after.result_score2 == 1]
draw = csv_data[csv_data.result_score1 == 0]
draw = draw[draw.result_score2 == 0]

# Get the proper table structure
competitions_without_draw = []
competitions_draw = []
for i, row in winner_before.iterrows():
    winner = row['team1']
    loser = row['team2']
    competitions_without_draw.append((winner,loser))
for j, row in winner_after.iterrows():
    winner = row['team2']
    loser = row['team1']
    competitions_without_draw.append((winner,loser))
for k, row in winner_after.iterrows():
    team1 = row['team1']
    team2 = row['team2']
    competitions_draw.append((team1,team2))

# BTmodel
import numpy as np
import choix

n_items = 12
# Transfrom the data
for i in range(len(competitions_without_draw)):
    contest = list(competitions_without_draw[i])
    if contest[0] == 'SFS': contest[0] = 0
    if contest[0] == 'VAL': contest[0] = 1
    if contest[0] == 'SHD': contest[0] = 2
    if contest[0] == 'GLA': contest[0] = 3
    if contest[0] == 'DAL': contest[0] = 4
    if contest[0] == 'SEO': contest[0] = 5
    if contest[0] == 'LDN': contest[0] = 6
    if contest[0] == 'FLA': contest[0] = 7
    if contest[0] == 'PHI': contest[0] = 8
    if contest[0] == 'HOU': contest[0] = 9
    if contest[0] == 'BOS': contest[0] = 10
    if contest[0] == 'NYE': contest[0] = 11
    if contest[1] == 'SFS': contest[1] = 0
    if contest[1] == 'VAL': contest[1] = 1
    if contest[1] == 'SHD': contest[1] = 2
    if contest[1] == 'GLA': contest[1] = 3
    if contest[1] == 'DAL': contest[1] = 4
    if contest[1] == 'SEO': contest[1] = 5
    if contest[1] == 'LDN': contest[1] = 6
    if contest[1] == 'FLA': contest[1] = 7
    if contest[1] == 'PHI': contest[1] = 8
    if contest[1] == 'HOU': contest[1] = 9
    if contest[1] == 'BOS': contest[1] = 10
    if contest[1] == 'NYE': contest[1] = 11
    competitions_without_draw[i] = tuple(contest)

# Do algorithm and get results
params = choix.ilsr_pairwise(n_items, competitions_without_draw)
#print(params)
leaderboard_BT = list(np.argsort(-params))
for i in range(len(leaderboard_BT)):
    if leaderboard_BT[i] == 0: leaderboard_BT[i] = 'SFS'
    if leaderboard_BT[i] == 1: leaderboard_BT[i] = 'VAL'
    if leaderboard_BT[i] == 2: leaderboard_BT[i] = 'SHD'
    if leaderboard_BT[i] == 3: leaderboard_BT[i] = 'GLA'
    if leaderboard_BT[i] == 4: leaderboard_BT[i] = 'DAL'
    if leaderboard_BT[i] == 5: leaderboard_BT[i] = 'SEO'
    if leaderboard_BT[i] == 6: leaderboard_BT[i] = 'LDN'
    if leaderboard_BT[i] == 7: leaderboard_BT[i] = 'FLA'
    if leaderboard_BT[i] == 8: leaderboard_BT[i] = 'PHI'
    if leaderboard_BT[i] == 9: leaderboard_BT[i] = 'HOU'
    if leaderboard_BT[i] == 10: leaderboard_BT[i] = 'BOS'
    if leaderboard_BT[i] == 11: leaderboard_BT[i] = 'NYE'
print("Ranking of BTmodel (best to worst):", leaderboard_BT)


# Bayes Approach base on Trueskill
from trueskill import rate_1vs1, global_env, TrueSkill
names = locals()

env = TrueSkill()
t0 = env.create_rating()
t1 = env.create_rating()
t2 = env.create_rating()
t3 = env.create_rating()
t4 = env.create_rating()
t5 = env.create_rating()
t6 = env.create_rating()
t7 = env.create_rating()
t8 = env.create_rating()
t9 = env.create_rating()
t10 = env.create_rating()
t11 = env.create_rating()

# Transfrom the data
for i in range(len(competitions_draw)):
    contest = list(competitions_draw[i])
    if contest[0] == 'SFS': contest[0] = 0
    if contest[0] == 'VAL': contest[0] = 1
    if contest[0] == 'SHD': contest[0] = 2
    if contest[0] == 'GLA': contest[0] = 3
    if contest[0] == 'DAL': contest[0] = 4
    if contest[0] == 'SEO': contest[0] = 5
    if contest[0] == 'LDN': contest[0] = 6
    if contest[0] == 'FLA': contest[0] = 7
    if contest[0] == 'PHI': contest[0] = 8
    if contest[0] == 'HOU': contest[0] = 9
    if contest[0] == 'BOS': contest[0] = 10
    if contest[0] == 'NYE': contest[0] = 11
    if contest[1] == 'SFS': contest[1] = 0
    if contest[1] == 'VAL': contest[1] = 1
    if contest[1] == 'SHD': contest[1] = 2
    if contest[1] == 'GLA': contest[1] = 3
    if contest[1] == 'DAL': contest[1] = 4
    if contest[1] == 'SEO': contest[1] = 5
    if contest[1] == 'LDN': contest[1] = 6
    if contest[1] == 'FLA': contest[1] = 7
    if contest[1] == 'PHI': contest[1] = 8
    if contest[1] == 'HOU': contest[1] = 9
    if contest[1] == 'BOS': contest[1] = 10
    if contest[1] == 'NYE': contest[1] = 11
    competitions_draw[i] = tuple(contest)

# Calculate win probability
import math
def win_prob(team_one, team_two):
    deltamu = team_one.mu - team_two.mu
    rsss = math.sqrt(team_one.sigma**2 + team_two.sigma**2)
    ts = global_env()
    return ts.cdf(deltamu/rsss)

# Run algorithm
for contest in competitions_without_draw:
    winner = contest[0]
    loser = contest[1]
    names['t%s' % winner],names['t%s' % loser] = rate_1vs1(names['t%s' % winner],names['t%s' % loser])
for contest in competitions_draw:
    team1 = contest[0]
    team2 = contest[1]
    names['t%s' % team1],names['t%s' % team2] = rate_1vs1(names['t%s' % team1],names['t%s' % team2], drawn=True)

# Rank the teams
teams_rate = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11]
leaderboard_TK = sorted(teams_rate, key=env.expose, reverse=True)
name_of_leaderboard_TK = []
for i in range(len(leaderboard_TK)):
    for j in range(len(teams_rate)):
        if leaderboard_TK[i] == teams_rate[j]: name_of_leaderboard_TK.append(j)
for i in range(len(name_of_leaderboard_TK)):
    if name_of_leaderboard_TK[i] == 0: name_of_leaderboard_TK[i] = 'SFS'
    if name_of_leaderboard_TK[i] == 1: name_of_leaderboard_TK[i] = 'VAL'
    if name_of_leaderboard_TK[i] == 2: name_of_leaderboard_TK[i] = 'SHD'
    if name_of_leaderboard_TK[i] == 3: name_of_leaderboard_TK[i] = 'GLA'
    if name_of_leaderboard_TK[i] == 4: name_of_leaderboard_TK[i] = 'DAL'
    if name_of_leaderboard_TK[i] == 5: name_of_leaderboard_TK[i] = 'SEO'
    if name_of_leaderboard_TK[i] == 6: name_of_leaderboard_TK[i] = 'LDN'
    if name_of_leaderboard_TK[i] == 7: name_of_leaderboard_TK[i] = 'FLA'
    if name_of_leaderboard_TK[i] == 8: name_of_leaderboard_TK[i] = 'PHI'
    if name_of_leaderboard_TK[i] == 9: name_of_leaderboard_TK[i] = 'HOU'
    if name_of_leaderboard_TK[i] == 10: name_of_leaderboard_TK[i] = 'BOS'
    if name_of_leaderboard_TK[i] == 11: name_of_leaderboard_TK[i] = 'NYE'
print("Ranking of Trueskill (best to worst):", name_of_leaderboard_TK)