import asyncio
import pytest 
from aiohttp import ClientSession
from test_helper import get_test_data

from hackernews import HnApi
from settings import NUM_STORIES


@pytest.fixture
def loop_session():
    loop = asyncio.new_event_loop()
    session = ClientSession(loop=loop)
    asyncio.set_event_loop(loop)
    yield loop, session
    session.close()
    loop.close()


def test_get_top_stories(loop_session):
    top_stories = HnApi(*loop_session).get_top_stories()
    assert len(top_stories) >= NUM_STORIES
    assert list(map(type, top_stories)) == [int] * len(top_stories)


def test_async_get_item(loop_session):
    hn_api = HnApi(*loop_session)
    future = asyncio.ensure_future(hn_api.async_get_item(1))
    hn_api.loop.run_until_complete(future)
    expected_results = {
        'by': 'pg', 'descendants': 15, 'id': 1, 'kids': [487171, 15, 234509,
                                                         454410, 82729],
        'score': 61, 'time': 1160418111, 'title': 'Y Combinator', 'type':
        'story', 'url': 'http://ycombinator.com'}
    assert future.result() == expected_results


@pytest.fixture
def expected_comments():
    return get_test_data("comments")


def test_get_comments(loop_session, expected_comments):
        hn_api = HnApi(*loop_session)
        comments = hn_api.get_comments(14751340)
        assert sorted(comments) == expected_comments
