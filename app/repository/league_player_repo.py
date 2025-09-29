import datetime

from app.db import DBConnection

class LeaguePlayerRepository:

    def fetch_account_summoner_data_name(self, name, tag, server):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "leaguedb/fetch_account_summoner_data_name.sql",
                (name, tag,)
            )
            return cursor.fetchone() # returns the first row in the search, since we expect one -> dict
        
    def insert_account_summoner_data(self, puuid, game_name, tag_line, summoner_level, profile_icon_id, riot_server):
        try:
            with DBConnection() as db:
                cursor = db.execute_sql(
                    "leaguedb/insert_account_summoner_data.sql",
                    (puuid,game_name,tag_line,summoner_level,profile_icon_id,riot_server)
                )
                return True
        except:
            return False
        
    def fetch_champion_mastery_puuid(self, puuid): 
        with DBConnection() as db:
            cursor = db.execute_sql(
                "leaguedb/fetch_champion_mastery_puuid.sql",
                (puuid,)
            )
            rows = cursor.fetchall()
        return rows

    def insert_champions_mastery_data(self, puuid, entries):
        with DBConnection() as db:
            for champion_entry in entries:
                last_play_time_sql = datetime.datetime.fromtimestamp(champion_entry['lastPlayTime']/1000)
                last_play_sql_format = last_play_time_sql.strftime('%Y-%m-%d %H:%M:%S')
                cursor = db.execute_sql(
                    "leaguedb/insert_champions_mastery_data.sql",
                    (puuid, champion_entry['championId'], champion_entry['championLevel'], champion_entry['championPoints'], last_play_sql_format,)
                )
            return True
        
    def fetch_ranked_data_puuid(self, puuid):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "leaguedb/fetch_ranked_data_puuid.sql",
                (puuid,)
            )
            rows = cursor.fetchall()
        return rows
        
    def insert_ranked_data_puuid(self, puuid, entries):
        with DBConnection() as db:
            for ranked_entry in entries:
                cursor = db.execute_sql(
                    "leaguedb/insert_ranked_data.sql",
                    (puuid, ranked_entry["queueType"], ranked_entry["tier"], ranked_entry["rank"], ranked_entry["leaguePoints"], ranked_entry["wins"], ranked_entry["losses"],
                     ranked_entry["veteran"], ranked_entry["inactive"], ranked_entry["freshBlood"], ranked_entry["hotStreak"],)
                )
        return True
    
    def fetch_challenges_data_puuid(self, puuid):
        with DBConnection() as db:
            cursor = db.execute_sql(
                "leaguedb/fetch_challenges_data_puuid.sql",
                (puuid,)
            )
            rows = cursor.fetchall()
        return rows
    
    def insert_challenges_data_puuid(self, puuid, challenges_data):
        with DBConnection() as db:
            for c in challenges_data["challenges"]:
                puuid = puuid
                challenge_id = c["challengeId"]
                percentile = c["percentile"]
                challenge_tier = c["level"]
                challenge_value = c["value"]
                challenge_time = c.get("achievedTime")
                if challenge_time is not None:
                    achieved_time = datetime.datetime.fromtimestamp(challenge_time/1000)
                else:
                    achieved_time = None
                position = c.get("position")
                players_in_level = c.get("playersInLevel")
                cursor = db.execute_sql(
                    "leaguedb/insert_challenges_data.sql",
                    (puuid, challenge_id, percentile, challenge_tier, challenge_value,
                     achieved_time, position, players_in_level,)
                )
        return True