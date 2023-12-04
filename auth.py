from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.user import User
from setup import db

# Admin Only Authorisation
def admin_required():
    # Get the users identity
    user_id = get_jwt_identity()

    # Match the user to an existing user id
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    
    return user and user.is_admin


# Authorisation for Users to only be able to access their own resources
def authorize(user_id=None):
    # Get users identity
    jwt_user_id = get_jwt_identity()

    # Match the user to an existing user id
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)

    # Check if the user id matches the authenticated user id OR check if the user is an admin (as this would also enable access; ddmins can access everything)
    if not (user.is_admin or (user_id and jwt_user_id == user_id)):
        abort(401)