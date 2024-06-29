from flask import request, jsonify
from extensions import db, jwt
from models import Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import task

@task.route("/get", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_list = [{
        "id": task.id, 
        "title": task.title, 
        "description": task.description,
        "category": task.category,
        "status": task.status,
        "date": task.date
        } for task in tasks]
    return jsonify(tasks_list), 200

@task.route("/get/<int:id>", methods=["GET"])
@jwt_required()
def fetch_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    serialized_task = {
        "id": task.id, 
        "title": task.title, 
        "description": task.description,
        "category": task.category, 
        "status": task.status, 
        "date": task.date
    }
    return jsonify({"task": serialized_task}), 200

@task.route("/add", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    status = 0
    new_task = Task(user_id=user_id, title=title, description=description, category=category, status=status)
    serialized_new_task = {
        "title": new_task.title, 
        "description": new_task.description,
        "category": new_task.category, 
        "status": new_task.status
    }
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"Insertion": "Task added successfully", "Task": serialized_new_task}), 201

@task.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def modify_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    task.title = data.get("title")
    task.description = data.get("description")
    task.category = data.get("category")
    task.status = data.get("status")
    serialized_task = {
        "id": task.id, 
        "title": task.title, 
        "description": task.description,
        "category": task.category, 
        "status": task.status, 
        "date": task.date
    }
    db.session.commit()
    return jsonify({"Updation": "Task updated successfully", "Task": serialized_task}), 200

@task.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"Deletion": "Task deleted successfully"}), 200

