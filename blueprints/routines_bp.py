from flask import Blueprint, request
from setup import bcrypt, db
# from models.user import User, UserSchema
# from models.product import Product, ProductSchema
from models.routine import Routine, RoutineSchema
from flask_jwt_extended import jwt_required
from auth import admin_required

# Create products blueprint
routines_bp = Blueprint('routines', __name__, url_prefix='/routines')

# Get all products (admin only)
@routines_bp.route('/')
@jwt_required()
def all_routines():
    # Only allow admins to access
    admin_required()
    # Query to select all products in the database
    stmt = db.select(Routine)
    routines = db.session.scalars(stmt).all()
    # Return all products (many)
    return RoutineSchema(many=True, exclude=['user.products', 'user.is_admin']).dump(routines)