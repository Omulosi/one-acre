from flask_admin.contrib.sqla import ModelView
from . import admin
from . import db

from .models import User, Farm, FundedFarm

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Farm, db.session))
admin.add_view(ModelView(FundedFarm, db.session))

print("Run file")
