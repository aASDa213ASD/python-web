from datetime import datetime, timedelta
from platform import machine as platform_machine
from platform import node as platform_node
from platform import processor as platform_proc
from platform import system as platform_sys
from platform import version as platform_ver
from re import compile as re_compile
from json import loads as json_loads
from flask import redirect, render_template, request, session, url_for, make_response, flash

from .models import db, Feedback
from .forms import FeedbackForm, LoginForm

from app import app
from app import bcrypt
from app.bundle.handlers import post_handle
from app.bundle.models import db, User

""" Render helper function """
def render(template: str, **kwargs):
    return render_template(template, user=session.get("user"), **kwargs)

""" Cookies block """
@app.route("/setcookie", methods=["GET", "POST"])
def set_cookie():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    
    key = request.args.get("key")
    value = request.args.get("value")
    response = make_response(redirect(url_for("whoami")))

    if session.get("user"):
        if key and value:
            response.set_cookie(key=key, value=value)
    else:
        return render_template(
            "exceptions/permissions.html",
            user=session.get("user"), route=request.path,
            exception="You don't have enough permissions to execute this command."
        )
    return response

@app.route('/wipecookie', methods=["GET", "POST"])
def wipe_cookie():
    if request.method == "POST" and (handle := post_handle()):
        return handle

    key = request.args.get("key")
    response = make_response(redirect(url_for("whoami")))
    
    if session.get("user"):
        if key:
            response.delete_cookie(key)
        else:
            cookie_keys = request.cookies.keys()
            for key in cookie_keys:
                response.delete_cookie(key)
    else:
        return render_template(
            "exceptions/permissions.html",
            user=session.get("user"), route=request.path,
            exception="You don't have enough permissions to execute this command."
        )
    return response

def list_folders():
    return render("information/list_folders.html")
""" Information block """
@app.route("/ls", methods=["GET"])
def list_folders():
    return render("information/list_folders.html")

@app.route("/help", methods=["GET"])
def help():
    return render("information/help.html")

@app.route("/whois", methods=["GET"])
def whois():
    return render("information/whois.html")

@app.route("/projects", methods=["GET"])
def projects():
    return render("information/projects.html")

""" Route block """
@app.route('/skills', methods=["GET", "POST"])
@app.route('/skills/<int:id>', methods=["GET", "POST"])
def skills(id=None):
    if request.method == "POST" and (handle := post_handle()):
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
            return render("routes/skill_detail.html", route=request.path, skill=skill)

    return render("routes/skill_list.html", route=request.path, skills=skills)

@app.route("/system", methods=["GET", "POST"])
def system():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    
    pattern = re_compile(r'(Mozilla/5.0 \(.*\)) (AppleWebKit/.* \(.*\)) (Chrome/.* Safari/.*)')
    platform, webkit, browser = pattern.match(request.headers.get('User-Agent')).groups() 

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = {
        "System": platform_sys(),
        "Node": platform_node(),
        "Version": platform_ver(),
        "Machine": platform_machine(),
        "Processor": platform_proc(),
    }

    return render(
        "routes/system.html", 
        route=request.path,
        ua_platform=platform, ua_webkit=webkit, ua_browser=browser,
        os_info=os_info, current_time=current_time
    )

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    return render("routes/about.html", route=request.path)

@app.route("/gamehacking", methods=["GET", "POST"])
def gamehacking():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    return render("routes/gamehacking.html", route=request.path)

@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    return render("routes/gallery.html", route=request.path)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("whoami"))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_flag = form.remember.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if remember_flag:
                session['user_id'] = user.id
                session['user'] = user.username
                session['remember'] = remember_flag
                return redirect(url_for("whoami"))
            else:
                flash("You didn't check 'Remember me' flag. Check you credentials again.", "danger")
                return redirect(url_for("login"))
        else:
            flash("Authentication failure", "danger")
    return render("routes/login.html", route=request.path, form=form)

@app.route("/whoami", methods=["GET", "POST"])
def whoami():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    if session.get("user"):
        return render("routes/whoami.html", route=request.path, cookies=request.cookies)
    return redirect(url_for("login"))

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            username=form.username.data, 
            feedback=form.feedback.data
        )

        db.session.add(feedback)
        db.session.commit()

        flash('Feedback submitted successfully!')
        return redirect(url_for("feedback"))
    
    return render("routes/feedback.html", route=request.path, cookies=request.cookies, form=form, feedback_list=reversed(db.session.query(Feedback).all()))
    
@app.route("/exit", methods=["GET", "POST"])
def exit():
    try:
        session.pop("user")
    except Exception:
        pass
    return redirect(url_for("root"))

# @app.route("/null", methods=["GET", "POST"])
# def null():
#     # Create some users <-- delete this after
#     print("Adding sample users to database...")
#     hashed_password = bcrypt.generate_password_hash("master").decode('utf-8')
#     user1 = User(username="master", password=hashed_password)
#     hashed_password = bcrypt.generate_password_hash("wellick123").decode('utf-8')
#     user2 = User(username='tyrell', password=hashed_password)
#     hashed_password = bcrypt.generate_password_hash("r0b0t").decode('utf-8')
#     user3 = User(username='sams3pi0l', password=hashed_password)

#     # Add users to the database session
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.add(user3)

#     # Commit the changes to the database
#     db.session.commit()

#     print("Done, checkout the database now.")
#     return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST" and (handle := post_handle()):
        return handle
    return render("routes/root.html", route="~")