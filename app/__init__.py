import time
import threading
from flask import Flask

from .routes import register_blueprints
from app.services.riot_service import RiotService
from app.services.background_workers.leaguedb_background_worker import LeagueDbBackgroundWorker
from app.services.background_workers.league_background_worker import LeagueBackgroundWorker

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
        (league_worker.acquire_loop_data, 60, [], {}),
        (leaguedb_worker.tasks_loop, 60, [], {}),
    ]

    threads = []
    for func, interval, args, kwargs in workers:
        threads.append(start_specific_background_worker(func, interval, *args, **kwargs))
    return threads

def create_flask_app(config: str = "config.DevelopmentConfig") -> Flask:
    app = Flask(__name__)

    start_all_background_workers()

    app.config.from_object(config)
    register_blueprints(app)

    return app