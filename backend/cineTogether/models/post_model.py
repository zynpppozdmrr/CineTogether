from dataclasses import dataclass
from datetime import datetime
from cineTogether import db

@dataclass
class Post(db.Model):
    __tablename__ = "posts"

    id: int
    user_id: int
    content: str
    image_url: str
    is_official: bool
    is_active: bool
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    is_official = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # ✅ Soft delete flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create_post(cls, user_id, content, image_url=None, is_official=False):
        post = cls(
            user_id=user_id,
            content=content,
            image_url=image_url,
            is_official=is_official
        )
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_active=True).order_by(cls.created_at.desc()).all()  # ✅ Sadece aktif postlar

    @classmethod
    def get_by_id(cls, post_id):
        post = cls.query.get(post_id)
        if post and post.is_active:
            return post
        return None

    @classmethod
    def delete_post(cls, post_id):
        post = cls.query.get(post_id)
        if post and post.is_active:
            post.is_active = False  # ✅ Silme yerine pasifleştirme
            db.session.commit()
            return True
        return False
    
    @classmethod
    def update_post(cls, post_id, content=None, image_url=None):
        # ID ile postu veritabanından bul
        post = cls.query.get(post_id)

        # Post bulunamazsa veya pasifse None döndür
        if not post or not post.is_active:
            return None

        # Güncellemek istenen alanlar varsa değiştir
        if content is not None:
            post.content = content

        if image_url is not None:
            post.image_url = image_url

        # Veritabanına değişiklikleri kaydet
        from cineTogether import db
        db.session.commit()

        # Güncellenen postu geri döndür
        return post

    @classmethod
    def reactivate_post(cls, post_id):
        post = cls.query.get(post_id)
        if post and not post.is_active:
            post.is_active = True
            db.session.commit()
            return post
        return None
