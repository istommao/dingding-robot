"""server.py."""
import datetime

from tornado import web, ioloop


class MainHandler(web.RequestHandler):

    def get(self):
        print(self.request.remote_ip)
        self.write('Hello world!\n')

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
