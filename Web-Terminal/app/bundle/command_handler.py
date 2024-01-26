from flask       import redirect, request, url_for
from flask_login import current_user, logout_user


"""
Some render help function:
----------------------------------------------
from flask import render_template

def render(template: str, **kwargs):
    return render_template(template, **kwargs)
"""

def handle_request(app):
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
    print(f"[Command handler] Available routes: {routes}")

    requested_command = request.form["command"]
    arguments = requested_command.split()
    command = arguments[0]

    match(command):
        # Main
        case "cd": # needs fix
            route = None
            try:
                route = arguments[1]
            except Exception:
                pass

            if route:
                matched_routes = [r for r in routes if r.endswith('.' + route)]
                if matched_routes:
                    return redirect(url_for(matched_routes[0]))
            elif not route or route == "/" or route == "~":
                return redirect(url_for("main.root"))
        
        case "skills":
            id = None
            try:
                id = arguments[1]
            except Exception:
                pass
            if id:
                return redirect(url_for("main.skills", id=int(id)))
            else:
                return redirect(url_for("main.skills"))
        
        # Accounts
        case "register":
            return redirect(url_for("accounts.register"))
        
        case "login":
            if not current_user:
                return redirect(url_for("accounts.whoami"))
            
            return redirect(url_for("accounts.login"))
        
        case "exit": 
            logout_user()
            return redirect(url_for("main.root"))
        
        case "whoami":
            if current_user:
                return redirect(url_for("accounts.whoami"))

            return redirect(url_for("accounts.login"))

        case "passwd": 
            return redirect(url_for("accounts.passwd"))

        case "users":
            return redirect(url_for("accounts.users"))
        
        # Cookies
        case "cookies":
            if len(arguments) >= 2:
                if len(arguments) == 4 and arguments[1] == "set":
                    return redirect(url_for("cookies.set_cookie", key=arguments[2], value=arguments[3]))
                elif arguments[1] == "wipe":
                    if len(arguments) == 3:
                        return redirect(url_for("cookies.wipe_cookie", key=arguments[2]))
                    else:
                        return redirect(url_for("cookies.wipe_cookie"))
        
        # Feedback
        case "feedback":
            return redirect(url_for("feedback.feedback_list"))
        
        # Todo
        case "todo":
            return redirect(url_for("todo.todo_list"))
        
        # Posts
        case "posts":
            return redirect(url_for("posts.view_categories"))
        
        case _:
            pass