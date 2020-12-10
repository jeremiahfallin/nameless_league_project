import sys
sys.path.append('..')
import leaguepedia_parser
import lol_id_tools as lit
import json

with open('../runes_reforged.json') as f:
  runes_reforged = json.load(f)

def get_regions():
    return leaguepedia_parser.get_regions()

def get_tournaments(region, year):
    # Gets tournaments in the region, by default only returns primary tournaments
    return leaguepedia_parser.get_tournaments(region, year=year)

def get_tournament_games(tournament):
    # Gets all games for a tournament. Get the name from get_tournaments()
    return leaguepedia_parser.get_games(tournament)

def get_tournament_game_details(game):
    # Gets picks and bans and other details from a game. Get the game object from get_games()
    return leaguepedia_parser.get_game_details(game)

# grab regions
# loop through regions
#   grab tournaments in each region for year decrementing
# loop through tournament games
# store game details in database

def sqlize_game(game):
    table = {}
    if "sources" in game and "riotLolApi" in game['sources']:
        table['platform'] = game['sources']['riotLolApi']['platformId'] 
        table['game_id'] = game['sources']['riotLolApi']['gameId']
        table['game_hash'] = game['sources']['riotLolApi']['gameHash']
    table['duration'] = game['duration']
    table['start'] = game['start']
    table['tournament'] = game['tournament']
    table['game_in_series'] = game['gameInSeries']

    return table

def sqlize_end_game_stats_player(game):
    teams = ["BLUE", "RED"]
    stats_needed = ['kills', 'assists', 'deaths', 'cs', 'gold']
    table = {}
    for team in teams:
        table[team] = {}
        for i, player in enumerate(game['teams'][team]["players"]):
            lp_player = player['uniqueIdentifiers']['leaguepedia']
            table[team][i] = {}
            for stat in stats_needed:
                table[team][i][stat] = lp_player[stat]

    return table

def sqlize_runes(game):
    teams = ["BLUE", "RED"]
    table = {}
    for team in teams:
        table[team] = {}
        for i, player in enumerate(game['teams'][team]["players"]):
            lp_player = player['uniqueIdentifiers']['leaguepedia']
            runes = lp_player['runes'].split(',')

            table[team][i] = {}
            for j, player_rune in enumerate(runes):
                for r in runes_reforged:
                    for row in r['slots']:
                        for rune in row['runes']:
                            if j >= 6:
                                table[team][i][f'base_stats_{j - 5}'] = player_rune
                            if player_rune == rune['name']:
                                if j == 0:
                                    table[team][i]["primary_tree"] = r['name']
                                    table[team][i]["primary_keystone"] = {"riot_id": rune['id'], "name": rune['name'], "primary": True}
                                    primary = r['name']
                                elif j <= 1 and j <= 3:
                                    table[team][i][f'primary_{j}'] = {"riot_id": rune['id'], "name": rune['name'], "primary": primary == r['name']}
                                elif j == 4:
                                    table[team][i]["secondary_tree"] = r['name']
                                    table[team][i]["secondary_1"] = {"riot_id": rune['id'], "name": rune['name'], "primary": primary == r['name']}
                                elif j == 5:
                                    table[team][i]["secondary_2"] = {"riot_id": rune['id'], "name": rune['name'], "primary": primary == r['name']}
    return table

def sqlize_items(game):
    teams = ["BLUE", "RED"]
    table = {}
    for team in teams:
        table[team] = {}
        for i, player in enumerate(game['teams'][team]["players"]):
            table[team][i] = {}
            lp_player = player['uniqueIdentifiers']['leaguepedia']
            table[team][i]["items"] = [item for item in lp_player['items'].split(',') if item != ""]
    return table

def sqlize_summoner_spells(game):
    teams = ["BLUE", "RED"]
    table = {}
    for team in teams:
        table[team] = {}
        for i, player in enumerate(game['teams'][team]["players"]):
            table[team][i] = {} 
            lp_player = player['uniqueIdentifiers']['leaguepedia']
            table[team][i]["ss"] = lp_player['ss'].split(',')
    return table

def sqlize_teams(game):
    teams = ["BLUE", "RED"]
    table = {} 
    for team in teams: 
        table[team] = {} 
        table[team]['name'] = game['teams'][team]["name"]
        table[team]['side'] = team
    return table

def sqlize_source(game):
    table = {}
    table["source_name"] = "leaguepedia"
    table["platform_id"] = game["sources"]["riotLolApi"]["platformId"]
    table['patch'] = game["patch"]
    return table

def sqlize_pick_ban(game):
    table = {}
    ban_num = 1
    picks = ['b1', 'r1', 'r2', 'b2', 'b3', 'r3', 'r4', 'b4', 'b5', 'r5']
    pick_num = 0
    for action in game["picksBans"]:
        if action["isBan"]:
            table[f"ban_{ban_num}"] = action["championName"]
            ban_num += 1
        else:
            table[picks[pick_num]] = action["championName"]
            print(pick_num)
            pick_num += 1
    return table
