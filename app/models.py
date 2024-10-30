from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa 
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login 
from enum import Enum
from hashlib import md5

class UserRole(Enum):
    ADMIN = 'admin'
    GHOSTBUSTER = 'ghostbuster'

class Ghosts(db.Model):
    __tablename__ = 'ghosts'

    id: so.Mapped[int] = db.Column(sa.Integer, primary_key=True)
    ghost_name: so.Mapped[str] = db.Column(sa.String[120], index=True, unique=True)
    description: so.Mapped[Optional[str]] = db.Column(sa.String(140))
    power_level: so.Mapped[int] = db.Column(sa.Integer)
    status: so.Mapped[str] = db.Column(sa.Enum("captured", "not captured", name="ghost_status_enum", default="not captured", nullable=False))
    special_abilities: so.Mapped[Optional[str]] = db.Column(sa.String(140))
    api_endpoint: so.Mapped[Optional[str]] = db.Column(sa.String(255))
    public: so.Mapped[bool] = db.Column(sa.Boolean, default=True)
    captured_by: so.Mapped[Optional[int]] = db.Column(sa.Integer, sa.ForeignKey('ghostbusters.user_id'), name="ghost_captured_by_user_id")
    picture_url: so.Mapped[Optional[str]] = db.Column(sa.String(255), nullable=True, default=None)

    captor: so.Mapped['Ghostbusters'] = so.relationship("Ghostbusters", back_populates="captured_ghosts")

class Ghostbusters(UserMixin, db.Model):
    __tablename__ = 'ghostbusters'
    user_id: so.Mapped[int] = db.Column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = db.Column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = db.Column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = db.Column(sa.String(256))
    role: so.Mapped[UserRole] = db.Column(sa.Enum(UserRole), name="user_role", default=UserRole.GHOSTBUSTER)
    first_name: so.Mapped[str] = db.Column(sa.String(64))
    last_name: so.Mapped[str] = db.Column(sa.String(64))
    join_date: so.Mapped[Optional[datetime]] = db.Column(sa.DateTime, default=datetime.now(timezone.utc))
    last_login: so.Mapped[Optional[datetime]] = db.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))

    

    captured_ghosts: so.Mapped[list['Ghosts']] = so.relationship("Ghosts", back_populates="captor")

    def __repr__(self):
        return '<ghostbuster {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_id(self):
        return str(self.user_id)

@login.user_loader
def load_user(id):
    return Ghostbusters.query.get(int(id))