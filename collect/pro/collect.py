import leaguepedia_parser
from pprint import pprint

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
    table['duration'] = game['duration']
    table['start'] = game['start']
    table['tournament'] = game['tournament']
    table['game_in_series'] = game['gameInSeries']

    return table

def sqlize_end_game_stats_player(game):
    table = {}
    return True

def collect():
    printed = False
    regions = get_regions()
    for region in regions:
        tournaments = get_tournaments(region, 2020)
        for tournament in tournaments:
            games = get_tournament_games(tournament["overviewPage"])
            for game in games:
                game_details = get_tournament_game_details(game)
                game_table = sqlize_game(game)
                pprint(game)
                pprint(game_details)
                if game:
                    printed = True
                if printed:
                    break
            if printed:
                break
        if printed:
            break


collect()