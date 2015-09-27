from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class TeamForm(Form):
    name = StringField('Team Name', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class TaskForm(Form):
    name = StringField('Task', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class UploadForm(Form):
    team = SelectField('Task', choices=['team1', 'team2'], validators=[DataRequired()])






