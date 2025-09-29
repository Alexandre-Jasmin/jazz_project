import datetime

from app.db import DBConnection

class LeagueDbBackgroundWorker:

    def __init__(self):
        pass

    def tasks_loop(self) -> None:
        self._test_league_db_connection()

    def _test_league_db_connection(self) -> None:
        with DBConnection() as db:
            print(f"[{datetime.datetime.now()}] leaguedb.background.worker: connection stable")