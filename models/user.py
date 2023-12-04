from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    products = db.relationship('Product', back_populates='user', cascade='all, delete-orphan')
    routines = db.relationship('Routine', back_populates='user', cascade='all, delete-orphan')

class UserSchema(ma.Schema):
    products = fields.Nested('ProductSchema', exclude=['user'], many=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8, error='Invalid Password. Must be at least 8 characters.'))

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'is_admin', 'password', 'products')