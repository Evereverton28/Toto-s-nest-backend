#!/usr/bin/env python3

# Remote library imports
from flask import request
from flask_restful import Resource
from flask_cors import CORS  # <== import CORS

# Local imports
from config import app, db, api
from models import User
from resources.auth import Signup, Login, DeleteUser  # <== make sure this file exists

CORS(app)  # <== enable CORS for all routes

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# Add your auth API endpoints
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(DeleteUser, '/delete-user')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
