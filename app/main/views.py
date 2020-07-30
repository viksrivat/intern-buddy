import os

from flask import render_template, request, jsonify, current_app, send_from_directory, session

from app import db
from app.main import main
import time

@main.route("/")
def index():
    return render_template('index.html')
