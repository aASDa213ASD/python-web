from datetime import datetime
from platform import machine as platform_machine
from platform import node as platform_node
from platform import processor as platform_proc
from platform import release as platform_release
from platform import system as platform_sys
from platform import version as platform_ver

from flask import redirect, render_template, request, url_for

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
            elif not route or route == "/":
                print("redirecting to root")
                return redirect(url_for("root"))
        case "system":
            user_agent = request.headers.get('User-Agent')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os_info = {
                "System": platform_sys(),
                "Node": platform_node(),
                "Release": platform_release(),
                "Version": platform_ver(),
                "Machine": platform_machine(),
                "Processor": platform_proc(),
            }
            return render_template("routes/system.html", os_info=os_info, user_agent=user_agent, current_time=current_time)
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
        case _:
            pass