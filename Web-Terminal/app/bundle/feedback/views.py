from . import feedback
from ..command_handler import handle_request
from ..render import render


from flask import flash, redirect, render_template, request, session, url_for, make_response
from flask_jwt_extended import create_access_token
from flask_login import login_user, current_user, logout_user, login_required

from .models import Feedback, db
from .forms import FeedbackForm

@feedback.route("/feedback", methods=["GET", "POST"])
def feedback_list():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            username=form.username.data, 
            feedback=form.feedback.data
        )

        db.session.add(feedback)
        db.session.commit()

        flash('Feedback submitted successfully!')
        return redirect(url_for("feedback.feedback_list"))
    
    return render("routes/feedback.html", route=request.path, cookies=request.cookies, form=form, feedback_list=reversed(db.session.query(Feedback).all()))