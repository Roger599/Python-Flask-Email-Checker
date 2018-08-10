from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class FileForm(FlaskForm):
    file = FileField('file', validators=[FileRequired(), FileAllowed(['txt', 'csv'], 'Text and CSV Files only!')])
    submit = SubmitField('Extract')


class TextAreaForm(FlaskForm):
    text = TextAreaField('text', validators=[DataRequired()], render_kw={"placeholder": "Enter or paste some text"})
    submit = SubmitField('Extract')


class EmailForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Verify')
