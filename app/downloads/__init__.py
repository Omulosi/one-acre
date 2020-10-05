from flask import Blueprint

download_blueprint = Blueprint('downloads', __name__)

from app.downloads import views
