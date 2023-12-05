from flask import Blueprint
from setup import db, bcrypt
from models.user import User
from models.product import Product
from models.routine import Routine
from models.routineproduct import RoutineProduct

db_commands = Blueprint('db', __name__)

# Drop any existing databases and create a new one
@db_commands.cli.command('create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created tables')

# Seed the database wth starting data
@db_commands.cli.command('seed')
def db_seed():

    # Seed Users
    users = [
        User(
            first_name='Kat',
            last_name='Admin',
            email='admin@admin.com',
            is_admin=True,
            password=bcrypt.generate_password_hash('password').decode('utf8')
        ),
        User(
            first_name='Testa',
            last_name='Testerson',
            email='test@gmail.com',
            password=bcrypt.generate_password_hash('password').decode('utf8')
        )
    ]

    # Add and commit users
    db.session.add_all(users)
    db.session.commit()

    # Seed Routines
    routines = [
        # First User (Admin)
        Routine(
            day_of_week='Monday',
            time_of_day='AM',
            user_id=users[0].id
        ),
        Routine(
            day_of_week='Monday',
            time_of_day='PM',
            user_id=users[0].id
        ),

        # Second User (Not Admin)
        Routine(
            day_of_week='Monday',
            time_of_day='AM',
            user_id=users[1].id
        ),
        Routine(
            day_of_week='Monday',
            time_of_day='PM',
            user_id=users[1].id
        )
    ]

    # Add and commit Routines
    db.session.add_all(routines)
    db.session.commit()

    # Seed Products
    products = [
        Product(
           name='Daily Moisturiser',
           brand='CeraVe',
           notes='Use both AM & PM. Contains Hylauronic Acid.',
           user_id=users[0].id
        ),
        Product(
           name='Niacinimide',
           brand='The Ordinary',
           notes='Very drying for my skin, I prefer to use it only once a day max. Apply before heavy creams.',
           user_id=users[0].id
        ),
        Product(
           name='Oil-Free Moisturiser',
           brand="Paula's Choice",
           notes="Use daily, morning and evening",
           user_id=users[1].id
        ),
        Product(
           name='Hydrating Cleanser',
           brand='CeraVe',
           notes="Cleanse AM & PM each day at the beginning of routine (before any creams or serums).",
           user_id=users[1].id
        ),
        Product(
           name='Hylauronic Acid 2% + B5',
           brand='The Ordinary',
           notes="Works best for me only in the AM. Apply before any creams. Only need a few drops.",
           user_id=users[1].id
        ),
    ]

    # Add & Commit Products
    db.session.add_all(products)
    db.session.commit()

    # Seed Products into Routines
    routine_products = [

        # First Users Products into Routines
        RoutineProduct(
            product_id = products[0].id, 
            routine_id = routines[0].id # Mon AM
        ),
        RoutineProduct(
            product_id = products[1].id, 
            routine_id = routines[0].id # Mon AM
        ),
        RoutineProduct(
            product_id = products[0].id,
            routine_id = routines[1].id # Mon PM
        ),
        RoutineProduct(
            product_id = products[1].id,
            routine_id = routines[1].id # Mon PM
        ),

        # Second Users Products into Routines
        RoutineProduct(
            product_id = products[2].id, 
            routine_id = routines[2].id # Mon AM
        ),
        RoutineProduct(
            product_id = products[3].id, 
            routine_id = routines[2].id # Mon AM
        ),
        RoutineProduct(
            product_id = products[2].id,
            routine_id = routines[3].id # Mon PM
        ),
        RoutineProduct(
            product_id = products[4].id,
            routine_id = routines[3].id # Mon PM
        )
    ]

    # Add & Commit RoutineProducts
    db.session.add_all(routine_products)
    db.session.commit()

    print('Database seeded')