from setup import db, ma
from marshmallow import fields

class Product(db.Model):
    __tablename__ = 'routine_products'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', back_populates='routine_products')

    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=False)
    routine = db.relationship('Routine', back_populates='routine_products')


class RoutineProductSchema(ma.Schema):
    product = fields.Nested('ProductSchema')
    routine = fields.Nested('RoutineSchema')

    class Meta:
        fields = ('id', 'routine', 'product')
