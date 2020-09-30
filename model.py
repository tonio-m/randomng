import os
from pymongo import MongoClient
from bson.objectid import ObjectId


host = os.environ['HOST']
port = int(os.environ['PORT'])

client = MongoClient(host=host,port=port)

db = client['db']
rooms = db['rooms']
users = db['users']


class Room:
    def __init__(self, owner=None, _id=None):
        try:
            if _id is None:
                assert owner is not None

                self.users = []
                self.user_objects = {}
                self.owner = owner._id

                result = rooms.insert_one(
                    {"owner": self.owner, 
                     "users":self.users,
                     "user_objects":self.user_objects}
                )

                self._id = result.inserted_id
                print("created room:",self._id)

            else:
                _id = ObjectId(_id) if type(_id) == str else _id
                _object = rooms.find_one({"_id": _id})
                [setattr(self,k,v) for k,v in _object.items()]

                print("got room:",self._id)
                
        except Exception as e:
            print(e)

    def delete(self):
        try:
            rooms.delete_one({"_id": self._id })
            print("deleted room:",self._id)

        except Exception as e:
            print(e)

    def add_user(self,user):
        try:
            if user._id in self.users:
                print("added user:",user._id,"in",self._id,"already in room")
                return
            myquery = { "_id": ObjectId(self._id) }
            update = { "$push": { "users": user._id } }
            rooms.update_one(myquery, update)
            self.users.append(user._id)
            self.user_objects[user._id] = user._object
            print("added user:",user._id,"to",self._id)
        except Exception as e:
            print(e)

    def remove_user(self,user):
        try:
            myquery = { "_id": ObjectId(self._id) }
            update = { "$pull": { "users": user._id } }
            rooms.update_one(myquery, update)
            self.users.remove(user._id)
            print("removed user:",user._id,"from",self._id)
        except Exception as e:
            print(e)


class User:
    def __init__(self, name=None, _id=None):
        try:
            if _id is None:
                assert name is not None

                self.name = name
                result = users.insert_one(
                    {"name": self.name}
                )

                self._id = result.inserted_id
                self._object = users.find_one({"_id": self._id})
                print("created user:",self._id)

            else:
                _id = ObjectId(_id) if type(_id) == str else _id
                self._object = users.find_one({"_id": _id})
                [setattr(self,k,v) for k,v in self._object.items()]
                print("got user:",self._id)
                

        except Exception as e:
            print(e)

    def delete(self):
        try:
            users.delete_one({"_id": self._id })
            print("deleted user:", self._id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # test

    # user = User(name="bigogerio")
    # room = Room(owner=user)
    # user_id = user._id
    # room_id = room._id
    # print(user_id)
    # print(room_id)

    room = Room(_id="5f72b2cc6512b0fbd5da3a5a")
    user = User(_id="5f72b2cc6512b0fbd5da3a59")
    room.add_user(user)
    print(room.users)

