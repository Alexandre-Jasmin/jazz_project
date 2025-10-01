from pathlib import Path
import requests
import tarfile
from app.utilities import BasicUtilities #! utilities should handle downloading and extracting code

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DDRAGON_DIR = DATA_DIR / "league" / "ddragon"
DDRAGON_VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

class DataDragonUpdater:

    def __init__(self):
        pass

    def get_local_version(self) -> str:
        path = DDRAGON_DIR
        p = Path(path)
        dirs = [d.name for d in p.iterdir() if d.is_dir()]
        return dirs[-1]

    def get_latest_version(self) -> str:
        response = requests.get(DDRAGON_VERSIONS_URL)
        versions = response.json()
        return versions[0]

    def update_league_assets(self) -> str:
        #* Get latest version of ddragon
        latest_version = self.get_latest_version()
        local_version = self.get_local_version()

        if local_version == latest_version:
            print(f"ddragon up-to-date ({local_version})")
            return local_version

        archive_path = DATA_DIR / "dragontail_temp.tgz"
        url = f"https://ddragon.leagueoflegends.com/cdn/dragontail-{latest_version}.tgz"

        update_choice = input(f"Update available\nLocal Version: {local_version}\nLatest Version: {latest_version}\nUpdate? (y/n)")
        if update_choice == "n":
            print("Update Canceled")
            return local_version

        print(f"Downloading {url} ...")
        response = requests.get(url, stream=True)
        with open(archive_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded to {archive_path}")

        print("Extracting ...")
        NEW_DDRAGON_DIR = DDRAGON_DIR / latest_version
        Path(NEW_DDRAGON_DIR).mkdir()
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=NEW_DDRAGON_DIR)
        print(f"Extracted to {NEW_DDRAGON_DIR}")

        print("Cleaning archive")
        archive_path.unlink()
        print("Cleaned archive")

        #! we also need to get the latest ranked emblems
        #! extract inside current_patch
        #! https://static.developer.riotgames.com/docs/lol/ranked-emblems-latest.zip

        return latest_version