import os
import abc
from random import choice
from pymongo import MongoClient
from bson.objectid import ObjectId


host = os.environ['HOST']
port = int(os.environ['PORT'])

client = MongoClient(host=host,port=port)

db = client['db']
rooms = db['rooms']
users = db['users']


class Document(abc.ABC):
    @property
    @abc.abstractmethod
    def _object(self) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def find(_id):
        pass

    @abc.abstractmethod
    def delete(self) -> None:
        pass


class User(Document):
    def __init__(self, name : str =None, _id : ObjectId =None) -> Document:
        if _id:
            self._id = _id
        else:
            assert name
            result = users.insert_one( { "name": name } )
            self._id = result.inserted_id

    @property
    def _object(self) -> dict:
        return users.find_one({"_id": self._id})

    @staticmethod
    def find(_id: ObjectId) -> dict:
        room = Room(_id=_id)
        if room._object is None:
            raise Exception(f"couldn't find object with id {_id}")
        return room

    def delete(self) -> ObjectId:
        users.delete_one({"_id": self._id })


class Room(Document):
    def __init__(self, owner: User =None, _id: ObjectId =None) -> Document:
        if _id:
            self._id = _id
        else:
            assert owner
            result = rooms.insert_one(
                {
                    "owner": owner._id, 
                    "users": [],
                    "user_objects": {}
                }
            )
            self._id = result.inserted_id

    @property
    def _object(self) -> dict:
        return rooms.find_one({"_id": self._id})

    @staticmethod
    def find(_id: ObjectId) -> Document:
        room = Room(_id=_id)
        if room._object is None:
            raise Exception(f"couldn't find object with id {_id}")
        return room

    def add_user(self,user: User) -> None:
        rooms.update_one(
            { "_id": self._id },
            { "$push": { "users": user._id }, 
              "$set": { f"user_objects.{user._id}": user._object } })

    def remove_user(self,user: User) -> None:
        rooms.update_one(
            { "_id": self._id },
            { "$pull": { "users": user._id }, 
              "$unset": { f"user_objects.{user._id}": user._object } })

    def draft(self) -> ObjectId :
        winner = choice(self._object["users"])
        rooms.update_one(
            { "_id": self._id },
            { "$set": { f"winner": winner } })
        return winner

    def delete(self) -> ObjectId:
        rooms.delete_one({"_id": self._id })


class Searcher:
    @staticmethod
    def room():
        pass

    @staticmethod
    def user():
        pass

