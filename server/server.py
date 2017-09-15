"""server.py."""
import os

from tornado import ioloop, web

from app.scheduler import scheduler
from app.views import MainHandler

BASE_DIR = os.path.dirname(__file__)

STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


if __name__ == '__main__':

    HANDLERS = [
        (r'/', MainHandler),
        (r'/static/(.*)', web.StaticFileHandler, {'path': STATIC_DIR})
    ]

    APP = web.Application(
        handlers=HANDLERS,
        template_path=TEMPLATE_DIR
    )
    PORT = 8081
    APP.listen(PORT)
    print('http://127.0.0.1:{}'.format(PORT))

    TIME_STEP = 4000    # 4s
    ioloop.PeriodicCallback(scheduler, TIME_STEP).start()
    ioloop.IOLoop.instance().start()
