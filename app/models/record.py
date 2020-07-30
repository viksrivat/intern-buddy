from sqlalchemy.orm import relationship

from app import db
import datetime

class SCHOOL_LEVEL:
    undergraduate = 0
    graduate = 1
    other = 2

class AGE_GROUPS:
    age17_to_22 = 0
    a22_to_27 = 1
    a27_plus = 2

class GROUP_SIZE:
    low = 0 
    medium = 1
    high = 2

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    record_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    log = db.Column(db.String(140))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Preference(db.Model):
    __table_args__ = {'extend_existing': True}
    extend_existing = True
    preference_id = db.Column(db.Integer, db.ForeignKey('record.record_id'))
    location = db.Column(db.String)
    school = db.Column(db.String)
    group_size = db.Column(db.Integer)
    position_type = db.Column(db.String)
    age = db.Column(db.Integer)

    school_level = db.Column(db.Integer)
    hangout_outside = db.Column(db.String)
