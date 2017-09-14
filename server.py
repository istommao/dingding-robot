"""server.py."""
import datetime

import tornadoredis

from tornado import web, ioloop, gen


CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=500,
                                              wait_for_available=True)


class MainHandler(web.RequestHandler):

    @web.asynchronous
    @gen.engine
    def get(self):
        client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
        info = yield gen.Task(client.info)

        print(self.request.remote_ip, info)

        self.write('Hello world!\n')
        yield gen.Task(client.disconnect)

    def post(self):
        print(self.request.body)
        # save to redis
        self.write(self.request.body)


def scheduler():
    print('4s ', datetime.datetime.now())
    # check redis task


if __name__ == '__main__':
    app = web.Application([
        (r'/', MainHandler),
    ])
    app.listen(8081)
    print('http://127.0.0.1:8081')

    ioloop.PeriodicCallback(scheduler, 4000).start()
    ioloop.IOLoop.instance().start()
