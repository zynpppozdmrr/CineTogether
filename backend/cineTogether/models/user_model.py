from datetime import datetime
from cineTogether import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int
    username: str
    email: str
    password: str
    full_name: str
    bio: str
    profile_picture_url: str
    role: str
    activated: bool
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False) # hashed password
    full_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    activated = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def add_user(cls, username, email, password, full_name=None, bio=None, profile_picture_url=None, role="user"):
        hashed_password = generate_password_hash(password)
        new_user = cls(
            username=username,
            email=email,
            password=hashed_password,
            full_name=full_name,
            bio=bio,
            profile_picture_url=profile_picture_url,
            role=role,
            activated=True,
            created_at=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        if user:
            user.activated = False  # kalıcı silme yerine pasif etme
            db.session.commit()
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def update_user(cls, user_id, **kwargs):
        user = cls.query.get(user_id)
        if user:
            for key, value in kwargs.items():
                # Güvenlik: email ve username güncellenemez
                if key in ["email", "username"]:
                    continue

                # Şifre hash'leme işlemi
                if key == "password" and value:
                    from werkzeug.security import generate_password_hash
                    value = generate_password_hash(value)

                # Yalnızca mevcut attribute'lar ve boş olmayan veriler güncellenir
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)

            db.session.commit()
            return user

