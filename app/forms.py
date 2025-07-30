from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField, DateField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=8 ,max=30)])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=5)])
    confirm_password = PasswordField("Confirm Password", validators=[
        InputRequired(),
        EqualTo('password', message="Password must be match")
    ])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Description", validators=[InputRequired(), Length(max=255)])
    created_date = DateField("Date", validators=[InputRequired()])
    status = SelectField("Status", choices=[("Pending", "Pending"), ("Working", "Working"), ("Done", "Done")])
    submit = SubmitField("Save Task")
