from . import accounts
from ..command_handler import handle_request
from ..render import render


from flask_login import login_user, current_user, logout_user, login_required
from flask import redirect, render_template, request, session, url_for, make_response, flash
from .forms import LoginForm, ChangePasswordForm, RegisterForm, UpdateAccountForm
from .models import User, db
from flask_jwt_extended import create_access_token
from secrets import token_hex
from PIL import Image
import os
from app import bcrypt
from datetime import datetime
from flask import current_app, request


@accounts.after_request
def update_last_seen(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error while updating user last seen: {str(e)}", "danger")
    return response


""" Pfp helper function"""
def save_picture(app, form_pfp):
    random_hex = token_hex(8)
    f_name, f_ext = os.path.splitext(form_pfp.filename)
    pfp_fn = random_hex + f_ext
    pfp_path = os.path.join(app.root_path, 'static/images/pfps', pfp_fn)
    image = Image.open(form_pfp)
    image.thumbnail((360, 360))
    image.save(pfp_path)
    return pfp_fn


@accounts.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.whoami"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been created.", category="flash-success")

        return redirect(url_for("accounts.login"))
    
    return render("routes/register.html", route=request.path, form=form)


@accounts.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.whoami"))
        
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_flag = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and user.validate_pwd(password):
            if remember_flag:
                access_token = create_access_token(identity=username)
                login_user(user, remember_flag)
                response = redirect(url_for("accounts.whoami"))
                response.set_cookie('access_token', access_token)
                return response
            else:
                return redirect(url_for("main.root"))
        else:
            flash("Authentication failure", "danger")
    return render("routes/login.html", route=request.path, form=form)


@accounts.route("/whoami", methods=["GET", "POST"])
@login_required
def whoami():
    form = UpdateAccountForm()
    form.username.default = current_user.username
    form.bio.default = current_user.bio

    if form.validate_on_submit():
        if form.pfp.data:
            with current_app.app_context():
                pfp_file = save_picture(current_app, form.pfp.data)
            current_user.pfp = pfp_file
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for("accounts.whoami"))
    
    if current_user.is_authenticated:
        """ Deprecated request.cookies, use LoginManager instead """
        form.process()
        return render("routes/whoami.html", route=request.path, cookies=request.cookies, form=form)
    
    return redirect(url_for("accounts.login"))


@accounts.route("/exit", methods=["GET", "POST"])
def exit():
    try:
        logout_user()
    except Exception:
        pass
    return redirect(url_for("main.root"))


@accounts.route("/passwd", methods=["GET", "POST"])
@login_required
def passwd():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_pwd = form.password.data
        confirm_pwd = form.confirm_password.data
        user = User.query.filter_by(username=current_user.username).first()

        if user:
            new_pwd = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
            user.password = new_pwd

            db.session.add(user)
            db.session.commit()

            logout_user()
            return redirect(url_for("accounts.login"))
        
    return render("routes/passwd.html", route=request.path, form=form)


@accounts.route("/users", methods=["GET", "POST"])
def users():
    with current_app.app_context():
        if request.method == "POST" and (handle := handle_request(current_app)):
            return handle
        
    return render("routes/users.html", route=request.path, user_list=User.query.all())