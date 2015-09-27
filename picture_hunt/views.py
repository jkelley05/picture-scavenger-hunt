from picture_hunt import config
from picture_hunt import app, db, lm
from picture_hunt.models import Media

from flask import render_template, flash, redirect, session, url_for, request, g, Response, jsonify

from flask.ext.login import login_user, logout_user, current_user, login_required


@app.route('/')
def index():
    
    media = Media.query.all()

    # Search by team or event or missing info

    return render_template('index.jinja2.html', media=media)
