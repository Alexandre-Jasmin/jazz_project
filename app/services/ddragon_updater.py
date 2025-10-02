from pathlib import Path
import requests
import tarfile
from app.utilities import BasicUtilities

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DDRAGON_DIR = DATA_DIR / "league" / "ddragon"
DDRAGON_VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

class DataDragonUpdater:

    def __init__(self):
        pass

    def _get_local_ddragon_version(self) -> str:
        try:
            p = Path(DDRAGON_DIR)
            dirs = [d.name for d in p.iterdir() if d.is_dir()]
            return dirs[-1]
        except:
            return None
    
    def _get_latest_ddragon_version(self) -> str | None:
        try:
            response = requests.get(DDRAGON_VERSIONS_URL)
            versions = response.json()
            return versions[0]
        except:
            return None
    
    def update_ddragon_assets(self) -> tuple:
        latest_version = self._get_latest_ddragon_version()
        local_version = self._get_local_ddragon_version()

        if not local_version or not latest_version:
            return False, "failed to get local_version/latest_version"
        
        if local_version == latest_version:
            return False, f"assets up-to-date ({local_version})"
        
        update_choice = input(f"\nUpdate available\nLocal Version: {local_version}\nLatest Version: {latest_version}\nUpdate? (y/n)")#! lower
        if update_choice != "y":
            return False, "user input is not yes"
        
        NEW_DDRAGON_DIR = DDRAGON_DIR / latest_version
        url = f"https://ddragon.leagueoflegends.com/cdn/dragontail-{latest_version}.tgz"
        archive_path = DATA_DIR / "dragontail_temp.tgz"

        BasicUtilities.download_file(url, archive_path)
        BasicUtilities.extract_tar_gz(archive_path, NEW_DDRAGON_DIR)
        archive_path.unlink()

        return True, latest_version