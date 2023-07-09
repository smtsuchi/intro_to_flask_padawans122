from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm your password", [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField(label = 'Title', validators=[DataRequired()])
    img_url = StringField(label = 'Image URL', validators=[DataRequired()])
    caption = StringField(label = 'Caption')
    submit = SubmitField()