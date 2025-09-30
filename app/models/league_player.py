from config import DevelopmentConfig
from app.utilities import LeagueUtilities, BasicUtilities
from flask import current_app

class LeaguePlayer:

    def __init__(self, account_summoner_data, champion_mastery_data, ranked_data, challenges_data):

        # setup static data
        self.basic_utils = BasicUtilities()
        self.current_patch = current_app.config["CURRENT_PATCH"]
        
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
            entry["queue_name"] = entry["queue_type"]#!
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
            entry["champion_name"] = self._get_champion_map(champion_id)["name"]
            entry["champion_icon_name"] = self._get_champion_map(champion_id)["id"]

        # challenges
        if not self.challenges_data:
            self.player_has_challenges = False
        else:
            self.player_has_challenges = True
        for challenge in self.challenges_data:
            challenge_id = int(challenge["challenge_id"])
            challenge["name"] = self._get_chall_map(challenge_id)["name"]
            challenge["percentile_percentage"] = round((challenge["percentile"]*100), 1)
            challenge["description"] = self._get_chall_map(challenge_id)["description"]
            challenge["max_value"] = 0
            challenge["image"] = f"league/ddragon/{self.current_patch}/img/challenges-images/{challenge_id}-{challenge['challenge_tier']}.png"

    def _get_champion_map(self, champion_id: int) -> dict:
        for champ in current_app.config["CHAMPION_DATA"]["data"].values():
            if int(champ["key"]) == champion_id:
                return {
                    "name": champ["name"],
                    "id": champ["id"]
                }
        return {
            "name": "Unknown",
            "id": "Unknown"
        }

    def _get_chall_map(self, challenge_id: int) -> dict:
        for challenge in current_app.config["CURRENT_CHALLENGES"]:
            if int(challenge["id"]) == challenge_id:
                #! calculate next threshold
                return {
                    "name": challenge["name"],
                    "description": challenge["description"],
                    "next_threshold": 0
                }
        return {
            "name": "Unknown",
            "description": "Unknown",
            "next_threshold": 0
        }
    