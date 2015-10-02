from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, regexp

class TeamForm(Form):
    name = StringField('Team Name', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class TaskForm(Form):
    name = StringField('Task', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class UploadForm(Form):
    team = SelectField('Team',coerce=int, choices=[(None, 'Make a Team first'),] )
    task = SelectField('Task',coerce=int, choices=[(None, 'Make a Task first'),] )

    media = FileField('Media File', validators=[DataRequired()])


class SearchForm(Form):
    team = SelectField('Team', coerce=int, choices=[(-1, 'Make a Team first'),] )
    task = SelectField('Task', coerce=int, choices=[(-1, 'Make a Task first'),] )




