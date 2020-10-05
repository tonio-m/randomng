import sys 
import requests
import unittest
sys.path.insert(0,'..')
from .database import User, Room, Searcher


class TestDatabase(unittest.TestCase):

    def test_add_user(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        self.assertIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_remove_user(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_add_user_twice(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        room.add_user(user)
        self.assertEqual(
            Room(_id=room._id)._object['users'].count(user._id),
            1
        )

    def test_remove_inexistent_user(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_delete_room(self):
        owner = User(name=name)
        room = Room(owner=owner)
        room.delete()
        self.assertRaises(Exception,Room(_id=room._id))

    def test_delete_user(self):
        user = User(name=name)
        user.delete()
        self.assertRaises(Exception,User(_id=user._id))

    def test_draft(self):
        owner = User(name=name)
        room = Room(owner=owner)
        for name in ['john','carl','james']:
            user = User(name=name)
            room.add_user(user)
        self.assertIn(
            room.draft(),
            Room(_id=room._id)._object['users']
        )

    def test_search_room(self):
        owner = User(name=name)
        room = Room(owner=owner)
        self.assertGreater(
            Searcher.search_room(room._id[:4]),
            0
        )

    def test_search_user(self):
        user = User(name=name)
        self.assertGreater(
            Searcher.search_user(user._id[:4]),
            0
        )

class TestAPI(unittest.TestCase):

    URL = "https://localhost:8000"
    def test_add_user(self):
        owner = requests.post(f"{self.URL}/user/?name={name}").json()

        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        self.assertIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_remove_user(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_add_user_twice(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        room.add_user(user)
        self.assertEqual(
            Room(_id=room._id)._object['users'].count(user._id),
            1
        )

    def test_remove_inexistent_user(self):
        owner = User(name=name)
        room = Room(owner=owner)
        user = User(name=name)
        room.add_user(user)
        room.remove_user(user)
        self.assertNotIn(
            user._id,
            Room(_id=room._id)._object['users']
        )

    def test_delete_room(self):
        owner = User(name=name)
        room = Room(owner=owner)
        room.delete()
        self.assertRaises(Exception,Room(_id=room._id))

    def test_delete_user(self):
        user = User(name=name)
        user.delete()
        self.assertRaises(Exception,User(_id=user._id))

    def test_draft(self):
        owner = User(name=name)
        room = Room(owner=owner)
        for name in ['john','carl','james']:
            user = User(name=name)
            room.add_user(user)
        self.assertIn(
            room.draft(),
            Room(_id=room._id)._object['users']
        )

    def test_search_room(self):
        owner = User(name=name)
        room = Room(owner=owner)
        self.assertGreater(
            Searcher.search_room(room._id[:4]),
            0
        )

    def test_search_user(self):
        user = User(name=name)
        self.assertGreater(
            Searcher.search_user(user._id[:4]),
            0
        )


if __name__ == '__main__':
    unittest.main()

    # # room
    """
        requests.get(f"{URL}/room/{room_id}")
        requests.post(f"{URL}/room/?owner={user_id}")
        requests.delete(f"{URL}/room/{room_id}")
        requests.put(f"{URL}/room/{room_id}/add_user/?user_id={user_id}")
        requests.put(f"{URL}/room/{room_id}/remove_user/?user_id={user_id}")
        requests.put(f"{URL}/room/{room_id}/draft")
    """
    # # user
    """
        requests.get(f"{URL}/user/{user_id}")
        requests.post(f"{URL}/user/?name=joe")
        requests.delete(f"{URL}/user/{user_id}")
    """
    # # search
    """
        requests.get("{URL}/search/room/?query={query}")
        requests.get("{URL}/search/user/?query={query}")
    """
    # # room
    """
        Room.find(room_id)
        Room(owner=owner)
        room.delete()
        room.add_user(user)
        room.remove_user(user)
        room.draft()
    """
    # # user
    """
        User.find(user_id)
        User(name=name)
        user.delete()
    """
    # # search
    """
        Searcher.room(query)
        Searcher.user(query)
    """
