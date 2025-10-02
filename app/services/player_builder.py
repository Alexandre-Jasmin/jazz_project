from datetime import datetime, timedelta

from app.services import RiotService
from app.models import LeaguePlayer
from app.repository.league_player_repo import LeaguePlayerRepository

class PlayerBuilder:
    def __init__(self, riot: RiotService, repo: LeaguePlayerRepository):
        self.riot_api = riot
        self.repo = repo

    def get_player(self, name: str, tag: str, server: str) -> LeaguePlayer:
        self.riot_api.set_region(server)

        data = self.repo.fetch_account_summoner_data_name(name, tag, server)

        if not data:
            #brand new, refresh
            data = self._refresh_player(name, tag, server)
        elif self._is_stale(data["last_updated"]):
            pass

        champion_mastery = self.repo.fetch_champion_mastery_puuid(data["puuid"])
        ranked = self.repo.fetch_ranked_data_puuid(data["puuid"])
        challenges = self.repo.fetch_challenges_data_puuid(data["puuid"])
        #recent matches (20) (stats) + show more
        #live game
        #recently played with

        return LeaguePlayer(data, champion_mastery, ranked, challenges)
    
    def _is_stale(self, last_updated: datetime) -> bool:
        return last_updated < datetime.now() - timedelta(hours=24)
    
    def _refresh_player(self, name: str, tag: str, server: str) -> dict:
        
        self.riot_api.set_region(server)
        api_account = self.riot_api.get_account(summoner_name=name, tag=tag)
        if not api_account:
            raise ValueError("Account not found")
        
        api_summoner = self.riot_api.get_summoner(api_account["puuid"])
        if not api_summoner:
            raise ValueError("Summoner not found")
        
        self.repo.insert_account_summoner_data(
            api_account["puuid"],
            api_account["gameName"],
            api_account["tagLine"],
            api_summoner["summonerLevel"],
            api_summoner["profileIconId"],
            server
        )

        self.repo.insert_champions_mastery_data(
            api_account["puuid"],
            self.riot_api.get_champion_mastery(api_account["puuid"])
        )

        self.repo.insert_ranked_data_puuid(
            api_account["puuid"],
            self.riot_api.get_league_entries_by_puuid(api_account["puuid"])
        )

        self.repo.insert_challenges_data_puuid(
            api_account["puuid"],
            self.riot_api.get_challenges(api_account["puuid"])
        )

        #recent matches (20) (stats) + show more
        #live game
        #recently played with

        return self.repo.fetch_account_summoner_data_name(api_account["gameName"], api_account["tagLine"], server)