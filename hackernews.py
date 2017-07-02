from firebase import firebase

import asyncio
from aiohttp import ClientSession
import json

class CommentRequest:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self._session = ClientSession(loop=self.loop)
        self._api_root = 'https://hacker-news.firebaseio.com/'
        self.comments = []
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
    async def _get_item(self,item):
        async with self._session.get(self._api_root+'/v0/item/'+str(item)+'.json') as response:
            f = await response.text()
            obj = json.loads(f)
            return obj
            
    def get_comments(self,item):
        """Nasty peice of works - BFS without history"""
        queue = [item]
        res =[]
        while queue:
            execution = queue.copy()
            tasks = list(map(lambda x: self._get_item(x) if type(x) == type(1) else x, execution))
            queue = []
            finished, unfinished = self.loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
            for task in finished:
                r = task.result()
                if r["type"] == "comment" and "text" in r:
                    res.append((r["id"],r["text"]))
                try:
                    queue += r["kids"]
                except KeyError:
                    pass
            queue += unfinished
        return res
    def __del__(self):
        self._session.close()
        self.loop.close()


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
