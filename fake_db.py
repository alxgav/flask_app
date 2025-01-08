from flask import Flask, render_template, request, flash, redirect, url_for

fake_db = [
    {"id": 1, "title": "Task One", "completed": False},
    {"id": 2, "title": "Task Two", "completed": True},
    {"id": 3, "title": "Task Three", "completed": False},
]

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")


@app.route("/")
def home():
    is_all_completed = all(task["completed"] for task in fake_db)
    context = {"tasks": fake_db, "is_all_completed": is_all_completed}
    return render_template("base.html", **context)


@app.route("/add", methods=["POST"])
def create_task():
    title = request.form.get("title", "")
    if title:
        fake_db.append({"id": len(fake_db) + 1, "title": title, "completed": False})
    else:
        flash("Task title is required", "error")
    return redirect(url_for("home"))


@app.route("/update/<int:task_id>")
def update_task(task_id):
    for task in fake_db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    else:
        flash("Task not found", "error")
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    for task in fake_db:
        if task["id"] == task_id:
            fake_db.remove(task)
            break
    else:
        flash("Task not found", "error")
    return redirect(url_for("home"))
