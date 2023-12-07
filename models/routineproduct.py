from setup import db, ma
from marshmallow import fields

class RoutineProduct(db.Model):
    __tablename__ = 'routine_products'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product = db.relationship('Product', back_populates='routines')

    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id', ondelete='CASCADE'), nullable=False)
    routine = db.relationship('Routine', back_populates='routine_products')


class RoutineProductSchema(ma.Schema):
    product = fields.Nested('ProductSchema')

    class Meta:
        fields = ('id', 'routine_id', 'product_id', 'product')
