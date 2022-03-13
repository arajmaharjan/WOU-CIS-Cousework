from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class PostForm(FlaskForm):
    category_id = SelectField(u"Category", coerce=int)
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=256)])
    link = BooleanField("Link Post")
    url = StringField("URL", validators=[Length(min=0, max=256)])
    body = TextAreaField("Text (optional)", validators=[Length(min=0, max=2800)])
    submit = SubmitField("Create Post")


class CommentForm(FlaskForm):
    body = TextAreaField("Thoughts?", validators=[Length(min=0, max=2800)])
    submit = SubmitField("Comment")
