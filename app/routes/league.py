from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services import RiotService, PlayerBuilder
from app.repository.league_player_repo import LeaguePlayerRepository
from app.utilities import LeagueUtilities

league = Blueprint("league", __name__, url_prefix="/lol")

riot_service = RiotService()
player_repo = LeaguePlayerRepository()
player_builder = PlayerBuilder(riot_service, player_repo)
league_utils = LeagueUtilities()

@league.route("/")
def home():
    return render_template("league_home.html")

@league.route("/search_summoner", methods=["POST"])
def find_summoner():

    try:
        server = request.form.get("server")
        summoner_name = request.form.get("summoner")
    except Exception as e:
        return render_template("error.html", error=e)
    
    return redirect(url_for("league.get_summoner", server=server, summoner_name=summoner_name))

@league.route("/summoner/<server>/<summoner_name>")
def get_summoner(server: str, summoner_name: str):

    name, tag = league_utils.split_summoner_name(summoner_name)
    if name is None or tag is None:
        return render_template("error.html", error="Can't split summoner name")
    
    try:
        player = player_builder.get_player(name, tag, server)
    except Exception as e:
        return render_template("error.html", error=e)
    
    return render_template("league_player_home.html", player=player) 

@league.route("/summoner/<server>/<summoner_name>/refresh", methods=["POST"])
def refresh_summoner(server: str, summoner_name: str):

    name, tag = league_utils.split_summoner_name(summoner_name)
    if name is None or tag is None:
        return render_template("error.html", error="Can't split summoner name")
    
    try:
        data = player_builder.repo.fetch_account_summoner_data_name(name, tag, server)
        if data:
            last_updated = data["last_updated"]
            if last_updated > datetime.now() - timedelta(minutes=1):
                flash("You can only refresh every minute.", "warning")
            else:
                player_builder._refresh_player(name, tag, server)
                flash("Profile refreshed!", "success")
        else:
            player_builder._refresh_player(name, tag, server)
            flash("New profile added and refreshed!", "success")
    except Exception as e:
        return render_template("error.html", error=e)

    return redirect(url_for("league.get_summoner", server=server, summoner_name=summoner_name))