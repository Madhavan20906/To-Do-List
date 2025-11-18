from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# ------------------ ROUTES ------------------

@app.get("/tasks")
def get_tasks():
    tasks = session.query(Task).all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "due_date": t.due_date,
            "done": t.done
        } for t in tasks
    ])

@app.post("/tasks")
def add_task():
    data = request.json
    new_task = Task(
        title=data["title"],
        description=data["description"],
        due_date=data["due_date"],
        done=data.get("done", False)
    )
    session.add(new_task)
    session.commit()
    return jsonify({"message": "Task added"}), 201

@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.json
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.title = data["title"]
    task.description = data["description"]
    task.due_date = data["due_date"]
    task.done = data["done"]
    session.commit()

    return jsonify({"message": "Task updated"})

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    session.delete(task)
    session.commit()
    return jsonify({"message": "Task deleted"})

@app.get("/")
def home():
    return "Task API is running!"

if __name__ == "__main__":
    app.run()
