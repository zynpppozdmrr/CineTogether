from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Like(db.Model):
    __tablename__ = "likes"
    
    user_id: int
    post_id: int
    created_at: datetime

    # PRIMARY KEY olarak iki sütun birlikte kullanılacak
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )

    @classmethod
    def add_like(cls, user_id, post_id):
        existing = cls.query.get((user_id, post_id))
        if existing:
            return None  # zaten beğenmiş
        like = cls(user_id=user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return like

    @classmethod
    def remove_like(cls, user_id, post_id):
        like = cls.query.get((user_id, post_id))
        if like:
            db.session.delete(like)
            db.session.commit()
            return True
        return False

    @classmethod
    def count_likes(cls, post_id):
        return cls.query.filter_by(post_id=post_id).count()


    @classmethod
    def get_likes_by_post(cls, post_id):
        return cls.query.filter_by(post_id=post_id).all()
