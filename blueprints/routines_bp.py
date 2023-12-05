from flask import Blueprint, request, abort
from setup import db
from models.user import User, UserSchema
from models.product import Product, ProductSchema
from models.routine import Routine, RoutineSchema
from models.routineproduct import RoutineProduct
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_required, authorize


# Create routine blueprint
routines_bp = Blueprint('routines', __name__, url_prefix='/routines')


#----------------------------------------------------------------
# GET ALL ROUTINES (Global - Admin Only)

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
    return RoutineSchema(many=True, exclude=['routine_products.routine_id', 'routine_products.product.user', 'routine_products.product_id']).dump(routines)


#----------------------------------------------------------------
# CREATE A ROUTINE

@routines_bp.route('/', methods=['POST'])
@jwt_required()
def create_routine():
    routine_info = RoutineSchema(exclude=['id']).load(request.json)

    # Extract the routine details first
    day_of_week=routine_info.get('day_of_week')
    time_of_day=routine_info.get('time_of_day')
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


#----------------------------------------------------------------
# GET USER ROUTINES & ASSOCIATED PRODUCTS

@routines_bp.route('/<int:user_id>')
@jwt_required()
def user_routines(user_id):
    current_user_id = get_jwt_identity()

    # Check if the current user is the same as the request user or an admin
    if current_user_id == user_id or admin_required():

        # Select the routines for the current user
        stmt = db.select(Routine).where(Routine.user_id == user_id)
        user_routines = db.session.scalars(stmt).all()

        return RoutineSchema(exclude=['routine_products.routine_id', 'routine_products.product.user', 'routine_products.product_id', 'user_id', 'routine_products.id'], many=True).dump(user_routines)
    
    # If current user not matching route user_id or user is not an admin -> abort
    else:
        abort(401)


#----------------------------------------------------------------
# DELETE A ROUTINE

@routines_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_routine(id):

    # Find the routine based on the matching routine_id that was provided in the request
    stmt = db.select(Routine).where(Routine.id == id)
    routine = db.session.scalar(stmt)

    # Check routine that matched was successfully found
    if routine:

        # User can only delete a routine that they created (unless they're an Admin)
        authorize(routine.user_id)
        db.session.delete(routine)
        db.session.commit()
        return {'Message': 'Routine has been successfully deleted. Any products have been dissasociated but not deleted.'}, 200
    
    else:
	    return {'Error': 'Routine not found'}, 404
