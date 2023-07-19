from . import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    recommendations = db.relationship('Recommendation', backref='movie', lazy='dynamic')

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
