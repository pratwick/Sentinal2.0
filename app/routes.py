# You are importing Flask tools: Blueprint → to create a module (feature), 
                              #: request → to read user input (form / query data)
                              #: jsonify to send JSON responses
                              #: render_template → to show HTML pages
from flask import Blueprint, request, jsonify, render_template

# Function that fetches posts from Reddit based on a topic
from app.fetch_reddit_data import fetch_reddit_data
#Function that analyzes sentiment (positive / negative / neutral)
from app.analysis import analyse_sentiment
# from app.graphs import generate_graphs
from app.graphs import generate_graphs


from app import db, cache # db → database connection (SQLAlchemy), cache → Redis cache object
from app.models import SentimentAnalysis # Imports the database table model.
from app.logger import configure_logger # Sets up logging so you can see: What is happening

# Now we will create a blueprint by the blueprint name
# we require the template folder here, we will use the templates for our purpose
# Groups all sentiment-related routes
# Uses templates from the templates folder, All sentiment logic lives here.
sentiments_bp = Blueprint('sentiment', __name__, template_folder='templates')
logger = configure_logger() # Creates a logger to print useful messages in terminal.

# Now we will use the blueprint, When user visits /, Show the index.html page
@sentiments_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html') # To return the index.html to render in UI

@sentiments_bp.route('/analyze', methods=['GET', 'POST'])
# Main Sentiment Analysis Route
# Since we are using redis cache so we will add cache annotator here -
# Depending on the topic the cache will be hit or miss

#Redis Cache Decorator
# Store result in cache for 1 hour, Cache key is based on the topic, this is why because If user asks same topic again, don’t recompute everything.
@cache.cached(
    timeout=3600,
    key_prefix=lambda: f"{request.form.get('topic') or request.args.get('topic', '')}_{request.form.get('num_records', 10)}"
)
def analyze_sentiment_route():
    # Reading User Input
    # Get topic from form or URL 
    topic = request.form.get('topic') or request.args.get('topic')

    #Get number of records (default = 10)
    limit = int(request.form.get('num_records', 10))

    # If user didn’t give topic → return error.
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Go to the sentiment_analysis table, find records for this topic, sort them by newest first, take only a few of them, and give me all those records
    sentiment_results = SentimentAnalysis.query.filter_by(topic=topic).order_by(SentimentAnalysis.created_at.desc()).limit(limit).all()
    
    # If data exists in DB
    # Data already exists → no need to call Reddit again
    # Log that DB was used
    # Convert DB objects into simple list of dictionary format
    if sentiment_results:
        logger.info('Data fetched from sentiment analysis table')
        sentiment_results = [
            {
                "title" : record.title,
                "content" : record.content,
                "sentiment": record.sentiment,
                "score": record.score,
            }
            for record in sentiment_results
        ]
    else:  # If data NOT in DB, Fetch Reddit data, Analyze sentiment, Save results to database
        posts = fetch_reddit_data(topic, limit) # Fetch Reddit posts for a given topic
        # Analyze sentiment -
        sentiment_results = analyse_sentiment(posts)

        # Save each result to database
        # db.session.add(...) - Add this new record to the temporary session, Still NOT saved in database, SQLAlchemy uses a session as a waiting area
        # For every sentiment result: Create a record and add it to the session, at this point the data is in memory not yet saved in database
        # db.session.commit() - Finally save everything permanently, Write data into the database table, which indicates Confirm and save all changes
        for result in sentiment_results:
            db.session.add(SentimentAnalysis(
                topic=topic,
                title=result['title'],
                content=result['content'],
                sentiment=result['sentiment'],
                score = result['score'],
            ))
        db.session.commit()

    # generate_graphs() creates: a bar chart, a word cloud, These images are converted into base64 strings
    # Not saved to disk, Not saved to Database, it is in memory
    bar_chart_64, word_cloud_b64 = generate_graphs(sentiment_results, topic)

    # Take all this data that is currently in memory and give it to index.html
    # Takes index.html, and injects topic, sentiment_results, bar_chart_64 and word_cloud_b64 all variables into it.
    return render_template(
        'index.html',
        topic=topic,
        sentiment_results=sentiment_results,
        bar_chart_64=bar_chart_64,
        word_cloud_b64=word_cloud_b64 
    )

# This is how the render template will take all of this all together and publish in Jinja template as dynamic variable
# and publish it as UI.