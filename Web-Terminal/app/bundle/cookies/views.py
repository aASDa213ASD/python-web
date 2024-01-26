from . import cookies
from ..command_handler import handle_request
from ..render import render

from flask import redirect, render_template, request, session, url_for, make_response
from flask_jwt_extended import create_access_token


@cookies.route("/setcookie", methods=["GET", "POST"])
def set_cookie():
    if request.method == "POST" and (handle := handle_request()):
        return handle
    
    key = request.args.get("key")
    value = request.args.get("value")
    response = make_response(redirect(url_for("main.root")))

    if key and value:
        response.set_cookie(key=key, value=value)
    
    return response


@cookies.route('/wipecookie', methods=["GET", "POST"])
def wipe_cookie():
    """ Deprecated, use LoginManager instead """
    if request.method == "POST" and (handle := handle_request()):
        return handle

    key = request.args.get("key")
    response = make_response(redirect(url_for("main.root")))
    
    if key:
        response.delete_cookie(key)
    else:
        cookie_keys = request.cookies.keys()
        for key in cookie_keys:
            response.delete_cookie(key)
    
    return response
