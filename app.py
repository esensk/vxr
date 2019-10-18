# -*- coding:utf-8 -*-

from bottle import route, run
from bottle import request, template

from settings import DB_PASSWORD
from constants import IMAGE_DIR
from dao import Dao


@route("/")
def top():
    return template("top")


@route("/user/register")
def register():
    username = request.query.get("user")
    password = request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return template("user/register", username=username, password=password)


@route("/user/register", method="POST")
def do_register():
    username = request.forms.get("username")
    password = request.forms.get("password")

    success = dao.insert_user(username, password)

    if success:
        return template("top",
                        username=username, password=password)

    return template("user/failed_to_register")


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
        return template("top", username=username, password=password)

    return template("user/failed_to_login")


@route("/user/update")
def update():
    username = request.query.get("user")
    password = request.query.get("pass")
    new_username = request.query.get("new_user")
    new_password = request.query.get("new_pass")

    username = "" if username is None else username
    password = "" if password is None else password
    new_username = "" if new_username is None else new_username
    new_password = "" if new_password is None else new_password

    return template("user/update", username=username, password=password,
                    new_username=new_username, new_password=new_password)


@route("/user/update", method="POST")
def do_update():
    username = request.forms.get("username")
    password = request.forms.get("password")
    new_username = request.forms.get("mew_username")
    new_password = request.forms.get("new_password")

    success = dao.update_user(username, password, new_username, new_password)

    if success:
        return template("user/do_update", username=username, password=password)

    return template("user/failed_to_update")


@route("/user/delete")
def delete():
    username = request.query.get("user")
    password = request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return template("user/delete", username=username, password=password)


@route("/user/delete", method="POST")
def do_delete():
    username = request.forms.get("username")
    password = request.forms.get("password")

    success = dao.delete_user(username, password)

    if success:
        return template("user/do_delete", username=username, password=password)

    return template("user/failed_to_delete")


@route("/image/upload")
def upload():
    return """
        <form action="/image/upload" method="post" enctype="multipart/form-data">
            <input type="submit" value"Upload"></br>
            <input type="file" name="upload"></br>
        </form>
    """


@route("/image/upload", method="POST")
def do_upload():
    upload = request.files.get("upload", "")
    if not upload.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return "File extenstion not allowed"

    upload.save(IMAGE_DIR)
    return "Upload OK. FilePath: %s%s" % (IMAGE_DIR, upload.filename)


dao = Dao("mysql://docker:{pw}@localhost:3306/vxr".format(pw=DB_PASSWORD))
run(host="localhost", port=8080, debug=True)
