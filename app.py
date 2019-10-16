# -*- coding:utf-8 -*-

from bottle import route, run


@route("/")
def index():
    pass


@route("/user/register")
def register():
    pass


@route("/user/register", method="POST")
def do_register():
    pass


@route("/user/login")
def login():
    pass


@route("/user/login", method="POST")
def do_login():
    pass


@route("/user/update")
def update():
    pass


@route("/user/update", method="POST")
def do_update():
    pass


@route("/user/delete")
def delete():
    pass


@route("/user/delete", method="POST")
def do_delete():
    pass


run(host="localhost", port=8080, debug=True)
