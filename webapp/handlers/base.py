# -*- coding: utf-8 -*-

from functools import wraps

import bcrypt
import tornado.web
import tornado.concurrent


class BaseHandler(tornado.web.RequestHandler):

    @property
    def loop(self):
        return self.application.loop

    @property
    def executor(self):
        return self.application.executor

    @property
    def cursor(self):
        return self.application.cursor

    @property
    def videos(self):
        return self.application.videos

    @tornado.concurrent.run_on_executor
    def verify_password(self, passwd, passwd_hash):
        return bcrypt.checkpw(passwd, passwd_hash)

    @wraps
    def run_in_loop_executor(method):
        """ Decorator for queries to sqlite from Handlers """

        async def wrapper(self, *args):
            future = self.loop.run_in_executor(None, method, self, *args)
            data = await future
            return data
        return wrapper

    @run_in_loop_executor
    def sqlite_execute(self, sql, *args):
        return self.cursor.execute(sql, *args)

    @run_in_loop_executor
    def sqlite_fetchall(self):
        return self.cursor.fetchall()

    def get_current_user(self):
        return self.get_secure_cookie('username')
