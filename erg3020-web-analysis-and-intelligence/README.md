# Inroduction
The Overwatch League is a professional eSports league for the video game Overwatch, developed
and fully controlled by Blizzard Entertainment. The Overwatch League aims to follow the model
of traditional North American professional sports, using a set of permanent teams and regular
season play.

## Team Information

The League divide the teams into two divisions:

**Pacific Division**: Dallas Fuel, Los Angeles Gladiators, Los Angeles Valiant, San Francisco Shock, Seoul Dynasty, Shanghai Dragons.

**Atlantic Division**: Boston Uprising, Florida Mayhem, Houston Outlaws, London Spitfire, New York Excelsior, Philadelphia Fusion.

## Competition Rule
OWL has 4 stages, preseason, regular season, playoffs, and all-star. And there’re 12 teams divided into 2 divisions.

## Rating System
Every competition would have 4 to 5 sub-competitions. For Massey
rating method, I consider score differential of each competition. For Bradley-Terry model
and Bayesian ranking method, we consider the results of the sub-competitions. For example,
if Dallas Fuel wins 3:2, 4:0, 3:1, 4:0 respectively in 4 sub-competitions against Florida
Mayhem, we would only count four times 1:0 with Dallas Fuel scored 1 and Florida Mayhem
scored 0.

## Goal
The project would mainly focus on the scores of the pre-season
and the ongoing regular season, and predict the ranking at the end of this season, and judge
which teams in each division would have the right to compete in the Playoff season.

# Dataset
I collected the score data by reference to https://github.com/ThomasLee969/owl-sr.

# Instruction
Run BTmodel-and-Trueskill.py in IDLE.
