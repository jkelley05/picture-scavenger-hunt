from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FileField, IntegerField
from wtforms.validators import DataRequired, regexp, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from picture_hunt.models import Team, Task

class TeamForm(Form):
    name = StringField('Team Name', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class TaskForm(Form):
    name = StringField('Task', validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])


class UploadForm(Form):
    team = SelectField('Team',coerce=int, choices=[(None, 'Make a Team first'),],validators=[NumberRange(min=0, message="Please choose a team first")] )
    task = SelectField('Task',coerce=int, choices=[(None, 'Make a Task first'),] ,validators=[NumberRange(min=0, message="Please choose a team first")])

    media = FileField('Media File', validators=[DataRequired()])


class SearchForm(Form):
    team =  QuerySelectField( query_factory=Team.query.all,
                              get_pk=lambda a: a.id,
                              get_label=lambda a: a.name,
                              allow_blank=True,
                              blank_text="All"
                            )

    task =  QuerySelectField( query_factory=Task.query.all,
                              get_pk=lambda a: a.id,
                              get_label=lambda a: a.name,
                              allow_blank=True,
                              blank_text="All"
                            )



