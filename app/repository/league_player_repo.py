from datetime import datetime
from app.db import DBConnection

class LeaguePlayerRepository:

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