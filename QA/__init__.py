import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'


def create_app(env_name=os.environ.get('env', 'dev')):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    with app.app_context():
        from QA.User.routes import user_blueprint
        from QA.Question.routes import question_blueprint
        app.register_blueprint(user_blueprint, url_prefix='/user')
        app.register_blueprint(question_blueprint)

        db.create_all()

        return app
