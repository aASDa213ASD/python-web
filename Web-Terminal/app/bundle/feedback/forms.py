from flask_wtf import FlaskForm
from datetime import date
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
  StringField,   SubmitField,
  TextAreaField, PasswordField,
  BooleanField,  DateField, 
  ValidationError
)
from wtforms.validators import (
  EqualTo, DataRequired,
  Length,  Regexp
)


class FeedbackForm(FlaskForm):
  username = StringField("Username:", validators=[DataRequired("This field is required"), Length(min=1, max=100)], default="Anonymous", render_kw={"class": "wtf-form-inputfield"})
  feedback = TextAreaField("Feedback", validators=[DataRequired("This field is required"), Length(min=1 , max=255)], render_kw={"class": "wtf-form-textarea"})
  submit = SubmitField("Send", render_kw={"class" : "wtf-form-submitfield"})