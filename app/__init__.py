from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

# Imports the SQLAlchemy class
# This class knows how to: Connect to a database, Create tables, Insert and read data
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
# Creates one database manager object
# Is not connected to any app yet
# Think db as database engine that is waiting to be connected
db = SQLAlchemy() # db is initialize with the class ie SQLAlchemy

cache = Cache() # Cache is initialize with the Cache class

# Now we will create create_app() functionality
# This function will: Create the Flask app, Configure it, Attach database to it
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we dont want versioning as of now so we can concentrate on the entire code itself
                                                         # But you can create the versioning and track the modification when we are dealing with the bigger application
    app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE')
    app.config['CACHE_REDIS_URL'] = os.getenv('CACHE_REDIS_URL')
    app.config['CACHE_REDIS_PORT'] = os.getenv('CACHE_REDIS_PORT')
    app.config['CACHE_DEFAULT_TIMEOUT'] = os.getenv('CACHE_DEFAULT_TIMEOUT')
    db.init_app(app) # This line connects db to the Flask app, after this db knows which app to use, 
                  # Hey db, this is the Flask app you should work with.
    cache.init_app(app) # For the cache also you will initialize this app

    # From here we will start working with routes.py file
    # we have to modularise the code and we have to create a blueprint
    # A Blueprint is a way to organize your Flask application by splitting it into smaller, feature-based parts 
      # Instead of putting all routes in one file, you group related routes together
      # Blueprint = a container for routes of one feature
      # ex -
      # Auth blueprint → login, register
      # Sentiment blueprint → sentiment APIs
      # Product blueprint → product APIs
       
    # You are importing a Blueprint named sentiment_bp
    # What is sentiment_bp - It is a Blueprint object, Defined in app/routes.py, Contains sentiment-related routes only, so we are trying to bring the sentiment route into the main app
    from app.routes import sentiments_bp 
    # This line attaches the sentiment blueprint to the main Flask app
    # Flask does not know about those routes, after this line Routes become live and accessible
    # url_prefix='/api/sentiment' - Add a common starting path to all routes in this blueprint.
    # ex - we have @sentiment_bp.route('/analyze') - Without prefix: http://localhost:5000/analyze
       # - with url_prefiz it will be http://localhost:5000/api/sentiment/analyze ie /api/sentiment  +  /analyze
    app.register_blueprint(sentiments_bp, url_prefix = '/api/sentiment')
    return app

