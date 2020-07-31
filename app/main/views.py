import os

from flask import render_template, request, jsonify, current_app, send_from_directory, session
from app.models.model import User, Preference, GroupSize, Position, SchoolLevel
from app import db
from app.main import main
import time

def parse_group_size(group_size):
    if group_size == 'large':
        return GroupSize.large
    if group_size == 'medium':
        return GroupSize.medium
    return GroupSize.small

def parse_position(position):
    if position == 'SDE' or position == 'sde' or position == 'Software Development Engineering':
        return Position.sde
    if position == 'Program Management' or position == 'pm' or position == 'PM':
        return Position.medium
    return GroupSize.small

def parse_school_level(position):
    if position == 'undergraduate' or position == 'undergraduate students' or position == 'undergraduates':
        return SchoolLevel.undergraduate
    if position == 'graduate students' or position == 'graduate' or position == 'graduates':
        return SchoolLevel.graduate
    return SchoolLevel.other

def parse_hangout_intent(hangout_str):
    return True if hangout_str == 'hang out' else False

@main.route("/session_info", methods=["POST", "GET"])
def session_details():
    content = request.json
    user_id = context['user_id']
    group_size_str = context['GroupSize']
    
    position_str = context['PositionIntent']
    age_group = context['AgeIntent']
    location = context['Location']
    school = context['School']
    hangout_intent_str = context['HangoutIntent']

    user = User(alexa_user_id=user_id)
    preference = Preference(group_size=parse_group_size(group_size_str),
                            position_type=parse_position(position_str), 
                            location=location, 
                            school=school,
                            school_level=parse_school_level(age_group),
                            hangout_outside=parse_hangout_intent(hangout_intent_str))
    db.session.add(preference)
    db.session.add(user)
    db.session.commit()
    user.preferences = preference
    db.session.commit
    return jsonify({"status": "created user account"})

@main.route("/")
def index():
    return render_template('index.html')
