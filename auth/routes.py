from flask import request, jsonify
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token
from . import auth

@auth.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"Auth": "User already exists with same credentials."}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username, hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"Success": "USer registered successfully!"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return ({"Login Error": "Invalid credentials."}), 400
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access token": access_token}), 201

