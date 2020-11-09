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