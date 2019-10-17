# -*- coding:utf-8 -*-

from bottle import route, run
from bottle import request, template

from settings import DB_PASSWORD
from dao import Dao


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
    username = request.query.get("user")
    password = request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return template("user/login", username=username, password=password)


@route("/user/login", method="POST")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")

    result = dao.select_user(username, password)
    if len(result) > 0:
        return template("user/do_login", username=username, password=password)

    return template("user/failed_to_login")


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


dao = Dao(
    "mysql://docker:{pw}@localhost:3306/vxr".format(pw=DB_PASSWORD))
run(host="localhost", port=8080, debug=True)
