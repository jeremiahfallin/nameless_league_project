import psycopg2
from config import config

# game_player_rune
# rune
# player
# player_item
# summoner_spell_player
# player_level_up_event
# player_item_event
# player_ward_event
# team
# team_building_kill
# end_game_stats_team
# kill
# source
# position
# pick_ban
# team_monster_kill

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE game (
            id SERIAL PRIMARY KEY,
            platform VARCHAR(255) NOT NULL,
            kills,
            team_id_blue,
            team_id_red,
            game_id,
            duration,
            start,
            tournament,game_in_series
        )
        """,
        """ CREATE TABLE game_player_snapshot (
                id SERIAL PRIMARY KEY,
                game_id VARCHAR(255) NOT NULL,
                player_id,
                current_gold,
                total_gold,
                total_gold_diff,
                xp,
                xp_diff,
                level,
                cs,
                cs_diff,
                monsters_killed,
                monsters_killed,diff,
                position,
                timestamp
                )
        """,
        """
        CREATE TABLE end_game_stats_player (
                id INTEGER PRIMARY KEY,
                player_id VARCHAR(5) NOT NULL,
                first_blood BYTEA NOT NULL,
                first_blood_assist,
                first_tower,
                first_tower_assist,
                first_inhibitor,
                first_inhibitor_assist,
                kills,
                deaths,
                assists,
                gold,
                cs,
                level,
                wards_placed,
                wards_killed,
                vision_wards_bought,
                killing_spree,
                largest_killing_spree,
                double_kills,
                triple_kills,
                quadra_kills,
                tower_kills,
                inhibitor_kills,
                monster_kills,
                monster_kills_in_allied_jungle,
                monster_kills_in_enemy_jungle,
                total_damage_dealt,
                physical_damage_dealt,
                magic_damage_dealt,
                total_damage_dealt_to_champions,
                physical_damage_dealt_to_champions,
                magic_damage_dealt_to_champions,
                total_damage_taken,
                physical_damage_taken,
                magic_damage_taken,
                damage_dealt_to_objectives,
                damage_dealt_to_turrets,
                longest_time_spent_living,
                largest_critical_strike,
                gold_spent,
                total_heal,
                total_units_healed,
                damage_self_mitigated,
                total_time_cc_dealt,
                time_ccing_others
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
        )
        """,
        """
        CREATE TABLE rune (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()