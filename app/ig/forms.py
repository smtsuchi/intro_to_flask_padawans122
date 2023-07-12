from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField(label = 'Title', validators=[DataRequired()])
    img_url = StringField(label = 'Image URL', validators=[DataRequired()])
    caption = StringField(label = 'Caption')
    submit = SubmitField()