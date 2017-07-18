import asyncio
import json
import requests

from aiohttp import ClientSession
from firebase import firebase
from itertools import chain


class HnApi:
    def __init__(self, loop=None, session=None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.session = session if session else ClientSession(loop=self.loop)
        self.api_root = 'https://hacker-news.firebaseio.com/'
        self.firebase = firebase.FirebaseApplication(
            'https://hacker-news.firebaseio.com/', None)

    def get_top_stories(self):
        """Retrieves the top stories"""
        try:
            return self.firebase.get('/v0/topstories', None)
        except requests.exceptions.RequestException:
            print("Couldn't fetch top stories")
            raise

    def get_item(self, item):
        try:
            return self.firebase.get(f'/v0/item/{item}', None)
        except requests.exceptions.RequestException as e:
            print("item '{item}' not found")
            raise

    async def async_get_item(self, item):
        item_url = f"{self.api_root}v0/item/{item}.json"
        async with self.session.get(item_url) as response:
            f = await response.text()
            return json.loads(f)

    def get_comments(self,item):
        """Nasty peice of works - BFS without history"""
        new_items = [item]
        pending = []
        results = []
        while new_items or pending:
            tasks = chain(map(self.async_get_item, new_items), pending)
            done, pending = self.loop.run_until_complete(
                asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

            new_items = []
            for task in done:
                r = task.result()
                if r["type"] == "comment" and "text" in r:
                    results.append((r["id"], r["text"]))

                if "kids" in r:
                    new_items += r["kids"]
        return results

    def close(self):
        self.session.close()
        self.loop.close()
