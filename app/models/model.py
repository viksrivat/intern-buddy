from sqlalchemy.orm import relationship

from app import db
import datetime

class SchoolLevel:
    undergraduate = 0
    graduate = 1
    other = 2

class GroupSize:
    small = 0 
    medium = 1
    high = 2

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

    @property
    def paired(self):
        return self.group is not None

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
