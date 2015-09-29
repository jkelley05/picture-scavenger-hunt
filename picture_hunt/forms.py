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
    team = SelectField('Team', choices=[('team1', 'Team 1'), ('team2', 'Team 2')] )
    task = SelectField('Task', choices=[('task1', 'Task 1'), ('task2', 'Task 2')] )

    media = FileField(u'Media File')






