from flask_wtf          import FlaskForm
from wtforms            import (StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired,Length)


class FeedbackForm(FlaskForm):
  username = StringField("Username:", validators=[DataRequired("This field is required"), Length(min=1, max=100)], default="Anonymous", render_kw={"class": "wtf-form-inputfield"})
  feedback = TextAreaField("Feedback", validators=[DataRequired("This field is required"), Length(min=1 , max=255)], render_kw={"class": "wtf-form-textarea"})
  submit   = SubmitField("Send", render_kw={"class" : "wtf-form-submitfield"})
