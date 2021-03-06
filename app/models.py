from datetime import datetime
from sqlalchemy_utils.types.choice import ChoiceType
from flask_login import UserMixin
import jwt
from time import time
from sqlalchemy.orm import backref
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, bcrypt, login_manager
from flask import current_app


class User(UserMixin, db.Model):

    ROLE = [('0', 'Funder'), ('1', 'Farmer')]

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), default='')
    last_name = db.Column(db.String(128), default='')
    id_num = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    bank_name = db.Column(db.String(64), default='')
    role = db.Column(ChoiceType(ROLE), default='')  # 0 or 1
    admin = db.Column(db.Boolean, default=False)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bank_account_num = db.Column(db.String(64), default='')
    bank_account_name = db.Column(db.String(64), default='')
    # farms = db.relationship('Farm', backref='person', lazy='dynamic')
    # funded_farms = db.relationship('FundedFarm', backref='person', lazy='dynamic')
    confirmed = db.Column(db.Boolean, default=False)  # email-confirmed

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.admin

    @property
    def serialize(self):
        role = self.role.code if self.role else ''
        return {
            'id': self.id,
            'email': self.email,
            'role': role,
            'createdon': self.createdon.strftime('%a, %d %b %Y'),
            'bank_name': self.bank_name,
            'bank_account_num': self.bank_account_num,
            'bank_account_name': self.bank_account_name,
            'confirmed': self.confirmed,
            'admin': self.admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'id_num': self.id_num
        }

    def get_activate_token(self, expires_in=6000):
        return jwt.encode({
            'activate': self.id,
            'exp': time() + expires_in
        },
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_activate_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activate']
        except:
            return
        return User.query.get(id)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.set_password(new_password)
        db.session.add(user)
        return True

    def __repr__(self):
        return '<{}>'.format(self.email)


class Farm(db.Model):

    STAGE = [('open', 'open'), ('closed', 'closed')]

    __tablename__ = 'farm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    stage = db.Column(ChoiceType(STAGE), default="closed")  # open/closed
    start_date = db.Column(db.DateTime)  # year, month, day
    duration = db.Column(db.String(300))
    location = db.Column(db.String(300))
    units = db.Column(db.Integer)  # No of units in the farm
    margin = db.Column(db.Float)  # Expected profit margin
    price = db.Column(db.Float)  # price per unit
    active = db.Column(db.Boolean, default=False)  # operates when active only
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    farmer = db.relationship(User,
                             foreign_keys=[user_id],
                             backref=backref("farms", cascade="all, delete"))

    @property
    def serialize(self):
        stage = self.stage.code if self.stage else ''
        return {
            'id':
            self.id,
            'name':
            self.name,
            'location':
            self.location,
            'units':
            self.units,
            'price':
            self.price,
            'active':
            self.active,
            'start_date':
            self.start_date and self.start_date.strftime('%a, %d %b %Y'),
            'margin':
            self.margin,
            'duration':
            self.duration,
            'stage':
            stage,
            'description':
            self.description,
            'createdon':
            self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
            'createdby':
            self.user_id,
        }

    def __repr__(self):
        return '<{}>'.format(self.name)


class FundedFarm(db.Model):

    STATUS = [('pending', 'pending'), ('confirmed', 'confirmed')]

    __tablename__ = 'funded_farm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(ChoiceType(STATUS))  #pending/confirmed
    # status = db.Column(db.String(64), default="") #pending/confirmed
    amount = db.Column(db.Float)  # amount paid for this farm
    units = db.Column(db.Integer)  # No of units paid for
    payout = db.Column(db.Float)
    # expected payout
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    funder = db.relationship(User,
                             foreign_keys=[user_id],
                             backref=backref("funded_farms",
                                             cascade="all, delete"))
    farm_id = db.Column(db.Integer)

    @property
    def serialize(self):
        status = self.status.code if self.status else ''

        return {
            'id': self.id,
            'name': self.name,
            'funded_on': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
            'status': self.status,
            'funded_by': self.user_id,
            'amount': self.amount,
            'units': self.units,
            'payout': self.payout,
            'farm_id': self.farm_id
        }

    def __repr__(self):
        return '<{}>'.format(self.name)


class TokenBlacklist(db.Model):

    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    @property
    def serialize(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires.strftime('%a, %d %b %Y %H:%M %p')
        }


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
