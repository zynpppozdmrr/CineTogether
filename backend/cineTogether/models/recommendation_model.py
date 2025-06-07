
from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Recommendation(db.Model):
    __tablename__ = "recommendations"

    user_id: int
    movie_id: int
    score: float
    recommended_at: datetime

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True)
    score = db.Column(db.Float, nullable=False)
    recommended_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def generate_for_user(cls, user_id, top_n=10):
        from collections import defaultdict
        from cineTogether.models.favorite_model import Favorite
        from cineTogether.models.movie_model import Movie

        favorites = Favorite.query.filter_by(user_id=user_id).all()

        if not favorites:
            cls.query.filter_by(user_id=user_id).delete()
            top_movies = Movie.query.order_by(Movie.rating.desc()).limit(top_n).all()
            for movie in top_movies:
                entry = cls(user_id=user_id, movie_id=movie.id, score=movie.rating or 0)
                db.session.add(entry)
            db.session.commit()
            return cls.query.filter_by(user_id=user_id).all()

        genre_scores = defaultdict(int)
        for fav in favorites:
            movie = Movie.get_by_id(fav.movie_id)
            if movie and movie.genre:
                for genre in movie.genre.split(", "):
                    genre_scores[genre] += 1

        if not genre_scores:
            return []

        sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
        top_genres = [g for g, _ in sorted_genres[:3]]
        user_fav_ids = set(f.movie_id for f in favorites)

        candidate_movies = Movie.query.all()
        recommendations = []

        for movie in candidate_movies:
            if movie.id in user_fav_ids or not movie.genre:
                continue
            movie_genres = movie.genre.split(", ")
            match_count = len([g for g in movie_genres if g in top_genres])
            if match_count > 0:
                score = match_count / len(movie_genres)
                recommendations.append((movie.id, score))

        cls.query.filter_by(user_id=user_id).delete()
        for movie_id, score in sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]:
            entry = cls(user_id=user_id, movie_id=movie_id, score=score)
            db.session.add(entry)

        db.session.commit()
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_recommendations(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.score.desc()).all()
