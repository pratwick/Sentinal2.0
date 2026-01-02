# Imports the same database object which is in __init__.py file
from app import db
from datetime import datetime
# This code defines a database table using Python, so Flask + SQLAlchemy know how to store sentiment data in the database of THIS app.
# You are creating a table design using a Python class.
# SentimentAnalysis → name of the table model
# db.Model - Comes from SQLAlchemy, Tells SQLAlchemy:This class belongs to the database connected to my Flask app
# This is where “knows which app to use” comes in Because earlier you did: db.init_app(app), db already knows which Flask app, So db.Model knows which database configuration to use
# Overall the below code says : This table belongs to THAT Flask app’s database.

class SentimentAnalysis(db.Model): # Creating the SentimentAnalysis class which is inheriting the db.model class
    __tablename__ = 'sentiment_analysis' # The table name in the database will be: sentiment_analysis
    # Each line below is one column in the table
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False) # nullable=False cannot be empty
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default = db.func.now()) # Stores date and time, Automatically filled when row is created, 

    # To represent the object you have to define the representer
    # This code decides how an object looks when you print it or see it in debugging
    # __repr__ defines a human-readable string representation of an object for debugging and logging purposes.
    # Here self is the object which is created for the above class
    def __repr__(self):
        return f'<Sentiment Analysis: {self.title}>'