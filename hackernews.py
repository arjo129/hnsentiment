from firebase import firebase

class HNApi:
        def __init__(self):
                self.firebase = firebase.FirebaseApplication('https://hacker-news.firebaseio.com/', None)
        def top_stories(self):
                """Retrieves the top stories"""
                try:
                        return self.firebase.get('/v0/topstories',None)
                except:
                        print("Couldn't fetch top stories")
        def get_item(self,item):
                try:
                        return self.firebase.get('/v0/item/'+str(item),None)
                except Exception as E:
                        print("item "+str(item)+" not found")
                        print(E)
        def get_comments(self,story):
                # TODO ASYNCIFY THIS
                comments = []
                story = self.get_item(story)
                try:
                        if story["type"] == "comment":
                                comments.append((story["id"],story["text"]))
                        children = story["kids"]
                        for comment in children:
                                comments += self.get_comments(comment)
                        return comments
                except KeyError as k:
                        return comments

