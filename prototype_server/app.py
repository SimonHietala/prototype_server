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

    def __init__(self, task, location, starttime, stoptime, time,  gps, notes, inmotion, edited):
        self.task = task
        self.location = location
        self.starttime = starttime
        self.stoptime = stoptime
        self.time = time
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


@app.route('/get', methods=['GET'])
def get():
    #working
    #q = Worktask.query.all()
    q = Worktask.query.filter_by(task='work').first().location
    return q   

@app.route('/worktasks/headers', methods=['GET'])
def get_headers():
    #query = db.session.query(Worktask.task.distinct())
    query = db.session.query(Worktask.task)
    headers = []
    for header in query:
        item = header[0]
        headers.append(item)

    myset = set(headers)
    mylist = list(myset)
    return jsonify(array=mylist)


@app.route('/worktasks/<id>', methods=['GET','PUT'])
def get_worktask(id):
    if request.method == 'GET':
        wt = Worktask.query.get(id)
        return Worktask.to_json(wt)
    
    elif request.method == 'PUT':
        content = request.get_json(force=True)
        wt = Worktask.query.filter_by(id=id).first()
        wt.task = content['task']
        wt.location = content['location']
        wt.starttime = content['starttime']
        wt.stoptime = content['stoptime']
        wt.time = content['time']
        wt.gps = content['gps']
        wt.notes = content['notes']
        wt.inmotion = content['inmotion']
        wt.edited = content['edited']
        db.session.commit() 

        return "Inserted into database."

@app.route('/worktasks', methods=['GET','POST'])
def get_worktasks():
    #wts = Worktask.query.order_by(Worktask.id.desc()).limit(10)
    if request.method == 'GET':
        wts = Worktask.query.order_by(Worktask.id.desc());
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
    
    elif request.method == 'POST':
        content = request.get_json(force=True)
    
        worktask = Worktask(content['task'],
                            content['location'],                     
                            content['starttime'],                  
                            content['stoptime'],
                            content['time'],
                            content['gps'],
                            content['notes'],
                            content['inmotion'],
                            content['edited'])
        db.session.add(worktask)
        db.session.commit()

        returnid = worktask.id
        return str(returnid)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

