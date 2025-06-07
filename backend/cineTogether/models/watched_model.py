from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Watched(db.Model):
    __tablename__ = "watched"

    user_id: int
    movie_id: int
    watched_at: datetime

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def mark_as_watched(cls, user_id, movie_id):
        existing = cls.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing:
            return None
        entry = cls(user_id=user_id, movie_id=movie_id)
        db.session.add(entry)
        db.session.commit()
        return entry

    @classmethod
    def unmark(cls, user_id, movie_id):
        entry = cls.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
