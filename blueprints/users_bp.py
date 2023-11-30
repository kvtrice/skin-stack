from flask import Blueprint, request
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from auth import admin_required

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

        return UserSchema(exclude=['password', 'products']).dump(user), 201
    
    except IntegrityError:
        return {'Error': 'This email address already in use!'}, 409
    

# Login Existing User
@users_bp.route('/login', methods=['POST'])
def login():
    # Parse incoming POST body through Schema
    user_info = UserSchema(only=['email', 'password']).load(request.json)

    # Query to match the user with an existing email
    stmt = db.select(User).where(User.email == user_info['email'])
    user = db.session.scalar(stmt)

    # Check user exists and that the password matches
    if user and bcrypt.check_password_hash(user.password, user_info['password']):
        # Create a JWT token
        token = create_access_token(identity=user.id, additional_claims={'email': user.email, 'first_name': user.first_name}, expires_delta=timedelta(hours=1)) # 1 hour expiry on token
        return {'token':token, 'user':UserSchema(exclude=['password', 'products']).dump(user)}
    
    # Otherwise advise login info was incorrect
    else:
        return {'Error': 'Password or Email address is invalid!'}, 401
    
# Get all users (admin only)
@users_bp.route('/')
@jwt_required()
def all_users():
    # Limit only to admins
    admin_required()
    # Query to select all users
    stmt = db.select(User) 
    users = db.session.scalars(stmt).all()

    return UserSchema(many=True, exclude=['password', 'products']).dump(users)