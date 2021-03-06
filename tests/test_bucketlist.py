"""Test registration."""

import unittest
import json
import os
from app import create_app, db
from config import app_config

app = create_app("testing")
# app.config.from_object(app_config["testing"])

class TestBucketlist(unittest.TestCase):
    """Test case for the bucketlist blueprint."""

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

        self.user_data1 = {
            "password": "12345678923",
            "username": "Black",
            "email": "black@gmail.com"
        }

        self.bucketlist = {
            "name" : "Blackg",
            "description" : "Black don't crack"
        }
        res1 = self.client.post('/auth/register', data=self.user_data)
        self.res = self.client.post('/auth/login', data=self.user_data)
        self.assertEqual(self.res.status_code, 200)
        res1 = self.client.post('/auth/register', data=self.user_data1)
        self.res1 = self.client.post('/auth/login', data=self.user_data1)
        self.assertEqual(self.res1.status_code, 200)
        self.response_data_in_json_format2 = json.loads(self.res1.data.decode('utf-8'))
        self.response_data_in_json_format = json.loads(self.res.data.decode('utf-8'))
        # get auth token
        self.token = (self.response_data_in_json_format["auth_token"])
        self.token2 = (self.response_data_in_json_format2["auth_token"])
        self.headers = {'Authorization': self.token}
        self.headers2 = {'Authorization': self.token2}

        # create bucketlist for first user



    def test_add_bucketlist(self):
        """Test that a user can  add."""
        res_bucketlist = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual("Bucketlist Blackg Added!",
                         res_message['message'])
        self.assertEqual(res_bucketlist.status_code, 201)

    def test_add_already_existing_bucketlist(self):
        """Test that a user can  add."""



        res_bucketlist = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")

        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist1.data.decode('utf8'))
        self.assertEqual("This Bucketlist already exists !",
                         res_message['message'])
        self.assertEqual(res_bucketlist1.status_code, 409)

    def test_add_bucketlist_with_empty_name(self):
        """Test that a user can  add."""
        bucketlist = {
            "name" : "",
            "description" : "Black don't crack"
        }
        res_bucketlist = self.client.post('/bucketlist/', data=json.dumps(bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual("Please enter a Bucketlist name!",
                         res_message['message'])
        self.assertEqual(res_bucketlist.status_code, 400)

    def test_add_bucketlist_with_invalid_token(self):
        """Test that a user can  add."""

        res_bucketlist = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers={'Authorization':'hjbjnbgjksngjvkdfnkj'}
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual("Invalid token. Please log in again.",
                         res_message['message'])
        self.assertEqual(res_bucketlist.status_code, 401)

    def test_get_all_bucket(self):
        """Test that a user can  add."""
        bucketlist = {
            "name" : "BlackD",
            "description" : "Black don't crack"
        }
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist2 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/',headers=self.headers
                                          ,content_type="application/json")

        self.assertEqual(res_bucketlist.status_code, 200)
        
    def test_get_bucketlist_id(self):
        """Test that a user can  add."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/1',headers=self.headers
                                          ,content_type="application/json")


        self.assertEqual(res_bucketlist.status_code, 200)

    def test_get_bucketlist_with_invalid_token(self):
        """Test that a user can  add."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/1',headers={'Authorization':'hjbjnbgjksngjvkdfnkj'}
                                          ,content_type="application/json")


        self.assertEqual(res_bucketlist.status_code, 401)

    def test_get_bucketlist_with_unauthorized_token(self):
        """Test that a user can  add."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/1',headers=self.headers2
                                          ,content_type="application/json")
        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist cannot be found",
                         res_message['message'])


    def test_get_none_existent_bucketlist_id(self):
        """Test that a user can  add."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/2',headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist cannot be found",
                         res_message['message'])

    def test_update_bucketlist(self):
        """Test that a user can update bucketlist."""
        data = {
        "name": "Blackd",
        "description": "hey hey hey"
        }
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.put('/bucketlist/1',data= json.dumps(data),
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 200)
        self.assertEqual("Bucketlist Blackd Updated!",
                         res_message['message'])

    def test_update_non_existent_bucketlist(self):
        """Test that a user can update bucketlist."""
        data = {
        "name": "Blackd",
        "description": "hey hey hey"
        }
        res_bucketlist = self.client.put('/bucketlist/4',data= json.dumps(data),
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist does not exist!!",
                         res_message['message'])

    def test_update_empty_bucketlist_name(self):
        """Test that a user can not update bucketlist with empty name."""
        data = {
        "name": "",
        "description": "hey hey hey"
        }
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.put('/bucketlist/1',data= json.dumps(data),
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 400)
        self.assertEqual("Cannot update to empty bucketlist name.!!",
                         res_message['message'])

    def test_update_bucketlist_with_same_name(self):
        """Test that a user can not update bucketlist with same name."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        self.assertEqual(res_bucketlist1.status_code, 201)
        res_bucketlist = self.client.put('/bucketlist/1',data= json.dumps(self.bucketlist),
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 200)

    def test_update_bucketlist_with_invalid_token(self):
        """Test that a user can not update bucketlist with same name."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        self.assertEqual(res_bucketlist1.status_code, 201)
        res_bucketlist = self.client.put('/bucketlist/1',data= json.dumps(self.bucketlist),
                                          headers={'Authorization':'hjbjnbgjksngjvkdfnkj'}
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 401)
        self.assertEqual("Invalid token. Please log in again.",
                         res_message['message'])

    def test_update_bucketlist_with_unauthorized_token(self):
        """Test that a user can not update bucketlist with same name."""
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(self.bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        self.assertEqual(res_bucketlist1.status_code, 201)
        res_bucketlist = self.client.put('/bucketlist/1',data= json.dumps(self.bucketlist),
                                          headers=self.headers2
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist does not exist!!",
                         res_message['message'])


    def test_delete_bucketlist(self):
        """Test that a user can update bucketlist."""
        res_bucketlist = self.client.post('/bucketlist/',data= json.dumps(self.bucketlist),
                                          headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.delete('/bucketlist/1',
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 200)
        self.assertEqual("Bucketlist deleted.!!",
                         res_message['message'])

    def test_delete_non_existent_bucketlist(self):
        """Test that a user can update bucketlist."""
        res_bucketlist = self.client.delete('/bucketlist/1',
                                          headers=self.headers
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist does not exist.!!",
                         res_message['message'])

    def test_delete_bucketlist_with_unauthorized_token(self):
        """Test that a user can update bucketlist."""
        res_bucketlist1 = self.client.post('/bucketlist/',data= json.dumps(self.bucketlist),
                                          headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.delete('/bucketlist/1',
                                          headers=self.headers2
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 404)
        self.assertEqual("Bucketlist does not exist.!!",
                         res_message['message'])

    def test_delete_bucketlist_with_invalid_token(self):
        """Test that a user can update bucketlist."""
        res_bucketlist1 = self.client.post('/bucketlist/',data= json.dumps(self.bucketlist),
                                          headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.delete('/bucketlist/1',
                                          headers={'Authorization':'hjbjnbgjksngjvkdfnkj'}
                                          ,content_type="application/json")

        res_message = json.loads(res_bucketlist.data.decode('utf8'))
        self.assertEqual(res_bucketlist.status_code, 401)
        self.assertEqual("Invalid token. Please log in again.",
                         res_message['message'])
    def test_search_non_existent_bucket(self):
        """Test that a user can  add."""
        bucketlist = {
            "name" : "BlackD",
            "description" : "Black don't crack"
        }
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/?q=nothin',headers=self.headers
                                          ,content_type="application/json")

        self.assertEqual(res_bucketlist.status_code, 200)
        self.assertTrue(len(json.loads(res_bucketlist.data)) == 0)

    def test_search_existent_bucket(self):
        """Test that a user can  add."""
        bucketlist = {
            "name" : "BlackD",
            "description" : "Black don't crack"
        }
        res_bucketlist1 = self.client.post('/bucketlist/', data=json.dumps(bucketlist)
                                          ,headers=self.headers
                                          ,content_type="application/json")
        res_bucketlist = self.client.get('/bucketlist/?q=black',headers=self.headers
                                          ,content_type="application/json")

        self.assertEqual(res_bucketlist.status_code, 200)
        self.assertTrue(len(json.loads(res_bucketlist.data)) > 0)


    def tearDown(self):
        db.drop_all()
        self.app_context.pop()





if __name__ == "__main__":
    unittest.main()
