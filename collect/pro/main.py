import psycopg2
from time import sleep
from collect import *
from create_tables import create_tables

def insert_game(conn, data):
    cur = conn.cursor()
    insert = (data["platform"], data["game_id"], data["game_hash"], data["duration"], data["start"], data["tournament"], data["game_in_series"])
    query = "INSERT INTO game (platform, game_id, game_hash, duration, start, tournament, game_in_series) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, insert)
    print("Success")


def collect(conn):
    regions = get_regions()
    for region in regions:
        tournaments = get_tournaments(region, 2020)
        for tournament in tournaments:
            games = get_tournament_games(tournament["overviewPage"])
            for game in games:
                game_table = sqlize_game(game)
                insert_game(conn, game_table)
                game_details = get_tournament_game_details(game)
                game_player_stats = sqlize_end_game_stats_player(game)
                game_teams = sqlize_teams(game)
                game_source = sqlize_source(game)
                game_pick_ban = sqlize_pick_ban(game)
                if len(game['teams']['BLUE']['players'][0]['uniqueIdentifiers']['leaguepedia']['runes']) > 0:
                    game_player_runes = sqlize_runes(game)
                if len(game['teams']['BLUE']['players'][0]['uniqueIdentifiers']['leaguepedia']['items']) > 0:
                    game_player_items = sqlize_items(game)
                if len(game['teams']['BLUE']['players'][0]['uniqueIdentifiers']['leaguepedia']['ss']) > 0:
                    game_player_summoner_spells = sqlize_summoner_spells(game)

def get_postgres_conn():
    try:
        conn = psycopg2.connect(
            host="db",
            database="pro_league",
            user="admin",
            password="admin",
            connect_timeout=1)
        conn.close()
        return conn
    except:
        return True

if __name__ == '__main__':
    conn = ""
    while True:
        conn = get_postgres_conn()
    create_tables(conn)
    # collect(conn)
