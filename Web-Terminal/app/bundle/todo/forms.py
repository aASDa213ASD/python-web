from flask_wtf          import FlaskForm
from datetime           import date
from wtforms            import (StringField, SubmitField, DateField)
from wtforms.validators import (DataRequired, Length)


class TODOForm(FlaskForm):
  title = StringField("Task", validators=[DataRequired("Task is required"), Length(min=1, max=100)], render_kw={"class": "wtf-form-inputfield"})
  description = StringField("Description", validators=[DataRequired("Description is required"), Length(min=1, max=200)], render_kw={"class": "wtf-form-inputfield"})
  due_date = DateField("Due Date", format="%Y-%m-%d", default=date.today())
  submit = SubmitField("Append", render_kw={"class" : "wtf-form-submitfield"})