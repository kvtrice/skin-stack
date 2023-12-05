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


#----------------------------------------------------------------
# ADD PRODUCT TO A ROUTINE

@routines_bp.route('/<int:routine_id>/products/<int:product_id>', methods=['POST'])
@jwt_required()
def add_product_to_routine(routine_id, product_id):

    # Find the routine based on the matching routine_id that was provided in the request
    stmt1 = db.select(Routine).where(Routine.id == routine_id)
    routine = db.session.scalar(stmt1)

    # Find the product based on the matching product_id that was provided in the request
    stmt2 = db.select(Product).where(Product.id == product_id)
    product = db.session.scalar(stmt2)

    # Check both the routine and product were successfully found
    if routine and product:

        # User can only add a product to a routine that they own (unless they're an Admin)
        authorize(routine.user_id)

        # Check if the product is already associated with that routine
        existing_association = db.session.query(RoutineProduct).filter(
             RoutineProduct.routine_id == routine_id,
             RoutineProduct.product_id == product_id
        ).first()

        if not existing_association:
             
            # Add a new relationship between specified routine and product in RoutineProduct
            new_product_routine = RoutineProduct(
                 routine=routine, 
                 product=product
                 )
            db.session.add(new_product_routine)
            db.session.commit()
            return {'Message': 'Product has been successfully added to this routine.'}, 200
        
        else:
             return {'Message': 'Product is already associated with this routine.'}, 400
    
    else:
	    return {'Error': 'Specified routine or product not found.'}, 404
    

#----------------------------------------------------------------
# DELETE A PRODUCT FROM A ROUTINE

@routines_bp.route('/<int:routine_id>/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product_from_routine(routine_id, product_id):

    # Find the routine based on the matching routine_id that was provided in the request
    stmt1 = db.select(Routine).where(Routine.id == routine_id)
    routine = db.session.scalar(stmt1)

    # Find the product based on the matching product_id that was provided in the request
    stmt2 = db.select(Product).where(Product.id == product_id)
    product = db.session.scalar(stmt2)

    # Check both the routine and product were successfully found
    if routine and product:

        # User can only delete a a product from a routine that they own (unless they're an Admin)
        authorize(routine.user_id)

        # Delete the specified product from RoutineProduct (removing the relationship only)
        stmt3 = db.delete(RoutineProduct).where(RoutineProduct.routine_id == routine_id, RoutineProduct.product_id == product_id)
        db.session.execute(stmt3)

        db.session.commit()
        return {'Message': 'Product has been successfully deleted from this routine.'}, 200
    
    else:
	    return {'Error': 'Specified routine or product not found'}, 404