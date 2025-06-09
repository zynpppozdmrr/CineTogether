from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Comment(db.Model):
    __tablename__ = "comments"

    id: int
    user_id: int
    post_id: int
    text: str
    is_active: bool
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # ✅ Soft delete flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Yorum oluştur
    @classmethod
    def create_comment(cls, user_id, post_id, text):
        comment = cls(user_id=user_id, post_id=post_id, text=text)
        db.session.add(comment)
        db.session.commit()
        return comment

    # ✅ Post'a ait aktif yorumları getir
    @classmethod
    def get_comments_by_post(cls, post_id):
        from .user_model import User # Circular import önlemek için burada import ediyoruz
        # Yorumları User tablosu ile birleştirip (join) her iki tablodaki aktiflik durumunu kontrol ediyoruz
        return cls.query.join(User, User.id == cls.user_id).filter(cls.post_id == post_id, cls.is_active == True, User.activated == True).order_by(cls.created_at.desc()).all()
    # ✅ Soft delete
    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.query.get(comment_id)
        if comment and comment.is_active:
            comment.is_active = False
            db.session.commit()
            return True
        return False

    # ✅ Tekil yorum getir (aktifse)
    @classmethod
    def get_by_id(cls, comment_id):
        comment = cls.query.get(comment_id)
        return comment if comment and comment.is_active else None
