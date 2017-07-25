"""Bucket list API endpoints."""
import re
from flask import g
import jwt
import json
from flask_restful import reqparse, Resource
from flask import jsonify, make_response, request
from app.models import User, Bucketlist, Item
from app import db


def validate_token(self):
    # get the auth token
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('Authorization', type=str, location="headers")
    args = self.reqparse.parse_args()
    token = args["Authorization"]
    if token:
        user_id = User.decode_auth_token(token)
        return user_id
    print(token)

class AuthRegister(Resource):
    """User registration."""

    def __init__(self):
        """Initialize register resource endpoint."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('email', type=str, help='Email required')

    def post(self):
        """Create new user."""
        args = self.reqparse.parse_args()
        username = args['username']
        if len(username.strip(" ")) == 0:
            response = {
                        "message": "Please provide a username!",
                        "status": "fail"
                        }

            return response, 400

        if len(args['password']) < 8:
            response = {
                        'message': 'Password needs to be 8 characters long!',
                        'status': 'fail'
                        }
            return response, 400

        if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$',
                        args['email']):
            response = {
                        'status': 'fail',
                        'message': 'Invalid email!'
                        }
            return (response), 400

        if User.query.filter_by(username=args['username']).first():
                    # if user with given username exists
            response = {
                        'message': 'A User with the same name already exists!',
                        'status': 'fail'
                        }
            return response, 409
        if User.query.filter_by(email=args['email']).first():
                    # if user with given username exists
            response = {
                        'message': 'This email account has already been used!',
                        'status': 'fail'
                        }
            return response, 409

        new_user = User(username=args['username'],
                    email=args['email'],
                    password=args['password'])
        new_user.save()
        return {'message': 'User Registration success!'}, 201



class AuthLogin(Resource):
    """Log in resource."""

    def __init__(self):
        """Initialize log in resource."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        """Authenticate user."""
        args = self.reqparse.parse_args()
        try:
            auth_user = User.query.filter_by(username=args['username']).first()

            if not auth_user:
                response = {'status': 'fail',
                            'message': 'Invalid username/password!'
                            }
                return (response), 401
            auth_token = auth_user.encode_auth_token(auth_user.id)
            print("auth token", auth_token)
            if not auth_token:
                response = {'status': 'fail',
                            'message': 'Login failed! Please try again'
                            }
                return (response), 401

            response = {'status': 'success',
                        'message': 'You have successfully logged in.',
                        'auth_token': auth_token
                        }

            return (response), 200
        except Exception as e:
            response = {'status': str(e),
                        'message': 'Login failed! Please try again'
                        }
            return (response), 500
