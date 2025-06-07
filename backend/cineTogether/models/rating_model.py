from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Rating(db.Model):
    __tablename__ = "ratings"

    id: int
    user_id: int
    movie_id: int
    rating: float
    comment: str
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )

    @classmethod
    def add_rating(cls, user_id, movie_id, rating, comment=None):
        existing = cls.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing:
            return None  # zaten puan vermiş

        new_rating = cls(user_id=user_id, movie_id=movie_id, rating=rating, comment=comment)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating

    @classmethod
    def get_ratings_by_movie(cls, movie_id):
        return cls.query.filter_by(movie_id=movie_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_average_rating(cls, movie_id):
        from sqlalchemy import func
        avg = db.session.query(func.avg(cls.rating)).filter_by(movie_id=movie_id).scalar()
        return round(avg, 2) if avg else 0.0
