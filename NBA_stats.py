#nba_game_warriors_thunder_20181016.txt available here
#https://drive.google.com/file/d/1SD702mItBvT8tNWTy_F8DyGvI3jWP_Vj/view?usp=sharing

import csv
import re
import pandas as pd

def load_data(filename):
    #open and access csv file, separate each column by delimiter "|"
    result = []
    with open(filename, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="|")
        for row in csvreader:
            result.append(row)
    return result

def is_away_team(away_team, current_team):
    #check if current_team is the away team
    return away_team == current_team

def my_regex():
    #fetch data for each acronym that is not a formula
    #(.*) == #. = Match any character except newline #* = Match 0 or more repetitions of RE
    regex_data = []
    regex_data.append(re.compile(r"(.*) misses [2-3]-pt")) #field_goals_attempts (FGA)
    regex_data.append(re.compile(r"(.*) makes 3-pt")) #three_pt_field_goals (3P)
    regex_data.append(re.compile(r"(.*) misses 3-pt")) #three_pt_field_goals_attempts (3PA)
    regex_data.append(re.compile(r"(.*) makes free throw")) #free_throws (FT)
    regex_data.append(re.compile(r"(.*) misses free throw")) #free_throw_attemps (FTA)
    regex_data.append(re.compile(r"Offensive rebound by (.*)")) #offensive_rebounds (ORB)
    regex_data.append(re.compile(r"Defensive rebound by (.*)")) #defensive_rebounds (DRB)
    regex_data.append(re.compile(r"assist by ([A-Z]\. [A-Za-z]+)")) #assists (AST)
    regex_data.append(re.compile(r"steal by ([A-Z]\. [A-Za-z]+)")) #steals (STL)
    regex_data.append(re.compile(r"block by ([A-Z]\. [A-Za-z]+)")) #blocks (BLK)
    regex_data.append(re.compile(r"Turnover by ([A-Z]\. [A-Za-z]+)")) #turnovers (TOV)
    regex_data.append(re.compile(r"foul by ([A-Z]\. [A-Za-z]+)")) #personal_fouls (PF)
    regex_data.append(re.compile(r"(.*) makes 2-pt")) #2PT
    return regex_data

def searchIn(playDescription, regex_data):
    #count occurrencies of each acronym from regex data and find player name
    acronym_list = ["FGA", "3P", "3PA", "FT", "FTA", "ORB", "DRB", "AST", "STL", "BLK", "TOV", "PF", "2PT"]
    player_name = ""
    returnedData = ""
    for i in range(len(regex_data)):
        data = regex_data[i].search(playDescription)
        if (data and data.group(1)):
            player_name = data.group(1)
            returnedData = acronym_list[i]
    return returnedData, player_name

def analyse_nba_game(play_by_play_moves):
    #return hash of data for each player in each team, by team
    result = {"home_team": {"name": play_by_play_moves[0][4], "players_data": {}},"away_team": {"name": play_by_play_moves[0][3], "players_data": {}}}
    regex_data = my_regex()
    for play in play_by_play_moves:
        current_team = play[2]
        home_team = play[4]
        away_team = play[3]
        data = play[7]
        returnedData, player_name = searchIn(data, regex_data)
        if returnedData: 
            if is_away_team(away_team,current_team):
                if player_name not in result["away_team"]["players_data"]:
                    result["away_team"]["players_data"][player_name] = {"FGA": 0, "3P": 0, "3PA": 0, "FT": 0, "FTA": 0, "ORB": 0, "DRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "2PT": 0}
                else: 
                    result["away_team"]["players_data"][player_name][returnedData] += 1 
            else: 
                if player_name not in result["home_team"]["players_data"]:
                    result["home_team"]["players_data"][player_name] = {"FGA": 0, "3P": 0, "3PA": 0, "FT": 0, "FTA": 0, "ORB": 0, "DRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "2PT": 0}                     
                else: 
                    result["home_team"]["players_data"][player_name][returnedData] += 1
    return result

def print_nba_game_stats(team_dict):
    #take dictionary with player name and data and return formatted data
    df = pd.DataFrame.from_dict(team_dict["players_data"])
    #change order of results (T = Transposing the data frame) and add columns that are values that are result of formula:
    df = df.T.head()
    #FG = 3P + 2P
    df["FG"] = (df["3P"] + df["2PT"]).round(0)
    fieldgoals_column = df.pop("FG")
    df.insert(0, "FG", fieldgoals_column)
    #FG% = (FG / FGA)
    df["FG%"] = (df["FG"]/df["FGA"]).round(3)
    FGper_column = df.pop("FG%")
    df.insert(2, "FG%", FGper_column)
    #3P% = (3P / 3PA)
    df["3P%"] = (df["3P"]/df["3PA"]).round(3)
    three_per_column = df.pop("3P%")
    df.insert(5, "3P%", three_per_column)
    #FT% = (FT / FTA)
    df["FT%"] = (df["FT"]/df["FTA"]).round(3)
    freethrow_per_column = df.pop("FT%")
    df.insert(8, "FT%", freethrow_per_column)
    #TRB = (offensive_rebound + defensive_rebound)
    total_rebounds = ["ORB", "DRB"]
    df["TRB"] = df[total_rebounds].sum(axis=1)
    TRB_column = df.pop("TRB")
    df.insert(11, "TRB", TRB_column)
    #PTS = (Points 3P * 3 (3-pt goals times 3 points per goal)  + 2P * 2  + FT*1 (free throws timed 1 point per goal))
    df["PTS"] = ((df["3P"]*3) + (df["2PT"]*2) + df["FT"]).round(0)#.astype(int)
    point_column = df.pop("PTS")
    df.insert(17, "PTS", point_column)
    df = df.drop("2PT", axis=1)
    #replace NaN with 0
    df = df.fillna(0)
    print(df)

def _main():
    play_by_play_moves = load_data("nba_game_warriors_thunder_20181016.txt")
    team_dict = analyse_nba_game(play_by_play_moves)
    print_nba_game_stats(team_dict["home_team"])
    print_nba_game_stats(team_dict["away_team"])
    
_main()
