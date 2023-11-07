from flask_wtf import FlaskForm

from wtforms import (
   StringField, SubmitField,
   TextAreaField,PasswordField,
   BooleanField
)

from wtforms.validators import (
  InputRequired, Email, EqualTo,
  DataRequired, Length
)

class FeedbackForm(FlaskForm):
  username = StringField("Username:", validators=[DataRequired("This field is required"), Length(min=1, max=100)], default="Anonymous", render_kw={"class": "wtf-form-inputfield"})
  feedback = TextAreaField("Feedback", validators=[DataRequired("This field is required"), Length(min=1 , max=255)], render_kw={"class": "wtf-form-textarea"})
  submit = SubmitField("Send", render_kw={"class" : "wtf-form-submitfield"})

class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(message="This field is required")], render_kw={"class": "wtf-form-inputfield"})
  password = PasswordField("Password", validators=[DataRequired("Password must contain at least 4 characters"), Length(min=4, max=10)], render_kw={"class": "wtf-form-inputfield"})
  remember = BooleanField("Remember me", default='unchecked', render_kw={"class": "toggle"})
  submit = SubmitField("Log In", render_kw={"class" : "wtf-form-submitfield"})

class ChangePasswordForm(FlaskForm):
  password = PasswordField("New PWD", validators=[DataRequired("Password must contain at least 4 characters"), Length(min=4, max=10)], render_kw={"class": "wtf-form-inputfield"})
  confirm_password = PasswordField("Confirm PWD", validators=[DataRequired("Password must contain at least 4 characters"), Length(min=4, max=10), EqualTo('password', message='Passwords must match')], render_kw={"class": "wtf-form-inputfield"})
  submit = SubmitField("Submit", render_kw={"class" : "wtf-form-submitfield"})