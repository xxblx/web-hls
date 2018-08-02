# -*- coding: utf-8 -*-

import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import tornado.web

from .handlers.auth import LoginHandler, LogoutHandler
from .handlers.main import MainPageHandler, SourcePageHandler

from .sql import SELECT


class WebApp(tornado.web.Application):

    def __init__(self, loop, db_path, debug):
        self.loop = loop  # tornado and asyncio loop
        self.executor = ThreadPoolExecutor(4)

        if not os.path.exists(db_path):
            raise
        self.db_path = db_path

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        handlers = [
            (r'/', MainPageHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/source/([0-9]*/?)', SourcePageHandler)
        ]

        # Fetch info about videos
        self.cursor.execute(SELECT['video'])
        self.videos = self.cursor.fetchall()

        # FIXME: m3u8 and ts are available without auth
        # Add video paths to handlers
        for video in self.videos:
            path = os.path.dirname(video[1])
            handlers.append(
                (r'/video/%d/(video[0-9]?\.(m3u8|ts))' % video[0],
                 tornado.web.StaticFileHandler, {'path': path})
            )

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        static_path = os.path.join(os.path.dirname(__file__), 'static')

        settings = {
            'template_path': template_path,
            'static_path': static_path,
            'login_url': '/login',
            'debug': debug,
            'xsrf_cookies': True,
            'cookie_secret': os.urandom(32)
        }

        super(WebApp, self).__init__(handlers, **settings)
