"""models."""
import os
import jwt
from app import db
from datetime import datetime, timedelta


class User(db.Model):
    """user table."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    email = db.Column(db.String(25), unique=True)
    bucketlists = db.relationship('Bucketlist', backref='user',
                                  cascade='all, delete',
                                  lazy='dynamic')

    def save(self):
        """Save a bucketlist."""
        db.session.add(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=33),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv("SECRET"),
                algorithm='HS256'
            ).decode("utf-8")

        except Exception as e:
            print(e)

    @staticmethod
    def decode_auth_token(auth_token):

        try:
            payload = jwt.decode(auth_token, os.getenv("SECRET"))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
