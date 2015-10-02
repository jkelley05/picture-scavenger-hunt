from picture_hunt import config, helpers
from picture_hunt import app, db, lm
from picture_hunt.models import Media, Team, Task
from picture_hunt.forms import TeamForm, TaskForm, UploadForm, SearchForm

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify

from flask.ext.login import login_user, logout_user, current_user, login_required

import pprint as pp
from datetime import datetime

@app.route('/')
def index():
    
    media = []
    media_query = Media.query
    args = dict(request.args)
    
    form = SearchForm(formdata=request.args)
    teams = Team.query.all()
    form.team.choices = [(-1, 'All')] + [ (i.id, i.name) for i in teams ]
  
    tasks = Task.query.all()
    form.task.choices = [(-1, 'All')] + [ (i.id, i.name) for i in tasks ]
    

    
    if args.get('team') and int(args.get('team')[0]) == -1:
        del args['team']

    if args.get('task') and int(args.get('task')[0]) == -1:
        del args['task']
    
    print(args) 
    if 'team' in args and 'task' in args: 
        print("Both team and task")
        team_id = request.args.get('team')
        task_id = request.args.get('task')

        media = Media.query.filter(Media.team_id == team_id, Media.task_id == task_id)
    
    elif 'team' in args:
        team_id = request.args.get('team')
        media_query = Media.query.filter(Media.team_id == team_id)

    elif 'task' in args:
        task_id = request.args.get('task')
        media_query = Media.query.filter(Media.task_id == task_id)
    
    media = media_query.order_by(Media.created.desc()).all()

    return render_template('index.jinja2.html', media=media, form=form) 


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    media = Media() 
    form = UploadForm()

    teams = Team.query.all()
    form.team.choices = [(-1, 'Choose One')] + [ (i.id, i.name) for i in teams ]
    
    tasks = Task.query.all()
    form.task.choices = [(-1, 'Choose One')] + [ (i.id, i.name + ": " + i.note) for i in tasks ]


    if form.validate_on_submit():
        team = form.team.data
        task = form.task.data
        
        print(form.media.data) 
        if form.media.data:
            print("Upload the file")
            print( form.media.name )

            file_ = request.files[form.media.name]
            if file_.stream: 
                path = helpers.upload_to_s3(file_) 
                media.uri = path
                 
                media.team = Team.query.get(team) 
                media.task = Task.query.get(task)
                media.created = datetime.now()
                db.session.add(media)
                db.session.commit()
                
                flash("You have uploaded " + media.uri) 
                return redirect( url_for('index') )
            else:
                flash("You must choose a file" + media.uri) 
                print("flash error for no file selected")
    else:
        print("Did not validate")

        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(fieldName, err)

    return render_template('upload.jinja2.html', form=form)



@app.route('/checklist')
def list_checklist():
    teams = Team.query.all()
    
    return render_template('list_checklist.jinja2.html', teams=teams)


@app.route('/checklist/<team>')
def checklist(team):
    print("In checklist")    
    team = Team.query.get_or_404(team) 
    print("Got team " + team.name)    
    checklist = []

    sql = """
          select 
            tk.id as task_id,
            tk.name as task_name,
            tk.note as task_note,
            m.id as media
          from 
            task tk
            left outer join media m on m.task_id = tk.id and m.team_id = {}
          order by
            task_id
          """.format(team.id)
    print("AFter sql var  " )    
    checklist = db.engine.execute(sql)#, team.id)
    print("Got results  " )    

    return render_template('checklist.jinja2.html', team=team, checklist=checklist)

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    
    team = None 
    form = TeamForm()
    if form.validate_on_submit():
        
        team = Team( name=form.name.data, note=form.note.data )
        
        db.session.add(team)
        db.session.commit()
        
        flash("You have added team {}".format(team.name))
        return redirect( url_for('teams') )
    
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
        
        flash("You have added task {}".format(task.name))
        return redirect( url_for('tasks') )
    
    tasks = Task.query.all()

    return render_template('tasks.jinja2.html', tasks=tasks, form=form)


@app.route('/task/<id_>/delete', methods=['POST',])
def task_delete(id_):

    task = Task.query.get_or_404(id_) 
    
    for i in task.submissions:
        db.session.delete(i)
    db.session.delete(task)
    db.session.commit()
    
    flash("You have delete task {} and all realated submissions".format(task.name))
    return redirect( url_for('tasks') )


@app.route('/team/<id_>/delete', methods=['POST',])
def team_delete(id_):

    team = Team.query.get_or_404(id_) 
    
    for i in team.submissions:
        db.session.delete(i)
    db.session.delete(team)
    db.session.commit()
    
    flash("You have delete team {} and all its submissions".format(team.name))
    return redirect( url_for('teams') )


@app.route('/media/<id_>', methods=['GET',])
def media(id_):
    
    media = Media.query.get_or_404(id_) 

    return render_template('media.jinja2.html', media=media)


@app.route('/meida/<id_>/delete', methods=['POST',])
def media_delete(id_):

    media = Media.query.get_or_404(id_) 
    
    db.session.delete(media)
    db.session.commit()
    
    flash("Deleted submission with " + media.uri) 
    return redirect( url_for('index') )

