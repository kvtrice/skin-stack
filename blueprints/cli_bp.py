from flask import Blueprint
from setup import db, bcrypt
from models.users import User
from models.products import Product

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

    # Add some starting users
    users = [
        User(
            first_name='Sarah',
            last_name='Smith',
            email='sarahsmith@gmail.com',
            password=bcrypt.generate_password_hash('smitherson').decode('utf8')
        ),
        User(
            first_name='Katie',
            last_name='Peterson',
            email='katie@gmail.com',
            password=bcrypt.generate_password_hash('katie123').decode('utf8')
        )
    ]

    # Add some starting products
    products = [
        Product(
           name='Daily Moisturiser',
           brand='CeraVe',
           notes='Use both AM & PM. Contains Hylauronic Acid.',
        #    user_id=users1.id # Association
        ),
        Product(
           name='Niacinimide',
           brand='The Ordinary',
           notes='Very drying for my skin, I prefer to use it only once a day max. Sometimes only once every 2 days if possible. But it definitely helps with texture so continue to include in routine',
        #    user_id=users1.id # Association
        ),
        Product(
           name='Azelaic Acid 20%',
           brand='Aztec',
           notes="Can use both AM & PM. Ideally don't use with other dying products (e.g: other acne treatments). Use SPF daily when using this product.",
        #    user_id=users2.id # Association
        )
    ]

    # Add & Commit the tables
    db.session.add_all(users)
    db.session.add_all(products)
    db.session.commit()

    print('Database seeded')