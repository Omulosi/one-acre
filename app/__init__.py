from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_admin import Admin
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
admin = Admin()


def create_app(config=Config):
    """Create the application instance"""

    # config files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)

    from app.api import bp
    app.register_blueprint(bp, url_prefix='/api')

    #CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    @app.route('/')
    def index():
        return 'API is live! - documentation'

    return app

from . import models
import app.user_admin
