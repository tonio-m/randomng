import os
from fastapi import FastAPI
from pymongo import MongoClient

host = os.environ['HOST']
port = os.environ['PORT']

client = MongoClient(host=host,port=port)
db = client["app"]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/room")
async def post_room():
    db["room"].insert(body)
    return {"message": "room was created"}
