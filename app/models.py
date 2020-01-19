from datetime import datetime
from . import db, bcrypt


class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    bank_name = db.Column(db.String(64), default='')
    role = db.Column(db.String(64), default='')
    admin = db.Column(db.Boolean, default=False)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bank_account_num = db.Column(db.String(64), default='')
    bank_account_name = db.Column(db.String(64), default='')
    farms = db.relationship('Farm', backref='person', lazy='dynamic')
    funded_farms = db.relationship('FundedFarm', backref='person', lazy='dynamic')
    confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        return {'id': self.id,
                'email': self.email,
                'role': self.role,
                'createdon': self.createdon.strftime('%a, %d %b %Y'),
                'bank_name': self.bank_name,
                'bank_account_num': self.bank_account_num,
                'bank_account_name': self.bank_account_name,
                'confirmed': self.confirmed,
                'admin': self.admin
                }


    def __repr__(self):
        return '<User {}>'.format(self.email)


class Farm(db.Model):

    __tablename__ = 'farm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    stage = db.Column(db.String(64), default="closed") # open/closed
    start_date = db.Column(db.DateTime) # year, month, day
    duration = db.Column(db.String(300))
    location = db.Column(db.String(300))
    units = db.Column(db.Integer) # No of units in the farm
    margin = db.Column(db.Float) # Expected profit margin
    price = db.Column(db.Float) # price per unit
    active = db.Column(db.Boolean, default=False) # operates when active only
    status = db.Column(db.String(64)) # Funding status (pending/confirmed)
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def serialize(self):

        return {'id': self.id,
                'name': self.name,
                'location': self.location,
                'units': self.units,
                'price': self.price,
                'active': self.active,
                'start_date': self.start_date and self.start_date.strftime('%a, %d %b %Y'),
                'margin': self.margin,
                'duration': self.duration,
                'stage': self.stage,
                'description': self.description,
                'createdon': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
                'createdby': self.user_id,
                'status': self.status
                }

    def __repr__(self):
        return '<Farm {}>'.format(self.farm_name)

class FundedFarm(db.Model):

    __tablename__ = 'funded_farm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    createdon = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(64), default="inactive") #pending/confirmed
    amount = db.Column(db.Float) # amount paid for this farm
    units = db.Column(db.Integer) # No of units paid for
    payout = db.Column(db.Float); # expected payout
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    farm_id = db.Column(db.Integer)

    @property
    def serialize(self):

        return {'id': self.id,
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
        return '<Funded Farm {}>'.format(self.name)


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
