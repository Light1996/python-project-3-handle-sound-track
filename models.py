from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    filename = db.Column(db.String(80))
    password = db.Column(db.String(80))
    repassword = db.Column(db.String(80))


class TrackRecords(db.Model):
    __tablename__ = 'trackrecords'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    year = db.Column(db.String(80))
    artist = db.Column(db.String(80))
    composer = db.Column(db.String(80))
