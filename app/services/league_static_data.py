from pathlib import Path

from config import DevelopmentConfig
from app.utilities import BasicUtilities

class LeagueStaticDataService:
    _current_patch = None
    _champions = None
    _challenges = None

    @classmethod
    def _get_latest_patch_from_dir(cls) -> str:
        p = Path(DevelopmentConfig.DDRAGON_DIR)
        dirs = [d.name for d in p.iterdir() if d.is_dir()]
        # Sort patches numerically instead of string order
        dirs.sort(key=lambda v: [int(x) for x in v.split('.')])
        return dirs[-1]

    @classmethod
    def load(cls):
        cls._current_patch = cls._get_latest_patch_from_dir()

        base_dir = DevelopmentConfig.DDRAGON_DIR / cls._current_patch / cls._current_patch / "data" / "en_US"
        utils = BasicUtilities()

        cls._champions = utils.read_json_file(base_dir / "champion.json")
        cls._challenges = utils.read_json_file(base_dir / "challenges.json")

    @classmethod
    def get_champion_data(cls) -> dict:
        if cls._champions is None:
            cls.load()
        return cls._champions
    
    @classmethod
    def get_champion(cls, champion_id: int) -> dict | None:
        champions = cls.get_champion_data()["data"].values()
        for champ in champions:
            if int(champ["key"]) == champion_id:
                return champ
        return None
    
    @classmethod
    def get_challenges_data(cls) -> list:
        if cls._challenges is None:
            cls.load()
        return cls._challenges
    
    @classmethod
    def get_challenge(cls, challenge_id: int) -> dict | None:
        challenges = cls.get_challenges_data()
        for challenge in challenges:
            if challenge["id"] == challenge_id:
                return challenge
        return None

    @classmethod
    def get_patch(cls) -> str:
        if cls._current_patch is None:
            cls.load()
        return cls._current_patch
    
    @classmethod
    def refresh(cls):
        cls.load()