"""server.py."""
import datetime

from tornado import web, ioloop


class MainHandler(web.RequestHandler):

    def get(self):
        print(self.request.remote_ip)
        self.write('Hello world!\n')

    def post(self):
        print(self.request.body)
        self.write(self.request.body)


def scheduler():
    print('4s ', datetime.datetime.now())


if __name__ == '__main__':
    application = web.Application([
        (r'/', MainHandler),
    ])
    application.listen(8081)
    print('http://127.0.0.1:8081')
    ioloop.PeriodicCallback(scheduler, 4000).start()
    ioloop.IOLoop.instance().start()
