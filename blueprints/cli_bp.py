from flask import Blueprint
from setup import db, bcrypt
from models.user import User
from models.product import Product
from models.routine import Routine

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
            first_name='Sarah',
            last_name='Smith',
            email='sarahsmith@gmail.com',
            is_admin=True,
            password=bcrypt.generate_password_hash('smitherson').decode('utf8')
        ),
        User(
            first_name='Katie',
            last_name='Peterson',
            email='katie@gmail.com',
            password=bcrypt.generate_password_hash('katie123').decode('utf8')
        )
    ]

    # Add and commit users
    db.session.add_all(users)
    db.session.commit()

    # Seed Routines
    routines = [
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
        Routine(
            day_of_week='Tuesday',
            time_of_day='AM',
            user_id=users[0].id
        ),
        Routine(
            day_of_week='Wednesday',
            time_of_day='AM',
            user_id=users[1].id
        ),
        Routine(
            day_of_week='Wednesday',
            time_of_day='PM',
            user_id=users[1].id
        ),
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
           notes='Very drying for my skin, I prefer to use it only once a day max. Sometimes only once every 2 days if possible. But it definitely helps with texture so continue to include in routine',
           user_id=users[0].id
        ),
        Product(
           name='Azelaic Acid 20%',
           brand='AzClear',
           notes="Can use both AM & PM. Ideally don't use with other drying products (e.g: other acne treatments). Use SPF daily when using this product.",
           user_id=users[1].id
        )
    ]

    # Add & Commit Products
    db.session.add_all(products)
    db.session.commit()

    print('Database seeded')