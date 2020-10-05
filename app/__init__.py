from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_bootstrap import Bootstrap
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
admin = Admin(base_template="my_master.html")
login_manager = LoginManager()
mail = Mail()
bootstrap = Bootstrap()


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
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.user_admin import CustomIndexView
    admin.init_app(app, index_view=CustomIndexView.MyAdminIndexView())

    from app.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.downloads import download_blueprint
    app.register_blueprint(download_blueprint)

    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    #CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    @app.route('/')
    def index():
        return 'API is live! - documentation'

    return app


from . import models
import app.user_admin
import app.downloads
