from picture_hunt import config, helpers
from picture_hunt import app, db, lm
from picture_hunt.models import Media, Team, Task
from picture_hunt.forms import TeamForm, TaskForm, UploadForm, SearchForm

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify

from flask.ext.login import login_user, logout_user, current_user, login_required

import pprint as pp

@app.route('/')
def index():
    
    media = []
    args = dict(request.args)
    
    form = SearchForm(formdata=request.args)
    teams = Team.query.all()
    form.team.choices = [(-1, 'All')] + [ (i.id, i.name) for i in teams ]
  
    tasks = Task.query.all()
    form.task.choices = [(-1, 'All')] + [ (i.id, i.name) for i in tasks ]
    
    if args.get('team') and int(args.get('team')[0]) == -1:
        del args['team']

    if args.get('team') and int(args.get('task')[0]) == -1:
        del args['task']
    
    print(args) 
    if 'team' in args and 'task' in args: 
        print("Both team and task")
        team_id = request.args.get('team')
        task_id = request.args.get('task')

        media = Media.query.filter(Media.team_id == team_id, Media.task_id == task_id).all() #, Task.id == int(task_id)).all()
    
    elif 'team' in args:
        team_id = request.args.get('team')
        team = Team.query.filter(Team.id == team_id).first()

        if team is not None:
            media = team.submissions
        else:
            print("Need to flash an error message")
            
    elif 'task' in args:
        task_id = request.args.get('task')
        task = Task.query.get(task_id)
        if task is not None:
            media = task.submissions
        else:
            print("Need to flash an error message")
    else:
        print("No team or task")
        media = Media.query.all()


    # Search by team or event or missing info

    return render_template('index.jinja2.html', media=media, form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    media = Media() 
    form = UploadForm()

    teams = Team.query.all()
    form.team.choices = [ (i.id, i.name) for i in teams ]
    
    tasks = Task.query.all()
    form.task.choices = [ (i.id, i.name) for i in tasks ]


    if form.validate_on_submit():
        team = form.team.data
        task = form.task.data
        
        print(form.media.data) 
        if form.media.data:
            print("Upload the file")
            print( form.media.name )

            file_ = request.files[form.media.name]
            path = helpers.upload_to_s3(file_) 
            media.uri = path
             
            media.team = Team.query.get(team) 
            media.task = Task.query.get(task)
            db.session.add(media)
            db.session.commit()
            
            return redirect( url_for('index') )
        else:
            print("flash error for no file selected")
    else:
        print("Did not validate")

        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(fieldName, err)

    return render_template('upload.jinja2.html', form=form)



@app.route('/teams', methods=['GET', 'POST'])
def teams():
    
    team = None 
    form = TeamForm()
    if form.validate_on_submit():
        
        team = Team( name=form.name.data, note=form.note.data )
        
        db.session.add(team)
        db.session.commit()
        
        redirect( url_for('teams') )
    
    teams = Team.query.all()
    
    return render_template('teams.jinja2.html', teams=teams, form=form)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    
    task = None 
    form = TaskForm()
    if form.validate_on_submit():
        
        task = Task(name=form.name.data, note=form.note.data)
        
        db.session.add(task)
        db.session.commit()
        
        redirect( url_for('tasks') )
    
    tasks = Task.query.all()

    return render_template('tasks.jinja2.html', tasks=tasks, form=form)


@app.route('/task/<id_>/delete', methods=['POST',])
def task_delete(id_):

    task = Task.query.get_or_404(id_) 
    
    for i in task.submissions:
        db.session.delete(i)
    db.session.delete(task)
    db.session.commit()
    
    print("Deleted task " + task.name) 
    return redirect( url_for('tasks') )


@app.route('/team/<id_>/delete', methods=['POST',])
def team_delete(id_):

    team = Team.query.get_or_404(id_) 
    
    for i in team.submissions:
        db.session.delete(i)
    db.session.delete(team)
    db.session.commit()
    
    print("Deleted team " + team.name) 
    return redirect( url_for('teams') )


@app.route('/media/<id_>', methods=['GET',])
def media(id_):
    
    media = Media.query.get_or_404(id_) 

    return render_template('media.jinja2.html', media=media)




