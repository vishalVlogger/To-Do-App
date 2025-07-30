from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from ..models import db, Tasks
from functools import wraps
from ..forms import TaskForm

tasks = Blueprint("tasks", __name__)

def login_required(root_func):
    @wraps(root_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access your tasks", "error")
            return redirect(url_for("auth.login"))
        return root_func(*args, **kwargs)
    return wrapper

@tasks.route("/")
@login_required
def dashboard():
    user_id = session.get("user_id")
    status_filter = request.args.get("status", "")  # Get status filter from query param

    if status_filter:
        tasks_list = Tasks.query.filter_by(user_id=user_id, status=status_filter).order_by(Tasks.created_date.desc()).all()
    else:
        tasks_list = Tasks.query.filter_by(user_id=user_id).order_by(Tasks.created_date.desc()).all()

    return render_template("dashboard.html", tasks=tasks_list, status_filter=status_filter)

@tasks.route("/add_tasks", methods=["GET", "POST"])
@login_required
def add_tasks():
    form = TaskForm()

    if form.validate_on_submit():
        new_task = Tasks(
            title=form.title.data,
            content = form.content.data,
            created_date = form.created_date.data,
            status = form.status.data,
            user_id=session.get("user_id")
        )
        db.session.add(new_task)
        db.session.commit()

        flash("Task added successfully", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("add_tasks.html", form=form)

@tasks.route("/edit_tasks/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_tasks(task_id):
    task = Tasks.query.get_or_404(task_id)

    if task.user_id != session.get("user_id"):
        flash("Unauthorized access", "error")
        return redirect(url_for("tasks.dashboard"))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        task.created_date = form.created_date.data
        task.status = form.status.data
        db.session.commit()

        flash("Task updated!", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("edit_tasks.html", form=form, task=task)

@tasks.route("/update_status/<int:task_id>", methods=["POST"])
@login_required
def update_status(task_id):
    task = Tasks.query.get_or_404(task_id)
    if task.user_id != session.get("user_id"):
        flash("Unauthorized", "error")
        return redirect(url_for("tasks.dashboard"))

    new_status = request.form.get("status")
    if new_status in ["Pending", "Working", "Done"]:
        task.status = new_status
        db.session.commit()

        flash("Status Updated", "success")

    return redirect(url_for("tasks.dashboard"))

@tasks.route("/delete_tasks/<int:task_id>")
@login_required
def delete_tasks(task_id):
    task = Tasks.query.get_or_404(task_id)
    if task.user_id != session["user_id"]:
        flash("Unauthorized action", "error")
        return redirect(url_for("tasks.dashboard"))

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted!", "success")
    return redirect(url_for("tasks.dashboard"))

@tasks.route("/toggle/<int:task_id>")
@login_required
def toggle_tasks(task_id):
    task = Tasks.query.get_or_404(task_id)

    # Ensure only the logged-in user's task can be toggled
    if task.user_id != session["user_id"]:
        flash("Unauthorized", "error")
        return redirect(url_for("tasks.dashboard"))

    # Toggle logic
    if task.status == "Pending":
        task.status = "Working"
    elif task.status == "Working":
        task.status = "Done"
    else:
        task.status = "Pending"

    db.session.commit()
    flash("Task status updated!", "info")

    return redirect(url_for("tasks.dashboard"))

@tasks.route("/clear_all")
@login_required
def clear_all():
    user_id = session["user_id"]
    Tasks.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash("All tasks are cleared!", "info")
    return redirect(url_for("tasks.dashboard"))
