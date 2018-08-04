# -*- coding: utf-8 -*-

import tornado.web

from .base import BaseHandler


class MainPageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        sources = [(v[0], v[2], v[3]) for v in self.videos]
        self.render('index.html', sources=sources)


class SourcePageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, source_num):
        if source_num.endswith('/'):
            source_num = source_num[:-1]

        if int(source_num) not in self.videos_nums:
            raise tornado.web.HTTPError(404)

        sources = [(v[0], v[2], v[3]) for v in self.videos]
        self.render('source.html', source_num=source_num, sources=sources)
