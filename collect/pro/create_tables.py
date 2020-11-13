import psycopg2

def create_tables(conn):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE game (
            id SERIAL PRIMARY KEY,
            platform TEXT NOT NULL,
            game_id INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            start TEXT NOT NULL,
            tournament TEXT NOT NULL,
            game_in_series INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE game_player_snapshot (
                id SERIAL PRIMARY KEY,
                current_gold INTEGER NOT NULL,
                total_gold INTEGER NOT NULL,
                total_gold_diff INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                xp_diff INTEGER NOT NULL,
                level INTEGER NOT NULL,
                cs INTEGER NOT NULL,
                cs_diff INTEGER NOT NULL,
                monsters_killed INTEGER NOT NULL,
                monsters_killed_diff INTEGER NOT NULL,
                timestamp BIGINT NOT NULL,
                game_id SERIAL REFERENCES game (id),
                player_id SERIAL REFERENCES player (id),
                position SERIAL REFERENCES position (id)
                )
        """,
        """
        CREATE TABLE end_game_stats_player (
                id SERIAL PRIMARY KEY,
                first_blood BYTEA NOT NULL,
                first_blood_assist BOOLEAN NOT NULL,
                first_tower BOOLEAN NOT NULL,
                first_tower_assist BOOLEAN NOT NULL,
                first_inhibitor BOOLEAN NOT NULL,
                first_inhibitor_assist BOOLEAN NOT NULL,
                kills INTEGER NOT NULL,
                deaths INTEGER NOT NULL,
                assists INTEGER NOT NULL,
                gold INTEGER NOT NULL,
                cs INTEGER NOT NULL,
                level INTEGER NOT NULL,
                wards_placed INTEGER NOT NULL,
                wards_killed INTEGER NOT NULL,
                vision_wards_bought INTEGER NOT NULL,
                killing_spree INTEGER NOT NULL,
                largest_killing_spree INTEGER NOT NULL,
                double_kills INTEGER NOT NULL,
                triple_kills INTEGER NOT NULL,
                quadra_kills INTEGER NOT NULL,
                tower_kills INTEGER NOT NULL,
                inhibitor_kills INTEGER NOT NULL,
                monster_kills INTEGER NOT NULL,
                monster_kills_in_allied_jungle INTEGER NOT NULL,
                monster_kills_in_enemy_jungle INTEGER NOT NULL,
                total_damage_dealt INTEGER NOT NULL,
                physical_damage_dealt INTEGER NOT NULL,
                magic_damage_dealt INTEGER NOT NULL,
                total_damage_dealt_to_champions INTEGER NOT NULL,
                physical_damage_dealt_to_champions INTEGER NOT NULL,
                magic_damage_dealt_to_champions INTEGER NOT NULL,
                total_damage_taken INTEGER NOT NULL,
                physical_damage_taken INTEGER NOT NULL,
                magic_damage_taken INTEGER NOT NULL,
                damage_dealt_to_objectives INTEGER NOT NULL,
                damage_dealt_to_turrets INTEGER NOT NULL,
                longest_time_spent_living INTEGER NOT NULL,
                largest_critical_strike INTEGER NOT NULL,
                gold_spent INTEGER NOT NULL,
                total_heal INTEGER NOT NULL,
                total_units_healed INTEGER NOT NULL,
                damage_self_mitigated INTEGER NOT NULL,
                total_time_cc_dealt INTEGER NOT NULL,
                time_ccing_others INTEGER NOT NULL,
                game_id REFERENCES game (id),
                player_id REFERENCES player (id)
        )
        """,
        """
        CREATE TABLE rune (
                id SERIAL PRIMARY KEY,
                riot_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                rune_tree TEXT NOT NULL,
                primary BOOLEAN NOT NULL,
                stats_1 INTEGER NOT NULL,
                stats_2 INTEGER NOT NULL,
                stats_3 INTEGER NOT NULL,   
                game_id REFERENCES game (id),
                player_id REFERENCES player (id)  
        )
        """,
        """
        CREATE TABLE game_player_rune (
                id SERIAL PRIMARY KEY,
                primary_tree TEXT NOT NULL,
                secondary_tree TEXT NOT NULL,
                base_stats_1 TEXT NOT NULL,
                base_stats_2 TEXT NOT NULL,
                base_stats_3 TEXT NOT NULL,
                game_id REFERENCES game (id),
                player_id REFERENCES player (id),
                primary_1 REFERENCES rune (id),
                primary_2 REFERENCES rune (id),
                primary_3 REFERENCES rune (id),
                secondary_1 REFERENCES rune (id),
                secondary_2 REFERENCES rune (id),
        )
        """,
        """
        CREATE TABLE player (
                id SERIAL PRIMARY KEY,
                team_id REFERENCES team (id),
                summoner_spells REFERENCES summoner_spell_player (id),
                runes REFERENCES rune (id),
                item_events REFERENCES player_item_event (id),
                ward_events REFERENCES player_ward_events (id),
                skill_level_events REFERENCES player_skill_level_events (id)
        )
        """,
        """
        CREATE TABLE player_item (
                id SERIAL PRIMARY KEY,
                slot INTEGER NOT NULL,
                riot_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                game_id REFERENCES game (id),
                player_id REFERENCES player (id),
        )
        """,
        """
        CREATE TABLE summoner_spell_player (
            id SERIAL PRIMARY KEY,
            summoner_spell_1_id INTEGER NOT NULL,
            summoner_spell_1_name TEXT NOT NULL,
            summoner_spell_2_id INTEGER NOT NULL,
            summoner_spell_2_name TEXT NOT NULL
            )
        """,
        """
        CREATE TABLE player_level_up_event (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            slot TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            position REFERENCES position (id),
            game_id REFERENCES game (id),
            player_id REFERENCES player (id),
            )
        """,
        """
        CREATE TABLE player_item_event (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            riot_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            undo_id BOOLEAN,
            timestamp BIGINT NOT NULL,
            position REFERENCES position (id),
            game_id REFERENCES game (id),
            player_id REFERENCES player (id),
            )
        """,
        """
        CREATE TABLE player_ward_event (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            ward_type TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            position REFERENCES position (id),
            game_id REFERENCES game (id),
            player_id REFERENCES player (id),
            )
        """,
        """
        CREATE TABLE team (
            id SERIAL PRIMARY KEY,
            side TEXT NOT NULL,
            name TEXT
            )
        """,
        """
        CREATE TABLE team_building_kill (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            lane TEXT NOT NULL,
            side TEXT NOT NULL,
            tower_location TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            position REFERENCES position (id),
            game_id REFERENCES game (id),
            killer_id REFERENCES player (id),
            team_id REFERENCES team (id)
            )
        """,
        """
        CREATE TABLE end_game_stats_team (
            id SERIAL PRIMARY KEY,
            tower_kills INTEGER NOT NULL,
            inhibitor_kills INTEGER NOT NULL,
            first_tower BOOLEAN NOT NULL,
            first_inhibitor BOOLEAN NOT NULL,
            rift_herald_kills INTEGER NOT NULL,
            dragon_kills INTEGER NOT NULL,
            baron_kills INTEGER NOT NULL,
            first_rift_herald BOOLEAN NOT NULL,
            first_dragon BOOLEAN NOT NULL,
            first_baron BOOLEAN NOT NULL,
            game_id REFERENCES game (id),
            team_id REFERENCES team (id),
            )
        """,
        """
        CREATE TABLE kill (
            id SERIAL PRIMARY KEY,
            timestamp BIGINT NOT NULL,
            game_id REFERENCES game (id),
            killer_id REFERENCES player (id),
            assist_id_1 REFERENCES player (id),
            assist_id_2 REFERENCES player (id),
            assist_id_3 REFERENCES player (id),
            assist_id_4 REFERENCES player (id),
            victim_id REFERENCES player (id),
            position REFERENCES position (id)
            )
        """,
        """
        CREATE TABLE source (
            id SERIAL PRIMARY KEY,
            source_name TEXT NOT NULL,
            platform_id TEXT NOT NULL,
            game_version TEXT NOT NULL,
            patch INTEGER NOT NULL
            )
        """,
        """
        CREATE TABLE position (
            id SERIAL PRIMARY KEY,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL
            )
        """,
        """
        CREATE TABLE pick_ban (
            id SERIAL PRIMARY KEY,
            ban_1 TEXT NOT NULL,
            ban_2 TEXT NOT NULL,
            ban_3 TEXT NOT NULL,
            ban_4 TEXT NOT NULL,
            ban_5 TEXT NOT NULL,
            ban_6 TEXT NOT NULL,
            b1 TEXT NOT NULL,
            r1 TEXT NOT NULL,
            r2 TEXT NOT NULL,
            b2 TEXT NOT NULL,
            b3 TEXT NOT NULL,
            r3 TEXT NOT NULL,
            ban_7 TEXT NOT NULL,
            ban_8 TEXT NOT NULL,
            ban_9 TEXT NOT NULL,
            ban_10 TEXT NOT NULL,
            r4 TEXT NOT NULL,
            b4 TEXT NOT NULL,
            b5 TEXT NOT NULL,
            r5 TEXT NOT NULL,
            game_id REFERENCES game (id),
            )
        """,
        """
        CREATE TABLE team_monster_kill (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL,
            sub_type TEXT NOT NULL,
            timestamp BIGINT NOT NULL,
            game_id REFERENCES game (id),
            team_id REFERENCES team (id),
            killer_id REFERENCES player (id),
            position REFERENCES position (id)
            )
        """,
        )
    try:
        # connect to the PostgreSQL server
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
