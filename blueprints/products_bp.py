from flask import Blueprint, request
from setup import bcrypt, db
from models.users import User, UserSchema
from models.products import Product, ProductSchema
from flask_jwt_extended import jwt_required
from auth import admin_required

# Create products blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

# Get all products (admin only)
@products_bp.route('/')
@jwt_required()
def all_products():
    # Only allow admins to access
    admin_required()
    # Query to select all products in the database
    stmt = db.select(Product)
    products = db.session.scalars(stmt).all()
    # Return all products (many)
    return ProductSchema(many=True, exclude=['user.products']).dump(products)

