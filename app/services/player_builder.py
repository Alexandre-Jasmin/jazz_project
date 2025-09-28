from datetime import datetime, timedelta

from config import DevelopmentConfig
from app.services import RiotService
from app.models import LeaguePlayer
from app.repository.league_player_repo import LeaguePlayerRepository

class PlayerBuilder:

    def __init__(self, riot: RiotService):
        self.riot = riot
        self.sql_folder = DevelopmentConfig.BASE_SQL_DIR
        self.repo = LeaguePlayerRepository()

    def main_build(self, name: str, tag: str, server: str) -> LeaguePlayer:
        
        self.riot.set_region(server)

        # try and fetch data from database
        account_summoner_data = self.repo.fetch_account_summoner_data_name(name, tag, server)
        now = datetime.now()
        time_limit = now - timedelta(seconds=120)

        if not account_summoner_data or account_summoner_data["last_updated"] < time_limit:
            if not self.update_build(name, tag, server):
                return "Update failed"
            account_summoner_data = self.repo.fetch_account_summoner_data_name(name, tag, server)

        champion_mastery_data = self.repo.fetch_champion_mastery_puuid(account_summoner_data["puuid"])
        ranked_data = self.repo.fetch_ranked_data_puuid(account_summoner_data["puuid"])

        return LeaguePlayer(
            account_summoner_data,
            champion_mastery_data,
            ranked_data
        )

    def update_build(self, name, tag, server) -> bool:

        self.riot.set_region(server)

        api_account_data = self.riot.get_account(summoner_name=name, tag=tag)
        if "puuid" not in api_account_data:
            return False
        
        api_summoner_data = self.riot.get_summoner(puuid=api_account_data["puuid"])
        puuid = api_account_data["puuid"]
        game_name = api_account_data["gameName"]
        tag_line = api_account_data["tagLine"]
        summoner_level = api_summoner_data["summonerLevel"]
        profile_icon_id = api_summoner_data["profileIconId"]
        riot_server = server
        insert_status = self.repo.insert_account_summoner_data(puuid, game_name, tag_line, summoner_level, profile_icon_id, riot_server)
        if insert_status == False:
            return insert_status
        
        mastery_data = self.riot.get_champion_mastery(api_account_data["puuid"])
        insert_status = self.repo.insert_champions_mastery_data(api_account_data["puuid"], mastery_data)
        if insert_status == False:
            return insert_status
        
        api_ranked_data = self.riot.get_league_entries_by_puuid(api_account_data["puuid"])
        insert_status = self.repo.insert_ranked_data_puuid(api_account_data["puuid"], api_ranked_data)
        if insert_status == False:
            return insert_status
        
        return True