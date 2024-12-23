from os import abort
from flask import Flask, jsonify, request
from main.models import Base, engine, session, Task
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world"


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route(
    "/tasks",
    methods=[
        "GET",
    ],
)
def get_all_tasks():
    """
    Getting a list of all tasks.
    """
    tasks = session.query(Task).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append(task.to_json())
    session.close()
    return jsonify(tasks_list=tasks_list), 200


@app.route(
    "/task/<int:id>",
    methods=[
        "GET",
    ],
)
def get_task(id):
    """
    Getting a task by its ID number.
    :param id:
    :return:
    """
    task = session.query(Task).filter(Task.id == id).one_or_none()
    if task is None:
        abort(404)
    return jsonify(task=task.to_json()), 200


@app.route("/add_task", methods=["POST"])
def add_task():
    """
    Adding a new task.
    :return:
    """
    title = request.form.get("title", type=str)
    description = request.form.get("description", type=str)
    status = request.form.get("status", type=str)
    created_at = datetime.strptime(request.form.get("created_at"), "%Y-%m-%d")
    updated_at = datetime.strptime(request.form.get("updated_at"), "%Y-%m-%d")
    new_task = Task(
        title=title,
        description=description,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
    )
    session.add(new_task)
    session.commit()
    return f"The task record {title} has been created successfully.", 201


@app.route(
    "/task/<int:id>",
    methods=[
        "DELETE",
    ],
)
def delete_task(id):
    """
    Deleting a task by its ID number.
    :param id:
    :return:
    """
    session.query(Task).filter(Task.id == id).delete()
    session.commit()
    return f"Task {id} successfully deleted", 200


@app.route(
    "/task/<int:id>",
    methods=[
        "PUT",
    ],
)
def update_task(id):
    """
    Updating a task by its ID number.
    :param id:
    :return:
    """
    title = request.form.get("title", type=str)
    description = request.form.get("description", type=str)
    status = request.form.get("status", type=str)
    created_at = request.form.get("created_at", type=datetime)
    updated_at = request.form.get("updated_at", type=datetime)

    task = session.query(Task).filter(Task.id == id).one_or_none()
    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status
    if created_at:
        task.created_at = created_at
    if updated_at:
        task.updated_at = updated_at
    session.commit()

    return f"Task {id} updated successfully", 200


if __name__ == "__main__":
    app.run()
