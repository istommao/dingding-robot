"""app views."""
import os
import logging

from tornado import web, gen
from tornado.escape import json_encode

from . import cache, conf

logging.basicConfig(level=logging.INFO, filename='main.log')

BASE_DIR = os.path.dirname(__file__)

START_KEY = 'monitor:{}:{}'


class MainHandler(web.RequestHandler):
    """MainHandler."""

    def handler_message(self):
        """handler_message."""
        key = START_KEY.format('sentry', 'alarm')
        data = self.request.body.decode()

        logging.info('handler message %s', data)

        value = json_encode(data)
        cache.KVSTORE.lpush(key, value)

        self.write(self.request.body)

    @web.asynchronous
    @gen.engine
    def post(self):
        token = self.get_query_argument('access_token', default=None, strip=True)
        if token is None or token != conf.ALLOW_TOKEN:
            self.write('invalid token')
        else:
            self.handler_message()
        self.finish()
