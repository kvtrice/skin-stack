from setup import db, ma

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text())
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('User', back_populates='products')

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'brand', 'notes', 'user_id')
