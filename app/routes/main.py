from flask import Blueprint, render_template, send_from_directory
from config import DevelopmentConfig

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("main_index.html")

@main.route("/data/<path:filename>")
def data_file(filename):
    return send_from_directory(DevelopmentConfig.DATA_DIR, filename)