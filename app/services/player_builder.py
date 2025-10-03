from datetime import datetime, timedelta

from app.services import RiotService
from app.models import LeaguePlayer
from app.repository.league_player_repo import LeaguePlayerRepository

class PlayerBuilder:
    def __init__(self, riot: RiotService, repo: LeaguePlayerRepository):
        self.riot_api = riot
        self.repo = repo

    def get_player(self, name: str, tag: str, server: str) -> LeaguePlayer:

        account_data = self.repo.fetch_account_with_name_tag(name, tag)

        if not account_data:
            # brand new/name_change -                               invalid account
            account_data = self._refresh_player(name, tag, server)

        summoner_data = self.repo.fetch_summoner_with_puuid_server(account_data["puuid"], server)
        mastery_data = self.repo.fetch_champ_mastery_with_puuid(account_data["puuid"])
        ranked_data = self.repo.fetch_rank_with_puuid(account_data["puuid"])
        challenges_data = self.repo.fetch_challenges_with_puuid(account_data["puuid"]) #! need to fetch from all 3 tables
        #latest_match_data = self.repo.fetch_matches_with_puuid(account_data["puuid"], 20)

        return account_data, challenges_data

        return LeaguePlayer(
            account_data,
            summoner_data,
            mastery_data,
            ranked_data,
            latest_match_data
        )

    def _refresh_player(self, name: str, tag: str, server: str) -> dict:

        def load_matchlist_data(list_of_match_ids):
            all_match_data = []
            for match_id in list_of_match_ids:
                match_data = self.riot_api.get_match(match_id)
                match_timeline = self.riot_api.get_match_timeline(match_id)
                all_match_data.append(match_data, match_timeline)
            return all_match_data

        self.riot_api.set_region(server)

        api_account_data = self.riot_api.get_account(summoner_name=name, tag=tag)
        if not api_account_data:
            raise ValueError("Account not found")
        self.repo.insert_account_data(api_account_data)

        api_summoner_data = self.riot_api.get_summoner(api_account_data["puuid"])
        if not api_summoner_data:
            raise ValueError("Summoner not found")
        self.repo.insert_summoner_data(api_summoner_data, server)

        self.repo.insert_champ_mastery_data(self.riot_api.get_champion_mastery(api_account_data["puuid"]))
        self.repo.insert_ranked_data(self.riot_api.get_league_entries_by_puuid(api_account_data["puuid"]))
        self.repo.insert_challenges_data(api_account_data["puuid"], self.riot_api.get_challenges(api_account_data["puuid"]))
        #self.repo.insert_match_from_matchlist(load_matchlist_data(self.riot_api.get_matches_by_puuid(puuid=api_account_data["puuid"], count=20)))

        #! while loop to catch a flask return on self.repo

        return self.repo.fetch_account_with_name_tag(api_account_data["gameName"], api_account_data["tagLine"])
        