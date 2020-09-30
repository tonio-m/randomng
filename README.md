# Randomng

A trustworthy and transparent platform for giveaways and "gambling". 

## Purpose

Random number picker with money involved


this is supposed to be a reliable true rng like random.org, but with money involved.


this is the mvp im trying to build:


a backend api with:
- a user/room system
- a mock random picker for users in the room


the idea on the long term is to have a eth smart contract randomly selecting the user and giving the reward previously stipulated by room rules

## Design

- fastapi backend
- use parse-server as a "backend for the backend" (updating the database and all that)
- use a smart contract binding the user and the room to generate the number and give the reward
- a nice, minimalist front-end
