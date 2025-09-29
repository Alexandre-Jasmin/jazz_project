from config import DevelopmentConfig
from app.utilities import LeagueUtilities, BasicUtilities

class LeaguePlayer:

    def __init__(self, account_summoner_data, champion_mastery_data, ranked_data, challenges_data):

        # setup static data
        self.league_utils = LeagueUtilities()
        self.basic_utils = BasicUtilities()
        self.current_patch = self.league_utils.current_patch
        self.current_champion_json = self.league_utils.current_champion_json
        
        # setup received data
        self.account_summoner_data = account_summoner_data
        self.champion_mastery_data = champion_mastery_data
        self.ranked_data = ranked_data
        self.challenges_data = challenges_data
        
        # FORMAT DATA
        # name + zz id + server
        self.jazz_id = self.account_summoner_data["puuid"][:5]
        self.name = f'{self.account_summoner_data["game_name"]}#{self.account_summoner_data["tag_line"]}'
        self.server = self.account_summoner_data["riot_server"]

        #last_update
        self.update_time_ago = self.basic_utils.time_ago(self.account_summoner_data["last_updated"])

        # ranked information
        if not self.ranked_data:
            self.player_is_ranked = False
        else:
            self.player_is_ranked = True
        for entry in self.ranked_data:
            entry["queue_name"] = self._map_queue(entry["queue_type"])
            w, l = entry["wins"], entry["losses"]
            if w+l == 0:
                entry["win_rate"] = "NaN"
            else:
                entry["win_rate"] = round(((w/(w+l))*100), 1)

        # champion mastery
        if not self.champion_mastery_data:
            self.player_has_champion_mastery = False
        else:
            self.player_has_champion_mastery = True
        for entry in self.champion_mastery_data:
            champion_id = entry["champion_id"]
            champion_name = self._map_champion_key(champion_id)
            entry["champion_name"] = champion_name

    def _map_champion_key(self, champion_id: int) -> str:
        return self.league_utils.champion_id_to_name_dict.get(champion_id, "Unknown")
    
    def _map_queue(self, queue_type: str) -> str:
        return self.league_utils.queue_mapping.get(queue_type, "Unknown")