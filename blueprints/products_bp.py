from flask import Blueprint, request, abort
from setup import db
from models.product import Product, ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_required, authorize


# Create products_bp blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')


#----------------------------------------------------------------
# GET ALL PRODUCTS (Global - Admin Only)

@products_bp.route('/')
@jwt_required()
def all_products():

    # Abort if user is not an admin
    if not admin_required():
        abort(401)

    # Query to select all products in the database
    stmt = db.select(Product)
    products = db.session.scalars(stmt).all()

    # Return all products (many)
    return ProductSchema(exclude=['user.is_admin', ], many=True).dump(products)


#----------------------------------------------------------------
# CREATE A PRODUCT

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

    return ProductSchema(exclude=['user']).dump(product), 201


#----------------------------------------------------------------
# GET USER PRODUCTS

@products_bp.route('/<int:user_id>')
@jwt_required()
def user_products(user_id):
    current_user_id = get_jwt_identity()

    # Check if the current user is the same as the request user or an admin
    if current_user_id == user_id or admin_required():

        stmt=db.select(Product).where(Product.user_id == user_id)
        user_products=db.session.scalars(stmt).all()

        return ProductSchema(exclude=['user', 'user.products'], many=True).dump(user_products)
    else:
        abort(401)


#----------------------------------------------------------------
# UPDATE A PRODUCT

@products_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):

    # Parse the product body through the ProductSchema
    product_info = ProductSchema(exclude=['id'], partial=True).load(request.json)

    # Find the product based on the matching product_id that was provided in the request
    stmt = db.select(Product).where(Product.id == id)
    product = db.session.scalar(stmt)

    # Check product that matched was successfully found
    if product:
        # User can only update a product that they created (unless they're an Admin)
        authorize(product.user_id)
        # Conditionally update fields if present
        if 'name' in product_info:
            product.name = product_info['name']
        if 'brand' in product_info:
            product.brand = product_info['brand']
        if 'notes' in product_info:
            product.notes = product_info['notes']
    
        db.session.commit()
        return ProductSchema(exclude=['user', 'user.products']).dump(product), 200
    
    else:
	    return {'Error': 'Product not found'}, 404


#----------------------------------------------------------------
# DELETE A PRODUCT

@products_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):

    # Find the product based on the matching product_id that was provided in the request
    stmt = db.select(Product).where(Product.id == id)
    product = db.session.scalar(stmt)

    # Check product that matched was successfully found
    if product:
        # User can only delete a product that they created (unless they're an Admin)
        authorize(product.user_id)
        db.session.delete(product)
        db.session.commit()
        return {'Message': 'Product has been successfully deleted'}, 200
    
    else:
	    return {'Error': 'Product not found'}, 404