from .        import feedback
from .models  import Feedback, db
from .forms   import FeedbackForm
from ..render import render

from flask    import flash, redirect, request, url_for


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
