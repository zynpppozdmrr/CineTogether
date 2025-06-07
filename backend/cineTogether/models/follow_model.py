from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Follow(db.Model):
    __tablename__ = "follows"

    follower_id: int
    followee_id: int
    followed_at: datetime

    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    followee_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def follow(cls, follower_id, followee_id):
        if follower_id == followee_id:
            return None  # Kullanıcı kendini takip edemez

        existing = cls.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if existing:
            return None  # Zaten takip ediyor

        new_follow = cls(follower_id=follower_id, followee_id=followee_id)
        db.session.add(new_follow)
        db.session.commit()
        return new_follow

    @classmethod
    def unfollow(cls, follower_id, followee_id):
        follow = cls.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_followers(cls, user_id):
        return cls.query.filter_by(followee_id=user_id).all()

    @classmethod
    def get_following(cls, user_id):
        return cls.query.filter_by(follower_id=user_id).all()
