from .models import Category, Tag


from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, SubmitField, PasswordField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length


UPLOAD_FOLDER = 'app/static/images/posts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif', 'webp'}
MAX_IMAGE_SIZE = (400, 300)
TYPE_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High')
]


class CreatePostForm(FlaskForm):
    title      = StringField("Post Title",validators=[DataRequired(message="This field is required")], render_kw={'placeholder': 'Enter the title of the post: '})
    text       = StringField("Post Text", validators=[DataRequired(message="This field is required")], render_kw={'placeholder': 'Enter the text of the post: '})
    image_file = FileField("Choose Image", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    type       = SelectField("Post Type", choices=TYPE_CHOICES, validators=[DataRequired(message="This field is required")])
    enabled    = BooleanField("Enable the post:", default='unchecked', render_kw={'placeholder': 'Enable the post: '})
    tag        = SelectMultipleField('Tag', coerce=int)
    category   = SelectField('Category', coerce=int)
    submit     = SubmitField("Create Post")

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]
        self.tag.choices = [(t.id, t.name) for t in Tag.query.all()]


class UpdatePostForm(FlaskForm):
    title      = StringField("Post Title", validators=[DataRequired(message="This field is required")], render_kw={'placeholder': 'Enter the title of the post: '})
    text       = StringField("Post Text", validators=[DataRequired(message="This field is required")], render_kw={'placeholder': 'Enter the text of the post: '})
    image_file = FileField("Choose Image", validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    type       = SelectField("Post Type", choices=TYPE_CHOICES, validators=[DataRequired(message="This field is required")])
    category   = SelectField('Category', coerce=int)
    tag        = SelectMultipleField('Tag', coerce=int)
    submit     = SubmitField("Update Post")

    def __init__(self, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]
        self.tag.choices = [(t.id, t.name) for t in Tag.query.all()]


class CreateCategoryForm(FlaskForm):
    name   = StringField('Category Name', validators=[DataRequired(message="This field is required"), Length(min=2, max=50)])
    submit = SubmitField('Create Category')


class UpdateCategoryForm(FlaskForm):
    name   = StringField('Category Name', validators=[DataRequired(message="This field is required"), Length(min=2, max=50)])
    submit = SubmitField('Update Category')


class CreateTagForm(FlaskForm):
    name   = StringField('Tag Name', validators=[DataRequired(message="This field is required"), Length(min=2, max=50)])
    submit = SubmitField('Create Tag')


class UpdateTagForm(FlaskForm):
    name   = StringField('Tag Name', validators=[DataRequired(message="This field is required"), Length(min=2, max=50)])
    submit = SubmitField('Update Tag')
