from flask import request
from flask_restful import Resource
from models import User
from config import db

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {"message": "Missing username, email or password"}, 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"message": "User already exists"}, 400

        new_user = User(username=username, email=email)
        new_user.password = password  # This will hash the password
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        login_input = data.get('login')  # can be username or email
        password = data.get('password')

        if not login_input or not password:
            return {"message": "Missing login or password"}, 400

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if user and user.authenticate(password):
            return {
                "message": "Login successful",
                "user": {"id": user.id, "username": user.username, "email": user.email}
            }, 200
        else:
            return {"message": "Invalid credentials"}, 401

class DeleteUser(Resource):
    def delete(self):
        data = request.get_json()
        login_input = data.get('login')  # can be username or email

        if not login_input:
            return {"message": "Missing login"}, 400

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": f"User '{login_input}' deleted successfully."}, 200
