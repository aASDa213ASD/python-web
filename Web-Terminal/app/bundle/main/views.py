from . import main
from ..command_handler import handle_request
from ..render import render


from flask import current_app, request
from datetime import datetime
from re import compile as re_compile
from platform import (
    machine   as platform_machine,
    node      as platform_node,
    processor as platform_cpu,
    system    as platform_system,
    version   as platform_version
)


@main.route("/", methods=["GET", "POST"])
def root():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
    
    return render("routes/root.html", route="~")


@main.route("/ls", methods=["GET"])
def list_folders():
    return render("information/list_folders.html")


@main.route("/help", methods=["GET"])
def help():
    return render("information/help.html")


@main.route("/whois", methods=["GET"])
def whois():
    return render("information/whois.html")


@main.route("/projects", methods=["GET"])
def projects():
    return render("information/projects.html")


@main.route("/about", methods=["GET", "POST"])
def about():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
        
    return render("routes/about.html", route=request.path)


@main.route("/gamehacking", methods=["GET", "POST"])
def gamehacking():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
    
    return render("routes/gamehacking.html", route=request.path)


@main.route("/gallery", methods=["GET", "POST"])
def gallery():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
    
    return render("routes/gallery.html", route=request.path)


@main.route("/system", methods=["GET", "POST"])
def system():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
    
    pattern = re_compile(r'(Mozilla/5.0 \(.*\)) (AppleWebKit/.* \(.*\)) (Chrome/.* Safari/.*)')
    platform, webkit, browser = pattern.match(request.headers.get('User-Agent')).groups() 

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os_info = {
        "System":    platform_system(),
        "Node":      platform_node(),
        "Version":   platform_version(),
        "Machine":   platform_machine(),
        "Processor": platform_cpu(),
    }

    return render(
        "routes/system.html", route=request.path,
        ua_platform=platform, ua_webkit=webkit, ua_browser=browser,
        os_info=os_info, current_time=current_time
    )


@main.route('/skills', methods=["GET", "POST"])
@main.route('/skills/<int:id>', methods=["GET", "POST"])
def skills(id: int = None):
    with current_app.app_context():
        if (request.method == "POST") and (handle := handle_request(current_app)):
            return handle
    
    skills = [
        {"name": "Assembly", "description": "Reverse Engineering"},
        {"name": "C++",      "description": "Internal Domain"    },
        {"name": "Python",   "description": "Botnet Producer"    },
        {"name": "Java",     "description": "Stuff Manager"      }
    ]

    if id or id == 0:
        try:
            skill = skills[id]
        except Exception:
            pass

        if skill:
            return render("routes/skill_detail.html", route=request.path, skill=skill)

    return render("routes/skill_list.html", route=request.path, skills=skills)
