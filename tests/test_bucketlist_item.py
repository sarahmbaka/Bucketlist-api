"""Test registration."""

import unittest
import json
import os
from app import create_app, db
from config import app_config

app = create_app("testing")
# app.config.from_object(app_config["testing"])

class TestBucketlistItems(unittest.TestCase):
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

        self.bucketlist = {
            "name" : "BlackB",
            "description" : "Black don't crack"
        }
        self.user_data1 = {
            "password": "12345678923",
            "username": "Black",
            "email": "black@gmail.com"
        }

        self.bucketlistitem = {
            "name" : "SouthC",
            "description" : "Black don't crack"
        }
        res = self.client.post('/auth/register', data=self.user_data)
        self.res = self.client.post('/auth/login', data=self.user_data)
        self.assertEqual(self.res.status_code, 200)
        self.response_data_in_json_format = json.loads(self.res.data.decode('utf-8'))
        # get auth token
        self.token = (self.response_data_in_json_format["auth_token"])
        self.headers = {'Authorization': self.token}
        #register second user
        res1 = self.client.post('/auth/register', data=self.user_data1)
        self.res1 = self.client.post('/auth/login', data=self.user_data1)
        self.response_data_in_json_format2 = json.loads(self.res1.data.decode('utf-8'))
        # get token for second user
        self.token2 = (self.response_data_in_json_format2["auth_token"])
        self.headers2 = {'Authorization': self.token2}
        # create bucketlist for first user
        res_bucketlist = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual("Bucketlist BlackB Added!",
                         res_message['message'])
        self.assertEqual(res_bucketlist.status_code, 201)

        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(self.bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlistitem.data.decode('utf8'))
        self.assertEqual("Item SouthC has been added",
                         res_message['message'])
        self.assertEqual(res_bucketlist.status_code, 201)

    def test_add_bucketlist_item(self):
        """Test that a user can  add."""
        bucketlistitem = {
            "name" : "SouthAfrica",
            "description" : "Black don't crack"
        }
        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlistitem.data.decode('utf8'))
        self.assertEqual("Item SouthAfrica has been added",
                         res_message['message'])
        self.assertEqual(res_bucketlistitem.status_code, 201)

    def test_add_already_bucketlist_item(self):
        """Test that a user can  add."""
        res_bucketlistitem1 = self.client.post('/bucketlist/1/items/', data=json.dumps(self.bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(self.bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlistitem.data.decode('utf8'))
        self.assertEqual("Bucketlist Item already exists!!",
                         res_message['message'])
        self.assertEqual(res_bucketlistitem.status_code, 409)

    def test_add_bucketlist_item_empty_name(self):
        """Test that a user can  add."""
        bucketlistitem = {
            "name" : "",
            "description" : "Black don't crack"
        }
        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlistitem.data.decode('utf8'))
        self.assertEqual("Please provide a name!!",
                         res_message['message'])
        self.assertEqual(res_bucketlistitem.status_code, 400)

    def test_add_bucketlist_item_invalid_token(self):
        """Test that a user can  add."""
        bucketlistitem = {
            "name" : "",
            "description" : "Black don't crack"
        }
        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(bucketlistitem)
                                          ,headers={'Authorization':'hjbjnbgjksngjvkdfnkj'}
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlistitem.data.decode('utf8'))
        self.assertEqual("Invalid token. Please log in again.",
                         res_message['message'])
        self.assertEqual(res_bucketlistitem.status_code, 401)

    def test_get_all_bucketlist_items(self):
        """Test that a user get all items."""
        bucketlistitem = {
            "name" : "BlackBill",
            "description" : "Black don't crack"
        }
        res_bucketlistitem = self.client.post('/bucketlist/1/items/', data=json.dumps(bucketlistitem)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlistitems = self.client.get('/bucketlist/1/items/',headers=self.headers
                                          ,content_type="application/json")

        self.assertEqual(res_bucketlistitems.status_code, 200)
        self.assertTrue(len(json.loads(res_bucketlistitems.data)) > 1)

    

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()





if __name__ == "__main__":
    unittest.main()