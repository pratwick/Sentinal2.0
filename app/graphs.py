import os
import matplotlib
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter, defaultdict
import re
matplotlib.use('Agg')  # We are using aggrigrate functions for rendering GUI aggrigations
import matplotlib.pyplot as plt  # for saving the figure into the directory


# Create the directory for the images:
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_graphs(sentiment_results, topic):
    # extract sentiment label and scores
    # Here we will use list comprehensions
    sentiment = [result['sentiment'] for result in sentiment_results]  
    # This line creates a new list in memory that contains only the sentiment values from all the results

    scores = [result['score'] for result in sentiment_results]  
    # Create a list of all sentiment scores from sentiment_results

    # ----------------------------------------------------
    # FIX: Aggregate scores per sentiment (REQUIRED)
    # ----------------------------------------------------
    sentiment_score_map = defaultdict(list)

    for s, score in zip(sentiment, scores):
        sentiment_score_map[s].append(score)

    sentiments = list(sentiment_score_map.keys())
    avg_scores = [sum(values) / len(values) for values in sentiment_score_map.values()]

    images_dir = os.path.join('static', 'images')  
    # static directory is used for images and templates directory is for all the html templates
    create_directory(images_dir)

    bar_chart_path = os.path.join(images_dir, 'sentiment_bar_chart.png')
    word_cloud_path = os.path.join(images_dir, 'word_cloud.png')

    # define bar plots:
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=sentiments, y=avg_scores, palette='coolwarm')

    plt.title(f'Sentiment Scores for the Reddit Posts on "{topic}"', fontsize=16)
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Average Score', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Add data labels on top of the bars
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.2f}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            fontsize=12,
            color='black',
            xytext=(0, 5),
            textcoords='offset points'
        )

    # Add gridlines for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the bar plot to a PNG file
    plt.savefig(bar_chart_path)
    plt.close()  # Close the plot to avoid memory issues

    # Convert the bar chart to base64 for returning in the response
    bar_chart_64 = encode_image_to_base64(bar_chart_path)

    # Generate word cloud from most frequent words in content
    text = ' '.join([result['content'] for result in sentiment_results])

    # Clean the text (remove special characters, numbers, etc.)
    text = re.sub(r'[^A-Za-z\s]', '', text.lower())  
    # Remove non-alphabetic characters and make lowercase

    # Tokenize the text into words and count frequency
    words = text.split()
    word_counts = Counter(words)

    # Generate the word cloud from the most frequent words
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=200,
        colormap='viridis'
    ).generate_from_frequencies(word_counts)

    # Save the word cloud to a PNG file
    wordcloud.to_file(word_cloud_path)

    # Convert the word cloud image to base64 for returning in the response
    word_cloud_b64 = encode_image_to_base64(word_cloud_path)

    return bar_chart_64, word_cloud_b64


def encode_image_to_base64(imagepath):
    with open(imagepath, "rb") as img_file:
        img_64 = base64.b64encode(img_file.read()).decode("utf-8")
    return img_64
