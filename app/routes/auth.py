from flask import Blueprint, render_template, session ,redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import db, User
from ..forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already register", "error")
            return redirect(url_for("auth.register"))

        hashed_pass = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successfully, Please log in", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session["user_id"] = user.id
            session["email"] = user.email

            flash("Login Successfully", "success")
            return redirect(url_for("tasks.dashboard"))
        else:
            flash("Invalid Credentials", "error")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)

@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("email", None)
    flash("Logout Successfully", "info")
    return redirect(url_for("auth.login"))



