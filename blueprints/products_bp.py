from flask import Blueprint, request, abort
from setup import bcrypt, db
from models.user import User, UserSchema
from models.product import Product, ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_required, authorize
from marshmallow.exceptions import ValidationError

# Create products_bp blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

# Get all global products (admin only)
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

# Get a list of all user's own products
@products_bp.route('/<int:user_id>')
@jwt_required()
def all_user_products(user_id):
    current_user_id = get_jwt_identity()

    # Check if the current user is the same as the request user or an admin
    if current_user_id == user_id or admin_required():

        stmt=db.select(Product).where(Product.user_id == user_id)
        user_products=db.session.scalars(stmt).all()

        return ProductSchema(exclude=['user', 'user.products'], many=True).dump(user_products)

    else:
        abort(401)


# Create a new Product
@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    # Parse the product body through the ProductSchema
    product_info = ProductSchema(exclude=['id', 'user']).load(request.json)

    # Create the product
    product = Product(
        name=product_info.get('name'),
        brand=product_info.get('brand'),
        notes=product_info.get('notes', ''),
        user_id=get_jwt_identity() # Assign user_id to the product
    )

    # Add & Commit the new product to the database
    db.session.add(product)
    db.session.commit()

    return ProductSchema().dump(product), 201