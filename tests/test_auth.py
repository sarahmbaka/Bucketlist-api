"""Test registration."""

import unittest
import json
import os
from app import create_app, db
from config import app_config

app = create_app("testing")

class TestAuthRegister(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""

        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # create all tables
        db.create_all()

        self.user_data = {
            "password": "12345678923",
            "username": "sarahh",
            "email": "abner@gmail.com"
        }


    def test_registration(self):
        """Test user registration works correcty."""

        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)


    def test_already_registered_username(self):
        """Test that a user cannot be registered twice."""
        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 409)

    def test_already_registered_useremail(self):
        """Test that a user cannot be registered twice."""
        user1_data = {
            "password": "jkndsjbchjfr",
            "username": "Black",
            "email": "abner@gmail.com"
        }

        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/auth/register', data=user1_data)
        self.assertEqual(second_res.status_code, 409)

    def test_password_short(self):
        """Test that a user cannot be registered twice."""
        user1_data = {
            "password": "jknd",
            "username": "Black",
            "email": "abner@gmail.com"
        }
        res = self.client.post('/auth/register', data=user1_data)
        self.assertEqual(res.status_code, 400)

    def test_username_empty(self):
        """Test that a username cannot be empty."""
        user1_data = {
            "password": "jkn735473573d",
            "username": "",
            "email": "abner@gmail.com"
        }
        res = self.client.post('/auth/register', data=user1_data)
        self.assertEqual(res.status_code, 400)

    def test_email_format(self):
        """Test that a email is in the right format."""
        user1_data = {
            "password": "jkn735473573d",
            "username": "Sarah",
            "email": "abner@gmail"
        }
        res = self.client.post('/auth/register', data=user1_data)
        self.assertEqual(res.status_code, 400)
    def test_encode_auth_token(self):
        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        res1 = self.client.post('/auth/login', data=self.user_data)
        self.assertEqual(res1.status_code, 200)


    def tearDown(self):
        db.drop_all()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
