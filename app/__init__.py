from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SECRET_KEY'] = 'todoapp123'

    db.init_app(app)

    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.tasks import tasks as tasks_blueprint
    app.register_blueprint(tasks_blueprint)

    with app.app_context():
        db.create_all()

    return app