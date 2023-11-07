from datetime import datetime
from platform import machine as platform_machine
from platform import node as platform_node
from platform import processor as platform_proc
from platform import release as platform_release
from platform import system as platform_sys
from platform import version as platform_ver
from json import load as json_load
from json import dump as json_dump
from flask import redirect, render_template, request, url_for, session

from app import app


def post_handle():
    """
    Handles the POST request.
    Retrieves the list of routes from the Flask app's URL map, excluding the 'static' endpoint.
    Parses the command from the request form data and splits it into individual arguments.
    Determines the command from the first argument.
    Parameters:
        None
    Returns:
        Flask response object or None
    """
    user = session.get("user")
    routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
    command = request.form["command"]
    args = command.split()
    cmd = args[0]

    match(cmd):
        case "cd":
            route = None
            try:
                route = args[1]
            except Exception:
                pass
            if route and route in routes:
                return redirect(url_for(route))
            elif not route or route == "/" or route == "~":
                return redirect(url_for("root"))
        case "system":
            return redirect(url_for("system"))
        case "skills":
            id = None
            try:
                id = args[1]
            except Exception:
                pass
            if id:
                return redirect(url_for("skills", id=int(id)))
            else:
                return redirect(url_for("skills"))
        case "login":
            try:
                if not user:
                    username = args[1]
                    session["user"] = username

                return redirect(url_for("whoami"))
            except Exception as e:
                pass

            return redirect(url_for("login"))
        case "whoami":
            if user:
                return redirect(url_for("whoami"))
            
            return redirect(url_for("login"))
        case "exit": 
            if user:
                session.pop("user")
            return redirect(url_for("root"))
        case "passwd":
            return redirect(
                url_for("passwd")
            ) if session.get("user") else render_template(
                "exceptions/permissions.html",
                user=session.get("user"),
                route=request.path,
                exception="You don't have enough permissions to execute this command."
            )
        case "cookies":
            if len(args) >= 2:
                if len(args) == 4 and args[1] == "set":
                    return redirect(url_for("set_cookie", key=args[2], value=args[3]))
                elif args[1] == "wipe":
                    if len(args) == 3:
                        return redirect(url_for("wipe_cookie", key=args[2]))
                    else:
                        return redirect(url_for("wipe_cookie"))
        case "feedback":
            return redirect(url_for("feedback"))
        case _:
            pass