#!/bin/bash

export HOST=localhost
export PORT=27017

if [ "$(docker ps -a | grep randomng-mongo)" ]; then
    docker start randomng-mongo
else
    docker run --name randomng-mongo -p 27017:27017 -d mongo
fi

uvicorn main:app --reload
