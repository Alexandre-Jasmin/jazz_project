from pathlib import Path

from app.services import RiotService

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LEAGUE_DIR = DATA_DIR / "league"
MATCHES_DIR = LEAGUE_DIR / "matches" 
LEAGUE_ARENA_DIR = LEAGUE_DIR / "arena"
RANKED_LADDER_PATH = LEAGUE_DIR / "ranked_ladder"

HIGH_LEAGUES = ['challengerleagues', 'grandmasterleagues', 'masterleagues']
LEAGUES = ['BRONZE', 'SILVER', 'GOLD', 'IRON', 'PLATINUM', 'EMERALD', 'DIAMOND']
DIVISIONS = ['IV', 'III', 'II', 'I']

class LeagueBackgroundWorker:

    def __init__(self, riot: RiotService):
        self.riot = riot

    def acquire_loop_data(self) -> None:
        self.riot.set_region("na1")
        #self._get_ranked_ladder()
        #self._dump_random_matches()

    #! auto update players in database