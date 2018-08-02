# -*- coding: utf-8 -*-

import tornado.web

from ..sql import SELECT
from .base import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            self.render('login.html')

    async def post(self):
        username = self.get_argument('username')
        passwd = self.get_argument('passwd')

        self.sqlite_execute(SELECT['users'], (username,))
        res = self.sqlite_fetchall()

        passwd_check = await self.verify_password(
            tornado.escape.utf8(passwd),
            res[0][0]
        )
        if not passwd_check:
            raise tornado.web.HTTPError(403, 'invalid password')

        self.set_secure_cookie('username', username)
        self.redirect(self.get_argument('next', '/'))


class LogoutHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.clear_cookie('username')
        self.redirect(self.get_argument('next', '/'))
