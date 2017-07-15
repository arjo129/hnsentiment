import pytest
from test_helper import get_test_data

from texthandler import CommentClassifier

@pytest.fixture
def comment():
    return get_test_data("comment")

@pytest.fixture
def clean_comment():
    return get_test_data("clean_comment")

def test_comment_cleaner(comment, clean_comment):
    assert CommentClassifier().clean_comment(comment) == clean_comment

def test_comment_classifier(comment):
    sentimental_analysis = CommentClassifier()(comment)
    assert sentimental_analysis["neg"] > sentimental_analysis["pos"]
