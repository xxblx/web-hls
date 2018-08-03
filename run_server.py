#!VENV/bin/python
# -*- coding: utf-8 -*-

import argparse

import tornado.httpserver
import tornado.ioloop

from webapp.app import WebApp


def main():
    parser = argparse.ArgumentParser(prog='web-hls')
    parser.add_argument('--db', type=str, required=True,
                        help='absolute path to db')
    parser.add_argument('--debug', action='store_true', default=False)

    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8888)
    args = parser.parse_args()

    loop = tornado.ioloop.IOLoop.current()
    app = WebApp(loop, args.db, args.debug)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(args.port, args.host)

    try:
        loop.start()
    except KeyboardInterrupt:
        loop.stop()
    finally:
        loop.close()


if __name__ == '__main__':
    main()
