import ast
from os import path
from hackernews import HnApi


TEST_DATA_PATH = "test_data"


def get_test_data(data_path):
    with open(path.join(TEST_DATA_PATH, data_path), 'r') as data_file:
        return ast.literal_eval(data_file.read())


def set_comments():
    hn_api = HnApi()
    comments = sorted(hn_api.get_comments(14751340))
    with open(path.join(TEST_DATA_PATH, "comments"), 'w') as output_file:
        output_file.write(repr(comments))
        print(repr(comments))
    hn_api.session.close()
