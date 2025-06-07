from dataclasses import dataclass
from cineTogether import db

@dataclass
class Movie(db.Model):
    __tablename__ = "movies"

    id: int
    rank: int
    title: str
    description: str
    year: int
    rating: float
    genre: str
    image: str
    imdbid: str
    imdb_link: str

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(512), nullable=True)
    imdbid = db.Column(db.String(20), nullable=True)
    imdb_link = db.Column(db.String(255), nullable=True)

    @classmethod
    def add_movie(cls, **kwargs):
        movie = cls(**kwargs)
        db.session.add(movie)
        db.session.commit()
        return movie

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.rank.asc()).all()

    @classmethod
    def get_by_id(cls, movie_id):
        return cls.query.get(movie_id)

    @classmethod
    def update_movie(cls, movie_id, **kwargs):
        movie = cls.query.get(movie_id)
        if not movie:
            return None
        for key, value in kwargs.items():
            if hasattr(movie, key) and value is not None:
                setattr(movie, key, value)
        db.session.commit()
        return movie

    @classmethod
    def delete_movie(cls, movie_id):
        movie = cls.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
