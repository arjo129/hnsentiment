import hackernews
import re
from html.parser import HTMLParser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class CommentCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = ""
        
    def handle_data(self, data):
        self.data += data


class CommentClassifier:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
    def clean_comment(self, comment):
        parser = CommentCleaner()
        parser.feed(comment)
        return parser.data

    def __call__(self, comment):
        # Call the sentiment analyzer. It might be a good idea to chain multiple
        # classifiers. So for instance VADER, then a Keras model etc.
        self.clean_comment(comment)
        return self.sentiment_analyzer.polarity_scores(comment)
