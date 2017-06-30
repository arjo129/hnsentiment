from texthandler import CommentCleaner, CommentClassifier
from hackernews import HNApi

class AnalysisDaemon:
    def __init__(self):
        self.hnapi = HNApi()
        self.stories = self.hnapi.top_stories()
        self.classifier = CommentClassifier()
        
    def generate_report(self):
        with open("index.html","w") as fp:
            print("<html><body><table>", file=fp)
            print("<tr><th>Story</th><th>Positive</th><th>Negative</th><th>Compund</th><th>Neutral</th></tr>", file=fp)
            i = 0
            for story in self.stories[:10]:
                print(i)
                i+=1
                st = self.hnapi.get_item(story)
                comments = self.hnapi.get_comments(story)
                pos, neg, comp, nuetral = 0,0,0,0
                for _id,comment in comments:
                    sent = self.classifier(comment)
                    if sent["pos"] > sent["neg"]:
                        pos += 1
                    else:
                        neg += 1
                    comp += sent["compound"]
                    nuetral += sent["neu"]
                print("<tr><td>%s</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>"%(st["title"],pos,neg,comp,nuetral), file=fp)
            print("</table></body></html>", file=fp)
if __name__ == "__main__":
    AnalysisDaemon().generate_report()
