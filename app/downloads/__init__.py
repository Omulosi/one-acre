from flask import Blueprint

bp = Blueprint('downloads', __name__)

from app.downloads import views
