class LeaguePlayer:

    def __init__(self, account_summoner_data, champion_mastery_data, ranked_data):
        
        self.account_summoner_data = account_summoner_data
        self.champion_mastery_data = champion_mastery_data
        self.ranked_data = ranked_data
        
        self.jazz_id = self.account_summoner_data["puuid"][:5]
        self.name = f'{self.account_summoner_data["game_name"]}#{self.account_summoner_data["tag_line"]}'

        # win rate
        # champion names