from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import os

app = Flask(__name__)
CORS(app)

# USE NEON DATABASE URL FROM RENDER ENVIRONMENT
DATABASE_URL = os.environ.get("DATABASE_URL")

# The most important part for NEON + Render stability
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,            # Auto reconnect if DB sleeps
    connect_args={"sslmode": "require"}  # Required for Neon SSL
)

# Safe session handling
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(String)
    done = Column(Boolean, default=False)


# Create tables
Base.metadata.create_all(engine)


@app.get("/tasks")
def get_tasks():
    session = Session()
    try:
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
    finally:
        session.close()


@app.post("/tasks")
def add_task():
    session = Session()
    try:
        data = request.json
        new_task = Task(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            done=data.get("done", False)
        )
        session.add(new_task)
        session.commit()
        return jsonify({"message": "Task added"}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    session = Session()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        data = request.json
        task.title = data["title"]
        task.description = data["description"]
        task.due_date = data["due_date"]
        task.done = data["done"]

        session.commit()
        return jsonify({"message": "Task updated"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    session = Session()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        session.delete(task)
        session.commit()
        return jsonify({"message": "Task deleted"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@app.get("/")
def home():
    return "Task API is running with Neon PostgreSQL!"


if __name__ == "__main__":
    app.run()
