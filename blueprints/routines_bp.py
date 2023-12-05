from flask import Blueprint, request, abort
from setup import db
from models.user import User, UserSchema
from models.product import Product, ProductSchema
from models.routine import Routine, RoutineSchema
from models.routineproduct import RoutineProduct
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_required
from sqlalchemy.orm import selectinload

# Create routine blueprint
routines_bp = Blueprint('routines', __name__, url_prefix='/routines')

# Get all routines (admin only)
@routines_bp.route('/')
@jwt_required()
def all_routines():
    # Abort if user is not an admin
    if not admin_required():
        abort(401)
    # Query to select all routines in the database
    stmt = db.select(Routine)
    routines = db.session.scalars(stmt).all()
    # Return all routines (many)
    return RoutineSchema(many=True, exclude=['user.products', 'user.is_admin']).dump(routines)


# Create a new Routine
@routines_bp.route('/', methods=['POST'])
@jwt_required()
def create_routine():
    routine_info = RoutineSchema(exclude=['id']).load(request.json)
    
    # Extract the routine details first
    day_of_week=routine_info.get('day_of_week')
    time_of_day=routine_info.get('time_of_day'),
    user_id=get_jwt_identity()

    # Check if there's already an existing routine matching these details
    existing_routine = Routine.query.filter_by(
        day_of_week=day_of_week,
        time_of_day=time_of_day,
        user_id=user_id
    ).first()

    if existing_routine:
        return {'Error': 'Duplicate routine already exists!'}, 400

    # Otherwise continue to create the routine
    routine = Routine(
        day_of_week=day_of_week,
        time_of_day=time_of_day,
        user_id=user_id
    )
    # Add & Commit the new routine to the database
    db.session.add(routine)
    db.session.commit()
    return RoutineSchema().dump(routine), 201


# Get a list of a user's routines and associated products
@routines_bp.route('/<int:user_id>')
@jwt_required()
def user_routines(user_id):
    current_user_id = get_jwt_identity()
    # Check if the current user is the same as the request user or an admin
    if current_user_id == user_id or admin_required():

        stmt = db.select(Routine).where(Routine.user_id == user_id)
        user_routines = db.session.scalars(stmt).all()

        return RoutineSchema(exclude=['routine_products.routine_id', 'routine_products.product.user', 'routine_products.product_id', 'user_id', 'routine_products.id'], many=True).dump(user_routines)
    else:
        abort(401)
