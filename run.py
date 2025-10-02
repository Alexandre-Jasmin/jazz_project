from app import create_flask_app
from app.services.ddragon_updater import DataDragonUpdater

# before creating application, make sure assets are up to date
ddragon_updater = DataDragonUpdater()
status, message = ddragon_updater.update_ddragon_assets()
print(message)

app = create_flask_app()

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)