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

    

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()
