import os

from flask import render_template, request, jsonify, current_app, send_from_directory, session

from app import db
from app.main import main
from app.models.record import Record, Tag
from .. import socketio
from flask_socketio import emit, join_room, leave_room
import numpy as np
import tensorflow as tf
import torch
import pickle
import spacy, re
from transformers import pipeline
import torch
import time

@main.route("/")
def index():
    return render_template('index.html')
