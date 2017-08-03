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


class BucketlistView(Resource):
    """Bucket list CRUD functionality."""

    def __init__(self):
        """Initialize bucketlist Resource."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Authorization', type=str, location="headers")
        self.reqparse.add_argument('name', type=str, location="json")
        self.reqparse.add_argument('description', type=str, location="json")


    def post(self):
        """Add new bucketlist."""
        args = self.reqparse.parse_args()
        user_id = validate_token(self)

        if not isinstance(user_id, int):
            response = {
                        'status': 'fail',
                        'message': user_id
                        }
            return (response), 401

        if not args['name']:
            response = {
                        'message': 'Please enter a Bucketlist name!',
                        'status': 'fail'
                        }
            return response, 400

        if Bucketlist.query.filter_by(name=args['name'], created_by=user_id).first():
                    # if bucketlist with given name exists
            response = {
                        'message': 'This Bucketlist already exists !',
                        'status': 'fail'
                        }
            return response, 409
        bucketlist = Bucketlist(name=args['name'],
                                description=args['description'],
                                created_by=user_id)
        bucketlist.save()
        response = {
                    'message': 'Bucketlist {} Added!'.format(args['name']),
                    'status': 'success'
                    }
        return response, 201

    def get(self, id=None):
        """View bucketlists."""
        user_id = validate_token(self)
        if not isinstance(user_id, int):
            response = {
                        'status': 'fail',
                        'message': user_id
                        }
            return (response), 401

        self.reqparse.add_argument('limit', type=int, help='invalid limit',
            required=False, default=20, location='args')
        self.reqparse.add_argument('q', type=str, help='Invalid Query',
            required=False, location='args')
        self.reqparse.add_argument('page', type=int, required=False, default=1, location='args')
        args = self.reqparse.parse_args()
        bucketlists_data = []
        if id:
            # retrieve a bucketlist
            bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
            if not bucketlist:
                    response = {
                                'status': 'fail',
                                'message': 'Bucketlist cannot be found'
                                }
                    return (response), 404

            if not bucketlist.items:
                    items = {}
            else:
                item_data = []
            for item in bucketlist.items:
                items = {
                        "item_id": item.id,
                        "item_name": item.name,
                        "item_description": item.description
                        }
                item_data.append(items)
            response = {
                            'id': bucketlist.id,
                            'title': bucketlist.name,
                            'description': bucketlist.description,
                            'created_on': str(bucketlist.created_on),
                            'items': item_data
                }
            return (response), 200
        if args['q']:

            bucketlist = Bucketlist.query \
                          .filter_by(created_by=user_id) \
                          .filter(Bucketlist.name
                                  .ilike('%' + args['q'] + '%')).paginate(page=args['page'],
                                                                         per_page=args['limit'],
                                                                         error_out=False)


            for bucket in bucketlist.items:
                bucketlists = {
                        'id': bucket.id,
                        'title': bucket.name,
                        'description': bucket.description,
                        'created_on': str(bucket.created_on),
                        }
                bucketlists_data.append(bucketlists)
            return (bucketlists_data), 200

        else:
            bucketlist = (Bucketlist.query.filter_by(created_by=user_id).paginate(page=args['page'],
                                                   per_page=args['limit'],
                                                   error_out=False))

            for bucket in bucketlist.items:
                bucketlists = {
                        'id': bucket.id,
                        'title': bucket.name,
                        'description': bucket.description,
                        'created_on': str(bucket.created_on),
                        }
                bucketlists_data.append(bucketlists)
            return (bucketlists_data), 200
