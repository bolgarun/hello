from application import db
from datetime import datetime
from auth.models import User


class Articl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)
    user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)