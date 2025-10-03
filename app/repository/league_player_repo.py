from datetime import datetime
from app.db import DBConnection

class LeaguePlayerRepository:
    
    def insert_challenges_data(self, puuid, data):
        challenge_level = data["totalPoints"]["level"]
        current = data["totalPoints"]["current"]
        challenge_max = data["totalPoints"]["max"]
        percentile = data["totalPoints"]["percentile"]
        with DBConnection() as db:
            cursor = db.execute_sql(
                "insert/challenges_total_points_data.sql",
                (puuid,challenge_level,current,challenge_max,percentile,)
            )
        for category, info in data["categoryPoints"].items():
            challenge_level = info["level"]
            current = info["current"]
            challenge_max = info["max"]
            percentile = info["percentile"]
            with DBConnection() as db:
                cursor = db.execute_sql(
                    "insert/challenge_category_points_data.sql",
                    (puuid, category, challenge_level, current, challenge_max, percentile)
                )
        #! for every challenge
        for challenge in data["challenges"]:
            challenge_id = challenge["challengeId"]
            percentile = challenge["percentile"]
            challenge_tier = challenge["level"]
            challenge_value = challenge["value"]
            achieved_time = challenge.get("achievedTime", None)
            if achieved_time:
                achieved_time = datetime.fromtimestamp(achieved_time / 1000)
            position = challenge.get("position", 0)
            player_in_level = challenge.get("playersInLevel", 0)
            with DBConnection() as db:
                cursor = db.execute_sql(
                    "insert/challenges_data.sql",
                    (puuid, challenge_id, percentile, challenge_tier, challenge_value, achieved_time, position, player_in_level,)
                )
        return True

    def fetch_rank_with_puuid(self, puuid):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "fetch/ranked_data_with_puuid.sql",
                (puuid,)
            )
            return cursor.fetchall()

    def insert_ranked_data(self, entries):
        for rank in entries:
            puuid = rank["puuid"]
            league_id = rank["leagueId"]
            queue_type = rank["queueType"]
            tier = rank["tier"]
            division = rank["rank"]
            league_points = int(rank["leaguePoints"])
            wins = int(rank["wins"])
            losses = int(rank["losses"])
            veteran = rank["veteran"]
            inactive = rank["inactive"]
            fresh_blood = rank["freshBlood"]
            hot_streak = rank["hotStreak"]
            with DBConnection() as db:
                cursor = db.execute_sql(
                    "insert/ranked_data.sql",
                    (puuid, league_id, queue_type, tier, division, league_points,
                     wins, losses, veteran, inactive, fresh_blood, hot_streak,)
                )
        return True

    def fetch_champ_mastery_with_puuid(self, puuid):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "fetch/champ_mastery_with_puuid.sql",
                (puuid,)
            )
            return cursor.fetchall()

    def insert_champ_mastery_data(self, entries):
        for champ in entries:
            puuid = champ["puuid"]
            champion_id = champ["championId"]
            champion_level = champ["championLevel"]
            champion_points = champ["championPoints"]
            last_play_time = datetime.fromtimestamp(champ["lastPlayTime"] / 1000) 
            with DBConnection() as db:
                cursor = db.execute_sql(
                    "insert/champ_mastery_data.sql",
                    (puuid, champion_id, champion_level, champion_points, last_play_time,)
                )
        return True
        
    def fetch_account_with_name_tag(self, name, tag):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "fetch/account_with_name_tag.sql",
                (name, tag,)
            )
            return cursor.fetchone()
        
    def insert_account_data(self, data):
        puuid = data["puuid"]
        game_name = data["gameName"]
        tag_line = data["tagLine"]
        with DBConnection() as db:
            cursor = db.execute_sql(
                "insert/account_data.sql",
                (puuid, game_name, tag_line,)
            )
        return True
    
    def insert_summoner_data(self, data, server):
        puuid = data["puuid"]
        profile_icon_id = data["profileIconId"]
        revision_date = datetime.fromtimestamp(data["revisionDate"] / 1000)  
        summoner_level = data["summonerLevel"]
        riot_server = server
        with DBConnection() as db:
            cursor = db.execute_sql(
                "insert/summoner_data.sql",
                (puuid, profile_icon_id, revision_date, summoner_level, riot_server,)
            )
        return True
    
    def fetch_summoner_with_puuid_server(self, puuid, server):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "fetch/summoner_with_puuid_server.sql",
                (puuid, server)
            )
            return cursor.fetchone()