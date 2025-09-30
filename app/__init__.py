import time
import threading
from flask import Flask

from .routes import register_blueprints
from app.services.riot_service import RiotService
from app.services.background_workers.leaguedb_background_worker import LeagueDbBackgroundWorker
from app.services.background_workers.league_background_worker import LeagueBackgroundWorker
from app.services.league_static_data import get_current_patch, get_current_champion_data, get_current_challenges_data

def run_worker(task_func, sleeping_time: int = 60, *args, **kwargs):
    while True:
        task_func(*args, **kwargs)
        time.sleep(sleeping_time)

def start_specific_background_worker(task_func, sleeping_time: int=60, *args, **kwargs) -> threading.Thread:
    thread = threading.Thread(
        target=run_worker,
        args=(task_func, sleeping_time, *args),
        kwargs=kwargs,
        daemon=True
    )
    thread.start()
    return thread

def start_all_background_workers():
    riot_service = RiotService()
    league_worker = LeagueBackgroundWorker(riot_service)
    leaguedb_worker = LeagueDbBackgroundWorker()

    workers = [
        # function, sleep interval, args, kwargs
        #(league_worker.acquire_loop_data, 3600, [], {}),
        (leaguedb_worker.tasks_loop, 600, [], {}),
    ]

    threads = []
    for func, interval, args, kwargs in workers:
        threads.append(start_specific_background_worker(func, interval, *args, **kwargs))
    return threads

def create_flask_app(config: str = "config.DevelopmentConfig") -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)

    start_all_background_workers()

    # Setup current league static data
    app.config["CURRENT_PATCH"] = get_current_patch()
    app.config["CHAMPION_DATA"] = get_current_champion_data()
    app.config["CURRENT_CHALLENGES"] = get_current_challenges_data()

    register_blueprints(app)

    return app