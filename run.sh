#!/bin/bash

source .env
APIURL=$APIURL TOKEN=$TOKEN USERPREF_PATH=$USERPREF_PATH python app/andaluhbot.py
