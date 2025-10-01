from config import DevelopmentConfig
from app.utilities import LeagueUtilities, BasicUtilities
from flask import current_app

from app.services.league_static_data import LeagueStaticDataService

# PlayerProfile
# PlayerChampionMastery
# PlayerRank

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
            champion_dict = LeagueStaticDataService.get_champion(champion_id)
            entry["champion_name"] = champion_dict["name"]
            entry["champion_icon_name"] = champion_dict["id"]

        # challenges
        if not self.challenges_data:
            self.player_has_challenges = False
        else:
            self.player_has_challenges = True

        for challenge in self.challenges_data:
            challenge_id = int(challenge["challenge_id"])
            challenge_dict = LeagueStaticDataService.get_challenge(challenge_id)
            if not challenge_dict:
                challenge["description"] = challenge_id
                continue
            challenge["name"] = challenge_dict["name"]
            challenge["percentile_percentage"] = round((challenge["percentile"]*100), 1)
            challenge["description"] = challenge_dict["description"]
            challenge["max_value"] = 0
            challenge["image"] = f"league/ddragon/{self.current_patch}/img/challenges-images/{challenge_id}-{challenge['challenge_tier']}.png"
    