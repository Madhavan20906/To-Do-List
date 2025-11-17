# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Use SQLAlchemy 1.4 style engine
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes
@app.get("/api/tasks")
def get_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).order_by(Task.id.desc()).all()
        return jsonify([{"id": t.id, "title": t.title, "description": t.description, "due_date": t.due_date, "done": t.done} for t in tasks])
    finally:
        db.close()

@app.post("/api/tasks")
def add_task():
    db = SessionLocal()
    data = request.get_json()
    new_task = Task(
        title = data.get("title", ""),
        description = data.get("description", ""),
        due_date = data.get("due_date", ""),
        done = bool(data.get("done", False))
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return jsonify({"message":"Task added","id": new_task.id}), 201

@app.put("/api/tasks/<int:id>")
def update_task(id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        db.close()
        return jsonify({"error":"not found"}), 404
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.due_date = data.get("due_date", task.due_date)
    task.done = bool(data.get("done", task.done))
    db.commit()
    db.close()
    return jsonify({"message":"updated"})

@app.delete("/api/tasks/<int:id>")
def delete_task(id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        db.close()
        return jsonify({"error":"not found"}), 404
    db.delete(task)
    db.commit()
    db.close()
    return jsonify({"message":"deleted"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
