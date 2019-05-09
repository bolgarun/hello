from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(2008))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    country = db.Column(db.String(2406))
    active = db.Column(db.Boolean, default=False)
    nickname = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
        self.id, self.first_name, self.last_name,
        self.email, self.password_hash, self.age, self.gender,
        self.timestamp, self.country, self.active, self.nickname) 

    def write_fullname(self):
    	return 'User: {}, {}'.format(self.first_name, self.last_name)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_token = db.Column(db.String(200), unique=True)
    expire_date = db.Column(db.DateTime, default=datetime.utcnow)