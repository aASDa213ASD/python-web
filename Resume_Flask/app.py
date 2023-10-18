from datetime import datetime
from platform import machine as platform_machine
from platform import node as platform_node
from platform import processor as platform_proc
from platform import release as platform_release
from platform import system as platform_sys
from platform import version as platform_ver

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def handle_post():
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
            return render_template("system.html", os_info=os_info, user_agent=user_agent, current_time=current_time)
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

@app.route("/ls", methods=["GET"])
def list_folders():
    return render_template("information/list_folders.html")

@app.route("/help", methods=["GET"])
def help():
    return render_template("information/help.html")

@app.route("/whois", methods=["GET"])
def whois():
    return render_template("information/whois.html")

@app.route("/projects", methods=["GET"])
def projects():
    return render_template("information/projects.html")

@app.route('/skills', methods=["GET", "POST"])
@app.route('/skills/<int:id>', methods=["GET", "POST"])
def skills(id=None):
    if request.method == "POST" and (handle := handle_post()):
        return handle
    
    skills = [
        {"name": "Assembly", "description": "Reverse Engineering"},
        {"name": "C++", "description": "Internal Domain"},
        {"name": "Python", "description": "Botnet Producer"},
        {"name": "Java", "description": "Stuff Manager"}
    ]

    if id or id == 0:
        skill = None
        try:
            skill = skills[id]
        except Exception:
            pass
        if skill:
            return render_template("skill_detail.html", skill=skill)

    return render_template("skill_list.html", skills=skills)

@app.route("/system", methods=["GET", "POST"])
def system():
    if request.method == "POST" and (handle := handle_post()):
        return handle
    
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

    return render_template("system.html", os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST" and (handle := handle_post()):
        return handle
    return render_template("about.html")

@app.route("/gamehacking", methods=["GET", "POST"])
def gamehacking():
    if request.method == "POST" and (handle := handle_post()):
        return handle
    return render_template("gamehacking.html")

@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    if request.method == "POST" and (handle := handle_post()):
        return handle
    return render_template("gallery.html")

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST" and (handle := handle_post()):
        return handle
    return render_template("root.html")

if  __name__ == "__main__":
    app.run(debug=True)
