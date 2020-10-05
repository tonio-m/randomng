#!/bin/sh

export HOST=localhost
export PORT=27017

if [ "$(docker ps -a | grep randomng-mongo)" ]; then
    docker start randomng-mongo
else
    docker run --name randomng-mongo -p 27017:27017 -d mongo
fi

if [ "$(netstat -tulpn | grep LISTEN | grep 127.0.0.1:8000)" ]; then
    :
else
    uvicorn src.main:app --reload &
fi

./venv/bin/python src/test/test.py
