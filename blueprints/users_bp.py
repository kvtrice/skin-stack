from flask import Blueprint, request
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError

from models.users import User, UserSchema

# Create user blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Register new User
@users_bp.route('/register', methods=['POST'])
def register():
    try:
        # Parse incoming POST body through Schema
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)

        # Create a new user with the parsed data
        user = User(
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
        )

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        # Return the new user
        return UserSchema(exclude=['password', 'products']).dump(user), 201
    
    except IntegrityError:
        return {'Error': 'This email address already in use!'}, 409
    

# Login Existing User
