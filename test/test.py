import os
import sys 
import requests
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../src/'))
from database import User, Room, Searcher


class TestDatabase(unittest.TestCase):
    def test_add_user(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        user = User(name="james")
        room.add_user(user)
        self.assertIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_remove_user(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        user = User(name="james")
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_add_user_twice(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        user = User(name="james")
        room.add_user(user)
        room.add_user(user)
        self.assertEqual(
            Room(_id=room._id)._object['users'].count(user._id),
            1
        )

    def test_remove_inexistent_user(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        user = User(name="james")
        room.add_user(user)
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_delete_room(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        room.delete()
        self.assertRaises(Exception,Room(_id=room._id))

    def test_delete_user(self):
        user = User(name="joe")
        user.delete()
        self.assertRaises(Exception,User(_id=user._id))

    def test_draft(self):
        owner = User(name="joe")
        room = Room(owner=owner)
        for name in ['john','carl','james']:
            user = User(name=name)
            room.add_user(user)
        self.assertIn(
            room.draft(),
            Room(_id=room._id)._object['users']
        )


class TestAPI(unittest.TestCase):
    URL = "http://localhost:8000"

    def test_add_user_to_room(self):
        owner_id = requests.post(f"{self.URL}/user/?name={'joe'}").json()['_id']
        room_id = requests.post(f"{self.URL}/room/?owner={owner_id}").json()['_id']
        user_id = requests.post(f"{self.URL}/user/?name={'joel'}").json()['_id']
        requests.put(f"{self.URL}/room/{room_id}/add_user/?user_id={user_id}")
        room_users = requests.get(f"{self.URL}/room/{room_id}").json()['room']['users']
        self.assertIn(
            user_id,
            room_users
        )

    def test_remove_user_from_room(self):
        owner_id = requests.post(f"{self.URL}/user/?name={'joe'}").json()['_id']
        room_id = requests.post(f"{self.URL}/room/?owner={owner_id}").json()['_id']
        user_id = requests.post(f"{self.URL}/user/?name={'joel'}").json()['_id']
        requests.put(f"{self.URL}/room/{room_id}/add_user/?user_id={user_id}")
        requests.put(f"{self.URL}/room/{room_id}/remove_user/?user_id={user_id}")
        room_users = requests.get(f"{self.URL}/room/{room_id}").json()['room']['users']
        self.assertNotIn(
            user_id,
            room_users
        )

    def test_get_deleted_user(self):
        user_id = requests.post(f"{self.URL}/user/?name={'joe'}").json()['_id']
        requests.delete(f"{self.URL}/user/{user_id}")
        self.assertEqual(
            requests.get(f"{self.URL}/user/{user_id}").json()['success'],
            False
        )

    def test_get_deleted_room(self):
        owner_id = requests.post(f"{self.URL}/user/?name={'joe'}").json()['_id']
        room_id = requests.post(f"{self.URL}/room/?owner={owner_id}").json()['_id']
        requests.delete(f"{self.URL}/room/{room_id}")
        response = requests.get(f"{self.URL}/room/{room_id}").json()
        self.assertEqual(
            response['success'],
            False
        )
        self.assertEqual(
            'NoneType' in response['error_message'],
            True
        )


if __name__ == '__main__':
    unittest.main()
