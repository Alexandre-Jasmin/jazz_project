from flask import Blueprint, render_template, request, redirect, url_for

from app.services import RiotService, PlayerBuilder
from app.models import LeaguePlayer
from app.utilities import LeagueUtilities

league = Blueprint("league", __name__, url_prefix="/lol")

riot_service = RiotService()
player_builder = PlayerBuilder(riot_service)
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
        player = player_builder.main_build(name, tag, server)
        return render_template("league_player_home.html", player=player)
    except Exception as e:
        return render_template("error.html", error=e)