from app import create_flask_app
from app.services.ddragon_updater import DataDragonUpdater

ddragon_updater = DataDragonUpdater()
current_version = ddragon_updater.update_league_assets()

app = create_flask_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

#add image icon to champion mastery