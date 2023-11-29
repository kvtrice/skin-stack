from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.users import User
from setup import db

def admin_required():
    # Get the users identity
    user_id = get_jwt_identity()

    # Match the user to an existing email address
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)

    # Check if the user is an admin based on the is_admin boolean
    # If not, abort the request
    if not (user and user.is_admin):
        abort(401)