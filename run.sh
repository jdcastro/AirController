#!/bin/bash
cd app
export FLASK_APP=__init__.py
export FLASK_DEBUG=1 
export TEMPLATES_AUTO_RELOAD=1 
# export SERVER_NAME=airc.jdcastro.co
# flask run --host=0.0.0.0 --port=8080
flask run