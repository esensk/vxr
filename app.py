# -*- coding:utf-8 -*-

import pathlib
import bottle
from beaker.middleware import SessionMiddleware

from settings import DB_PASSWORD
from constants import IMAGE_DIR
from dao import Dao


SESSION_OPTS = {
    "session.type": "file",
    "session.data_dir": "/tmp",
    "session.cookie_expires": True,
    "session.auto": True,
}


@bottle.route("/")
def top():
    session = bottle.request.environ.get("beaker.session")
    username = session.get("username", "")
    return bottle.template("top", username=username)


@bottle.route("/user/register")
def register():
    session = bottle.request.environ.get("beaker.session")
    if "username" in session:
        return bottle.redirect("/")

    username = bottle.request.query.get("user")
    password = bottle.request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return bottle.template("user/register",
                           username=username, password=password)


@bottle.route("/user/register", method="POST")
def do_register():
    session = bottle.request.environ.get("beaker.session")
    if "username" in session:
        return bottle.redirect("/")

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    success = dao.insert_user(username, password)

    if success:
        session["username"] = username
        session.save()
        return bottle.template("top",
                               username=username, password=password)

    return bottle.template("user/failed_to_register")


@bottle.route("/user/login")
def login():
    session = bottle.request.environ.get("beaker.session")
    if "username" in session:
        return bottle.redirect("/")

    username = bottle.request.query.get("user")
    password = bottle.request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return bottle.template("user/login", username=username, password=password)


@bottle.route("/user/login", method="POST")
def do_login():
    session = bottle.request.environ.get("beaker.session")
    if "username" in session:
        return bottle.redirect("/")

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    result = dao.select_user(username, password)
    if len(result) > 0:
        session["username"] = username
        session.save()
        return bottle.template("top", username=username, password=password)

    return bottle.template("user/failed_to_login")


@bottle.route("/user/update")
def update():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    username = bottle.request.query.get("user")
    password = bottle.request.query.get("pass")
    new_username = bottle.request.query.get("new_user")
    new_password = bottle.request.query.get("new_pass")

    username = "" if username is None else username
    password = "" if password is None else password
    new_username = "" if new_username is None else new_username
    new_password = "" if new_password is None else new_password

    return bottle.template("user/update", username=username, password=password,
                           new_username=new_username,
                           new_password=new_password)


@bottle.route("/user/update", method="POST")
def do_update():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    new_username = bottle.request.forms.get("mew_username")
    new_password = bottle.request.forms.get("new_password")

    success = dao.update_user(username, password, new_username, new_password)

    if success:
        return bottle.template("user/do_update",
                               username=username, password=password)

    return bottle.template("user/failed_to_update")


@bottle.route("/user/delete")
def delete():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    username = bottle.request.query.get("user")
    password = bottle.request.query.get("pass")

    username = "" if username is None else username
    password = "" if password is None else password

    return bottle.template("user/delete", username=username, password=password)


@bottle.route("/user/delete", method="POST")
def do_delete():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    success = dao.delete_user(username, password)

    if success:
        return bottle.template("user/do_delete",
                               username=username, password=password)

    return bottle.template("user/failed_to_delete")


@bottle.route("/image/upload")
def upload():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    return """
        <form action="/image/upload" method="post" enctype="multipart/form-data">
            <input type="submit" value"Upload"></br>
            <input type="file" name="upload"></br>
        </form>
    """


@bottle.route("/image/upload", method="POST")
def do_upload():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    upload = bottle.request.files.get("upload", "")
    if not upload.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return "File extenstion not allowed"

    upload.save(IMAGE_DIR)
    return "Upload OK. FilePath: %s%s" % (IMAGE_DIR, upload.filename)


@bottle.route("/image/effect/apply/<filename:re:.*\.(png|jpg|jpeg)>")
def apply_effect(filename):
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    effector = bottle.request.query.get("effector")

    return bottle.template("image/effect/apply",
                           filename=filename, effector=effector)


@bottle.route("/image/effect/apply/<filename:re:.*\.(png|jpg|jpeg)>",
              method="POST")
def do_apply_effect(filename):
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    effector = bottle.request.forms.get("effector")

    exec(effector)
    return bottle.template("image/effect/applied", effector=effector,
                           filename_1=filename, filename_2="applied.jpg")


@bottle.route("/image/delete/<filename:re:.*\.(png|jpg|jpeg)>")
def delete_effect_applied_image(filename):
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    path = pathlib.Path(filename)

    assert path.exists()

    path.unlink()

    bottle.redirect("/show")


@bottle.route("/static/img/<filename:re:.*\.(png|jpg|jpeg)>")
def show_image(filename):
    return bottle.static_file(filename, root="static/img/")


@bottle.route("/static/css/<filename:re:.*\.css>")
def set_style(filename):
    return bottle.static_file(filename, root="static/css/")


@bottle.route("/show")
def show_images():
    session = bottle.request.environ.get("beaker.session")
    if "username" not in session:
        return bottle.redirect("/user/login")

    path_iter = pathlib.Path(IMAGE_DIR).iterdir()

    images = []
    for path in path_iter:
        images.append(str(path))

    return bottle.template("image/show", images=images)


dao = Dao("mysql://docker:{pw}@localhost:3306/vxr".format(pw=DB_PASSWORD))
app = bottle.default_app()
app = SessionMiddleware(app, SESSION_OPTS)
bottle.run(app=app, host="localhost", debug=True, port=8080, reloader=True)
