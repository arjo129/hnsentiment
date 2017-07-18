from texthandler import CommentClassifier
from hackernews import HnApi
from settings import NUM_STORIES, STORY_TEMPLATE, LAYOUT_PATH, PAGE_PATH


class AnalysisDaemon:
    def __init__(self, story_template, layout_path):
        self.hn_api = HnApi()
        self.classifier = CommentClassifier()
        self.story_template = story_template
        self.layout_path = layout_path

    def process_comment(self, comment):
        sent = self.classifier(comment)
        pos_neg = (1, 0) if sent['pos'] > sent['neg'] else (0, 1)
        return (*pos_neg, sent['compound'], sent["neu"])

    def process_story(self, story_id):
        comments = self.hn_api.get_comments(story_id)
        if comments:
            comments_sentiments = (
                self.process_comment(comment) for _, comment in comments)
            sentiment = list(map(sum, zip(*comments_sentiments)))
        else:
            sentiment = 0, 0, 0, 0
        title = self.hn_api.get_item(story_id)["title"]
        return self.story_template.format(title, *sentiment)

    def generate_report(self, num_stories, page_path):
        layout = read_file(self.layout_path)
        table = map(self.process_story,
                    self.hn_api.get_top_stories()[:num_stories])
        write_file(page_path, layout.replace("{}", "\n\t\t".join(table)))

    def close(self):
        self.hn_api.close()


def read_file(path):
    with open(path, 'r') as input_file:
        return input_file.read()


def write_file(path, text):
    with open(path, 'w') as output_file:
        return output_file.write(text)


if __name__ == "__main__":
    try:
        dae = AnalysisDaemon(STORY_TEMPLATE, LAYOUT_PATH)
        dae.generate_report(NUM_STORIES, PAGE_PATH)
    finally:
        dae.close()
