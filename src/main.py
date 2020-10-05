from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from database import User, Room


app = FastAPI()


@app.post("/room/")
async def create_room(owner: str): 
    response = {"success": False}
    try:
        room = Room(owner=owner)
        response["success"] = True
        response["room_id"] = room._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.get("/room/{room_id}")
async def get_room(room_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        response["success"] = True
        response["room"] = room._object
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.delete("/room/{room_id}")
async def delete_room(room_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        room.delete()
        response["success"] = True
        response["room_id"] = room._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.put("/room/{room_id}/add_user")
async def add_user(room_id: str, user_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        user = User(_id=user_id)
        room.add_user(User)
        response["success"] = True
        response["user_id"] = user._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.put("/room/{room_id}/remove_user")
async def remove_user(room_id: str):
    response = {"success": False}
    try:
        room = Room(_id=room_id)
        user = User(_id=user_id)
        room.remove_user(User)
        response["success"] = True
        response["room_id"] = room._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.put("/room/{room_id}/draft")
async def draft(room_id: str):
    #TODO: implement
    return {"message":"not implemented yet"}


@app.post("/user")
async def create_user(name: str):
    response = {"success": False}
    try:
        room = Room(name=name)
        response["success"] = True
        response["user_id"] = user._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    response = {"success": False}
    try:
        user = User(_id=user_id)
        response["success"] = True
        response["user"] = user._object
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.delete("/user/{user_id}")
async def delete_room(user_id: str):
    response = {"success": False}
    try:
        user = User(_id=user_id)
        user.delete()
        response["success"] = True
        response["user_id"] = user._id
    except Exception as e:
        response["error_message"] = e.message
    return response


@app.get("/search/room")
async def search_room(query: str):
    #TODO: implement
    return {"message":"not implemented yet"}


@app.get("/search/user")
async def search_user(query: str):
    #TODO: implement
    return {"message":"not implemented yet"}


