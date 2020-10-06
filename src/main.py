from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .database import User, Room

app = FastAPI()

@app.put("/room/{room_id}/add_user")
async def add_user(room_id: str, user_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        user = User(_id=user_id)
        room.add_user(user)
        response["success"] = True
        response["_id"] = user._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.put("/room/{room_id}/remove_user")
async def remove_user(room_id: str, user_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        user = User(_id=user_id)
        room.remove_user(user)
        response["success"] = True
        response["_id"] = room._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.delete("/room/{room_id}")
async def delete_room(room_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        room.delete()
        response["success"] = True
        response["_id"] = room._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.delete("/user/{user_id}")
async def delete_room(user_id: str):
    response = {"success": False}
    try:
        user = User(_id=user_id)
        user.delete()
        response["success"] = True
        response["_id"] = user._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.post("/room/")
async def create_room(owner: str): 
    response = {"success": False}
    try:
        owner = User(_id=owner)
        room = Room(owner=owner)
        response["success"] = True
        response["_id"] = room._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.get("/room/{room_id}")
async def get_room(room_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        _object = room._object
        _object['_id'] = str(_object['_id'])
        _object['users'] = [str(u) for u in _object['users']]
        _object['owner'] = str(_object['owner'])
        for k,v in _object['user_objects'].items():
            v['_id'] = str(v['_id'])
            _object['user_objects'][k] = v
        response["room"] = _object
        response["success"] = True
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.post("/user")
async def create_user(name: str):
    response = {"success": False}
    try:
        user = User(name=name)
        response["success"] = True
        response["_id"] = user._id
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    response = {"success": False}
    try:
        user = User(_id=user_id)
        _object = user._object
        _object['_id'] = str(_object['_id'])
        response["user"] = _object
        response["success"] = True
    except Exception as e:
        response["error_message"] = getattr(e, 'message', repr(e))
    return response

@app.get("/search/room")
async def search_room(query: str):
    #TODO: implement
    return {"message":"not implemented yet"}

@app.get("/search/user")
async def search_user(query: str):
    #TODO: implement
    return {"message":"not implemented yet"}

@app.put("/room/{room_id}/draft")
async def draft(room_id: str):
    #TODO: implement
    return {"message":"not implemented yet"}
