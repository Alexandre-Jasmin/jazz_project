import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class DevelopmentConfig:

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    BASE_SQL_DIR = BASE_DIR / "sql"
    DDRAGON_DIR = DATA_DIR / "league" / "ddragon"

    RIOT_API_KEY = os.getenv("RIOT_API_KEY")

    LEAGUE_DB_HOST = os.getenv("LEAGUE_DB_HOST")
    LEAGUE_DB_USER = os.getenv("LEAGUE_DB_USER")
    LEAGUE_DB_PASSWORD = os.getenv("LEAGUE_DB_PASSWORD")
    LEAGUE_DB_NAME = os.getenv("LEAGUE_DB_NAME")
    LEAGUE_DB_PORT = int(os.getenv("LEAGUE_DB_PORT"))

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

class LeagueDBConfig:

    BASE_DIR = Path(__file__).resolve().parent
    HOST = os.getenv("LEAGUE_DB_HOST")
    USER = os.getenv("LEAGUE_DB_USER")
    PASSWORD = os.getenv("LEAGUE_DB_PASSWORD")
    NAME = os.getenv("LEAGUE_DB_NAME")
    PORT = int(os.getenv("LEAGUE_DB_PORT"))
    BASE_SQL_DIR = BASE_DIR / "sql" / "leaguedb"