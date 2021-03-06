import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_cors import CORS

# Importing blueprints
import main.controllers as controller
from main.resources import auth_controller
from main.services import mail_controller
from main.services.jobs import tasks

from main.extensions import db, jwt, out_server_sender, scheduler

# Flask API RESTFUL principal initialization
api = Api()

# Loading environment variables
load_dotenv()

DB_PATH = str(os.getenv("SQLALCHEMY_DB_PATH"))
DB_NAME = str(os.getenv("SQLALCHEMY_DB_NAME"))
DB_URL = "sqlite:////" + DB_PATH + DB_NAME


class Config(object):
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=DB_URL)
    }
    SCHEDULER_API_ENABLED = True


# Function that activates primary keys recognition in the SQLite DB
def activate_primary_keys(connection, _connection_record):
    connection.execute('pragma foreign_keys=ON')


# Function that creates an instance of the Flask application, summing other complements
def create_app():
    # Flask app initialization
    app = Flask(__name__)

    app.config.from_object(Config())

    # Creating database
    if not os.path.exists(DB_PATH + DB_NAME):
        os.mknod(DB_PATH + DB_NAME)

    # Database configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

    # Database initialization in Flask app
    db.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    @app.before_first_request
    def load_tasks():
        pass

    # Defining secret key for encryption and time of expiration of each access token that will be generated
    app.config['JWT_SECRET_KEY'] = str(os.getenv('JWT_SECRET_KEY'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    # JWT management initialization in Flask app
    jwt.init_app(app)

    # Defining general configuration for SMTP server
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    # Flask mail handler initialization in Flask app
    out_server_sender.init_app(app)

    # Flask CORS configuration to allow access 
    CORS(app, resources={r"/*": {"origins": "*", "expose_headers":  ['X-Total-Count']}})

    # When the database is "connected in Flask app, the primary keys will activate"
    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', activate_primary_keys)

    # Defining urls for each resource
    api.add_resource(controller.SensorController, '/sensors/<id_num>')
    api.add_resource(controller.SensorsController, '/sensors')
    api.add_resource(controller.USeismController, '/seisms/unverified/<id_num>')
    api.add_resource(controller.USeismsController, '/seisms/unverified/')
    api.add_resource(controller.VSeismController, '/seisms/verified/<id_num>')
    api.add_resource(controller.GSeismsController, '/seisms/coordinates')
    api.add_resource(controller.VSeismsController, '/seisms/verified/')
    api.add_resource(controller.UserController, '/users/<id_num>')
    api.add_resource(controller.UsersController, '/users')
    api.add_resource(controller.UsersFilter, '/users/filter')
    api.add_resource(controller.SensorsFilter, '/sensors/filter')

    # Defining blueprints for each blueprint
    app.register_blueprint(auth_controller)
    app.register_blueprint(mail_controller)

    # Final app initialization
    api.init_app(app)

    return app
