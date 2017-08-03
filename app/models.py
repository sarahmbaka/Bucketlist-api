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






class Bucketlist(db.Model):
    """Bucket lists table."""

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=datetime.now)
    modified_on = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='bucketlist',
                            cascade='all, delete',
                            lazy='dynamic')

    def save(self):
        """Save a bucketlist."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a bucketlist."""
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    """Item table."""

    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=datetime.now)
    modified_on = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def save(self):
        """Save a Item."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a Item."""
        db.session.delete(self)
        db.session.commit()
