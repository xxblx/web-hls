# -*- coding: utf-8 -*-

import os

import tornado.web

#from .handlers.testweb import TestWebHandler
#from .handlers.auth import LoginHandler, LogoutHandler
#
#from .handlers.api.testapi import TestApiHandler
#from .handlers.api.auth import SignupHandler, GetKeyHandler
#from .handlers.api.tokens import TokenGetHandler, TokenRenewHandler

from .conf import DEBUG, CAMERAS, VIDEO_DIR


class WebApp(tornado.web.Application):

    def __init__(self):

        handlers = [
#            (r'/', TestWebHandler),
#            (r'/login', LoginHandler),
#            (r'/logout', LogoutHandler),
#            (r'/api/signup', SignupHandler),
#            (r'/api/token/get', TokenGetHandler),
#            (r'/api/token/renew', TokenRenewHandler),
#            (r'/api/key/get', GetKeyHandler),
#            (r'/api/test', TestApiHandler)
        ]

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        static_path = os.path.join(os.path.dirname(__file__), 'static')

        settings = {
            'template_path': template_path,
            'static_path': static_path,
            'login_url': '/login',
            'debug': DEBUG,
            'xsrf_cookies': True,
            'cookie_secret': os.urandom(32)
        }

        super(WebApp, self).__init__(handlers, **settings)
