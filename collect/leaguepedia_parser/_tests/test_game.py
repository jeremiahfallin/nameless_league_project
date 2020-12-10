import pytest

import leaguepedia_parser

regions_names = ["China", "Europe", "Korea"]
tournaments_names = ["LEC/2020 Season/Spring Season", "LCK/2020 Season/Spring Season", "LPL/2020 Season/Spring Season"]


def test_regions():
    regions = leaguepedia_parser.get_regions()

    assert all(region in regions for region in regions_names)


@pytest.mark.parametrize("region", regions_names)
def test_tournaments(region):
    tournaments = leaguepedia_parser.get_tournaments(region, year=2020)

    for tournament in tournaments:
        print(tournament["overviewPage"])

    assert len(tournaments) > 0


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_games(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)

    assert len(games) > 0


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_get_details(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)

    # First, test without pageId
    leaguepedia_parser.get_game_details(games[0])

    # Then test with pageId
    game = leaguepedia_parser.get_game_details(games[0], True)

    assert "picksBans" in game

    for team in "BLUE", "RED":
        assert len(game["teams"][team]["players"]) == 5
        for player in game["teams"][team]["players"]:
            assert "irlName" in player["uniqueIdentifiers"]["leaguepedia"]
            assert "birthday" in player["uniqueIdentifiers"]["leaguepedia"]
            assert "pageId" in player["uniqueIdentifiers"]["leaguepedia"]
