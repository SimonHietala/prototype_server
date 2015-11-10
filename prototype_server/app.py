"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


class Worktask(db.Model):
    __tablename__ = 'worktasks_v2'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    starttime = db.Column(db.String(100), nullable=True)
    stoptime = db.Column(db.String(100), nullable=True)
    time = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    gps = db.Column(db.String(100), nullable=True)
    inmotion = db.Column(db.Boolean, nullable=True)
    edited = db.Column(db.Boolean, nullable=True)

    def __init__(self, task, location, starttime, gps, notes, inmotion, edited):
        self.task = task
        self.location = location
        self.starttime = starttime
        self.gps = gps
        self.notes = notes
        self.inmotion = inmotion
        self.edited = edited

    def to_json(wt):
        return jsonify(task=wt.task,
                   location=wt.location,
                   starttime=wt.starttime,
                   gps=wt.gps,
                   notes=wt.notes)

    def to_json_array(wts):
        for wt in wts:
            jsonify(task=wt.task,
                   location=wt.location,
                   starttime=wt.starttime,
                   gps=wt.gps,
                   notes=wt.notes)


@app.route('/get', methods=['GET'])
def get():
    #working
    #q = Worktask.query.all()
    q = Worktask.query.filter_by(task='work').first().location
    return q

@app.route('/post', methods=['POST'])
def post():
    
    content = request.get_json(force=True)
    
    worktask = Worktask(content['task'],
                        content['location'],                     
                        content['starttime'],
                        content['gps'],
                        content['notes'])
    db.session.add(worktask)
    db.session.commit()

    returnid = worktask.id
    return str(returnid)

@app.route('/worktasks/<id>', methods=['GET'])
def get_worktask(id):
    wt = Worktask.query.get(id)
    return Worktask.to_json(wt)

@app.route('/worktasks', methods=['GET'])
def get_worktasks():
    #wts = Worktask.query.order_by(Worktask.id.desc()).limit(10)
    wts = Worktask.query.all();
    list = []
    for wt in wts:
        item = {}
        item['id'] = wt.id
        item['task'] = wt.task
        item['location'] = wt.location
        item['starttime'] = wt.starttime                     
        item['stoptime'] = wt.stoptime
        item['time'] = wt.time
        item['notes'] = wt.notes
        item['gps'] = wt.gps
        item['inmotion'] = wt.inmotion
        item['edited'] = wt.edited
        list.append(item)
   
    return jsonify(array=list)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

