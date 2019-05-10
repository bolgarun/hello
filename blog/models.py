from application import db
from datetime import datetime


class Articl(db.Model):
	title = db.Column(db.String(60))
	text = db.Column(db.String(120))
	user = db.Column(db.String(64), unique=True)
	create_date = db.Column(db.DateTime, default=datetime.utcnow)