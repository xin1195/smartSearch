#!/usr/bin/env python3
# _*_coding:utf-8_*_
import hashlib
import traceback

import tornado.web
from tornado import gen

from admin.handler.baseHandler import BaseHandler
from common.authLib import auth_permissions
from setting import logger


class AdminUserHandler(BaseHandler):
    @tornado.web.authenticated
    @auth_permissions
    @gen.coroutine
    def get(self, *args, **kwargs):
        res_msg = ""
        users = []
        num = int(self.get_argument("num", 15))
        page = int(self.get_argument("page", 1))
        total_count = 0
        try:
            query = {}
            show = {"_id": 0}
            cursor = self.db.sys_user.find(query, show).skip((page - 1) * num).limit(num)
            while (yield cursor.fetch_next):
                user = cursor.next_object()
                users.append(user)
            total_count = yield self.db.sys_user.find().count()
        except:
            logger.error(traceback.format_exc())
        self.render("admin/sys_user_list.html", users=users, res_msg=res_msg, total_count=total_count, page=page, num=num)


class AdminUserAddHandler(BaseHandler):
    @tornado.web.authenticated
    @auth_permissions
    @gen.coroutine
    def get(self, *args, **kwargs):
        res_msg = ""
        user = {}
        self.render("admin/sys_user_add.html", res_msg=res_msg, form_action="/admin/user/add", user=user)

    @auth_permissions
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        email = self.get_argument("email", "")
        tell_phone = self.get_argument("tell_phone", "")
        try:
            salt = hashlib.md5(username.encode('utf-8')).hexdigest()
            hash_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            user_dict = {
                "username": username,
                "password": hash_password,
                "email": email,
                "tell_phone": tell_phone,
            }
            query = {"username": username}
            yield self.db.sys_user.update(query, user_dict, upsert=True)
        except:
            logger.error(traceback.format_exc())
        self.redirect("/admin/user")


class AdminUserUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    @auth_permissions
    @gen.coroutine
    def get(self, *args, **kwargs):
        res_msg = ""
        user = {}
        try:
            username = self.get_argument("username", "")
            query = {"username": username}
            show = {"_id": 0}
            user = yield self.db.sys_user.find_one(query, show)
        except:
            logger.error(traceback.format_exc())
        self.render("admin/sys_user_add.html", user=user, res_msg=res_msg, form_action="/admin/user/update")

    @auth_permissions
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        email = self.get_argument("email", "")
        tell_phone = self.get_argument("tell_phone", "")
        try:
            user_dict = {
                "username": username,
                "email": email,
                "tell_phone": tell_phone,
            }
            if password:
                salt = hashlib.md5(username.encode('utf-8')).hexdigest()
                hash_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
                user_dict["password"] = hash_password
            query = {"username": username}
            yield self.db.sys_user.update(query, {"$set": user_dict}, upsert=True)
        except:
            logger.error(traceback.format_exc())
        self.redirect("/admin/user")


class AdminUserDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @auth_permissions
    @gen.coroutine
    def get(self, *args, **kwargs):
        try:
            username = self.get_argument("username", "")
            query = {"username": username}
            self.db.sys_user.remove(query)
        except:
            logger.error(traceback.format_exc())
        self.redirect("/admin/user")
