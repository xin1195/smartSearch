#!/usr/bin/env python3

from home.handler.baseHandler import BaseHandler


class HomeIndexHandler(BaseHandler):
    def get(self):
        self.render("home/index.html")



