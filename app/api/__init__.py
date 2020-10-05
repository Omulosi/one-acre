from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint('one-acre', __name__)
api = Api(api_blueprint)

from .farms import FarmAPI
from .auth import SignUP, SignIn, RefreshToken, ResetPassword
from .tokens import Tokens
from .users import Users
from .funded_farms import FundedFarmAPI

# routes for farm resource
api.add_resource(FarmAPI,
                 '/farms',
                 '/farms/<id>',
                 '/farms/<id>/<field>',
                 endpoint='farm')
# Authenticaion routes
api.add_resource(
    SignUP,
    '/auth/register',
)

api.add_resource(
    SignIn,
    '/auth/login',
)

api.add_resource(
    RefreshToken,
    '/auth/refresh',
)

api.add_resource(ResetPassword, '/auth/reset')

api.add_resource(Tokens, '/auth/tokens', '/auth/tokens/<token_id>')

# users
api.add_resource(Users,
                 '/users',
                 '/users/<id>',
                 '/users/<id>/<field>',
                 endpoint='users')

# Funded farm

api.add_resource(
    FundedFarmAPI,
    '/funded_farms',
    '/funded_farms/<id>',
    '/funded_farms/<id>/<field>',
)
