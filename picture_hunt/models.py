from picture_hunt import db, app

import six

ROLE_USER = 2
ROLE_ADMIN = 1

class User(db.Model):
    """ Used by flask login """

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(1200))
    name = db.Column(db.String(120))

    role = db.Column(db.SmallInteger, default = ROLE_USER)


    def is_authenticated(self):
        return True 

    def is_active(self):
        return True 

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)



class Media(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    
    team_id = db.Column(db.Integer, db.ForeignKey('team.id')) 
    task_id = db.Column(db.Integer, db.ForeignKey('task.id')) 
    
    type_ = db.Column(db.String(128))
    
    uri = db.Column(db.String(1028)) # url or path  
    
    
class Team(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(256), index = True, unique = True)
    note = db.Column(db.String(1024))

    submissions = db.relationship('Media', backref='team')


    
class Task(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(256), index = True, unique = True)
    note = db.Column(db.String(1024))
    
    submissions = db.relationship('Media', backref='task')
