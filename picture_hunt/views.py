from picture_hunt import config
from picture_hunt import app, db, lm
from picture_hunt.models import Media, Team, Task
from picture_hunt.forms import TeamForm, TaskForm, UploadForm

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify

from flask.ext.login import login_user, logout_user, current_user, login_required

import pprint as pp

@app.route('/')
def index():
    
    media = Media.query.all()

    # Search by team or event or missing info

    return render_template('index.jinja2.html', media=media)


@app.route('/upload')
def upload():
    
    form = UploadForm()

    return render_template('upload.jinja2.html', form=form)



@app.route('/teams', methods=['GET', 'POST'])
def teams():
    
    teams = None 
    form = TeamForm()
    if form.validate_on_submit():
        
        team = Team( name=form.name.data, note=form.note.data )
        
        db.session.add(team)
        db.session.commit()
        
        teams.append(team)
        redirect('/teams')
    
    teams = Team.query.all()
    
    return render_template('teams.jinja2.html', teams=teams, form=form)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    
    tasks = None
    team = None 
    form = TaskForm()
    if form.validate_on_submit():
        
        team = Task(name=form.name.data, note=form.note.data)
        pp.pprint(form.note.data)
        
        db.session.add(team)
        db.session.commit()
        
        tasks.append(team)
        redirect( url_for('tasks') )
    
    tasks = Task.query.all()

    return render_template('tasks.jinja2.html', tasks=tasks, form=form)
