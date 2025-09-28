from flask import Flask
from .main import main
from .league import league

def register_blueprints(app: Flask):
    app.register_blueprint(main)
    app.register_blueprint(league)