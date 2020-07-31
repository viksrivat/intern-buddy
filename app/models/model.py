from sqlalchemy.orm import relationship

from app import db, mail
from flask_mail import Message

import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import geopy
class SchoolLevel:
    undergraduate = 0
    graduate = 1
    other = 2

class GroupSize:
    small = 0 
    medium = 1
    large = 2

class Position:
    pm = 0
    ba = 1
    sde = 2

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    alexa_user_id = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    group = relationship("Group", back_populates="users")

    preference_id = db.Column(db.Integer, db.ForeignKey('preference.preference_id'))
    preferences = relationship("Preference", back_populates="user", foreign_keys=[preference_id], uselist=False)
    
    phone_number = db.Column(db.String)
    email = db.Column(db.String)

    @hybrid_property
    def paired(self):
        return self.group is not None

    @paired.expression
    def paired(cls):
        return cls.group is not None

    def get_preference_details_as_list(self):
        geolocator = geopy.Nominatim(user_agent="intern-buddy")
        geoLocation1 = geolocator.geocode(self.preferences.location)
        coordinate1 = (geoLocation1.latitude, geoLocation1.longitude)
        hangout_outside = 1 if self.preferences.hangout_outside else 0
        return [coordinate1[0], coordinate1[1], self.preferences.group_size, self.preferences.school_level, hangout_outside, self.preferences.position_type]
    
    def send_paired_email(self, group):
        users_in_group = group.users
        emails = [user.email for user in users_in_group]
        phone_numbers = [user.phone_number for user in user_in_group]
        body = """
        You have been matched with an Intern Buddy Group. Please contanct them and meet up. \n
        Emails: {} \n
        Phone Numbers: {} \n
        """.format(emails, phone_numbers)
        msg = Message(subject="New Alexa Intern Buddy",
              sender="alexainternbuddy@outlook.com",
              recipients=emails,
              body="You have been Matched with {}".format())
        
        # change message ID
        msg.msgId = msg.msgId.split('@')[0] + '@alexainternbuddy'  # for instance your domain name

        # send email
        mail.send(msg)

class Group(db.Model):
    __tablename__ = 'group'
    __table_args__ = {'extend_existing': True}
    group_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    users = relationship("User", back_populates="group", uselist=True)

class Preference(db.Model):
    __tablename__ = 'preference'
    __table_args__ = {'extend_existing': True}
    extend_existing = True
    preference_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    location = db.Column(db.String)
    school = db.Column(db.String)
    
    group_size = db.Column(db.Integer)
    position_type = db.Column(db.Integer)
    school_level = db.Column(db.Integer)

    hangout_outside = db.Column(db.Boolean)

    user = relationship("User", back_populates="preferences", uselist=False)
