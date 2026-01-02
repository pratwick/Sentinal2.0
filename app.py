import os # Imports Python’s built-in os module, used to Access environment variables, Interact with the operating system, Later used to read the PORT value
from dotenv import load_dotenv # Imports load_dotenv() from the python-dotenv package, Reads variables from a .env file, Loads them into the system’s environment variables (os.environ)
from app import create_app, db # create_app is application factory function is the function which we will write in __init__.py file and db is SQLAlchemy database instance
                               # Also the database object is being created in the init itself
from app.logger import configure_logger

load_dotenv() # Reads the .env file and Loads all key-value pairs into os.environ

# Create Flask application instance and calling the application factory function
# You are creating your Flask app in a smart and organized way.
# Instead of writing: app = Flask(__name__), directly in one file, you put all app-setup logic inside a function called create_app().
# This is called the Application Factory Pattern.
# Think of create_app() like a factory: 
  # You give raw materials (config, database, routes)
  # The factory builds a ready-to-use Flask app
  # You get a finished product
  # Raw config + DB + routes → create_app() → Flask app
app = create_app() # Create the app with create_app() functionality

# Application context - Flask needs to know which app is currently active
# Here, app is the Flask application object created by create_app().
# with app.app_context(): with this You are explicitly telling Flask: For the following code, I am working with THIS application → app
# app.app_context() sets app as the active Flask application so its configuration and extensions can be used safely.
with app.app_context():
    db.create_all() # Create database tables, Based on models defined using db.Model, Runs only if tables do not already exist

# Main module check -
# What is __name__ - Python gives every file a special variable called __name__
# If you run the file directly: then __name__ == '__main__'
# if __name__ == '__main__': the line means run the code below only when this file is executed directly.
# Overall with the below code it means Start the app only if this file is the starting point.
if __name__ == '__main__':
    # app.run() Starts the Flask web server
    # Parameters:  host='0.0.0.0' means Allows the app to be accessed from: Other devices, Docker containers, Cloud platforms, Not just your local computer
                #  debug=True : Auto-restarts server on code changes, Shows detailed error messages, Helpful for development, Don’t use debug=True in production
    port = int(os.environ.get('PORT', 8080)) # get PORT if available, else use 8080
    app.run(host='0.0.0.0', port=port, debug=True)

# Over all If this file is run directly, get the port number and start the Flask server.