from setup import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    products = db.relationship('Product', back_populates='user')

class UserSchema(ma.Schema):
    products = fields.Nested('ProductSchema', exclude=['user'], many=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'is_admin', 'password', 'products')