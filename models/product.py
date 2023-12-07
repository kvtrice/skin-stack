from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='products')
    
    routines = db.relationship('RoutineProduct', back_populates='product')


class ProductSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password'])
    name = fields.String(required=True, validate=Length(min=2, error='Product name must be at least 2 characters.'))
    brand = fields.String(required=True, validate=Length(min=2, error='Brand name must be at least 2 characters.'))

    class Meta:
        fields = ('id', 'user', 'name', 'brand', 'notes')
