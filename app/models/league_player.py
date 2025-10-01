from config import DevelopmentConfig
from app.utilities import LeagueUtilities, BasicUtilities
from flask import current_app

from app.services.league_static_data import LeagueStaticDataService

# PlayerProfile
# PlayerChampionMastery
# PlayerRank

class LeaguePlayerProfile:

    def __init__(self, account_summoner_data):
        self.data = account_summoner_data
        self.basic_utils = BasicUtilities()

        self.jazz_id = self.data["puuid"][:10]
        self.name = f'{self.data["game_name"]}#{self.data["tag_line"]}'
        self.game_name = self.data["game_name"]
        self.tag_line = self.data["tag_line"]
        self.level = self.data["summoner_level"]

        self.server = self.data["riot_server"]
        
        self.last_updated = self.data["last_updated"]
        self.last_update_time_ago = self.basic_utils.time_ago(self.data["last_updated"])

class LeaguePlayerRank:

    def __init__(self, ranked_data):
        self.data = ranked_data
        self.player_is_ranked = bool(self.data)

        if self.player_is_ranked:
            for rank in self.data:
                rank["queue_name"] = rank["queue_type"]
                w, l = rank["wins"], rank["losses"]
                if w + l == 0:
                    rank["win_rate"] = "NaN"
                else:
                    rank["win_rate"] = round((w / (w + l)) * 100, 1)

class LeaguePlayerChampionMastery:

    def __init__(self, champion_mastery_data):
        self.data = champion_mastery_data
        self.player_has_champion_mastery = bool(self.data)

        if self.player_has_champion_mastery:
            for entry in self.data:
                champion_id = entry["champion_id"]
                champion_dict = LeagueStaticDataService.get_champion(champion_id)
                entry["champion_name"] = champion_dict["name"]
                entry["champion_icon_name"] = champion_dict["id"]

class LeaguePlayerChallenges:
    
    def __init__(self, challenges_data):
        self.data = challenges_data
        self.current_patch = LeagueStaticDataService.get_patch()
        self.player_has_challenges = bool(self.data)

        if self.player_has_challenges:
            for challenge in self.data:
                challenge_id = int(challenge["challenge_id"])
                challenge_dict = LeagueStaticDataService.get_challenge(challenge_id)
                if not challenge_dict:
                    challenge["description"] = challenge_id
                    continue
                threshold_dict = self._find_thresholds(challenge["challenge_value"], challenge_dict)
                challenge["next_threshold"] = threshold_dict["next_threshold"]
                challenge["name"] = challenge_dict["name"]
                challenge["percentile_percentage"] = round((challenge["percentile"]*100), 1)
                challenge["description"] = challenge_dict["description"]
                challenge["max_value"] = 0
                challenge["image"] = f"league/ddragon/{self.current_patch}/img/challenges-images/{challenge_id}-{challenge['challenge_tier']}.png"

    def _find_thresholds(self, current_value: int, challenge_dict: dict) -> dict:

        thresholds = challenge_dict["thresholds"]
        levels = [(level, data["value"]) for level, data in thresholds.items()]
        levels.sort(key=lambda x: x[1])

        last_reached = 0
        next_threshold = 0
        furthest_threshold = levels[-1]  # highest one

        for level, value in levels:
            if value <= current_value:
                last_reached = value
            elif value > current_value and next_threshold is 0:
                next_threshold = value

        if next_threshold == 0:
            next_threshold = last_reached

        return {
            "last_reached": last_reached,
            "next_threshold": next_threshold,
            "furthest_threshold": furthest_threshold,
        }

class LeaguePlayer:

    def __init__(self, account_summoner_data, champion_mastery_data, ranked_data, challenges_data):

        # setup static data
        self.basic_utils = BasicUtilities()
        self.current_patch = LeagueStaticDataService.get_patch()
        
        # setup received data
        self.account_summoner_data = account_summoner_data
        self.champion_mastery_data = champion_mastery_data
        self.ranked_data = ranked_data
        self.challenges_data = challenges_data

        self.profile = LeaguePlayerProfile(account_summoner_data)
        self.champion_mastery = LeaguePlayerChampionMastery(champion_mastery_data)
        self.ranks = LeaguePlayerRank(ranked_data)
        self.challenges = LeaguePlayerChallenges(challenges_data)