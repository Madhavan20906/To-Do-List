from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------
# Database Model
# ---------------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(String)
    done = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# ---------------------
# Helper: DB Session
# ---------------------
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# ---------------------
# ROUTES
# ---------------------

@app.get("/tasks")
def get_tasks():
    db = get_db()
    tasks = db.query(Task).all()

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
    db = get_db()
    data = request.json

    new_task = Task(
        title=data["title"],
        description=data.get("description", ""),
        due_date=data.get("due_date", ""),
        done=data.get("done", False)
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return jsonify({"message": "Task added", "id": new_task.id})


@app.put("/tasks/<int:id>")
def update_task(id):
    db = get_db()
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.due_date = data.get("due_date", task.due_date)
    task.done = data.get("done", task.done)

    db.commit()
    return jsonify({"message": "Task updated"})


@app.delete("/tasks/<int:id>")
def delete_task(id):
    db = get_db()
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.delete(task)
    db.commit()

    return jsonify({"message": "Task deleted"})


# ---------------------
# RUN APP
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)
