from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.products_bp import products_bp
from blueprints.routines_bp import routines_bp

app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(routines_bp)

# print(app.url_map)