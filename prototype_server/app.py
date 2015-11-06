"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

class Worktasks(db.Model):
    __tablename__ = 'worktasks'
    id = db.Column('id', db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    location = db.Column(db.String(100))

    def __init__(self, task, location):
        self.task = task
        self.location = location

@app.route('/get', methods=['GET'])
def get():
    q = Worktasks.query.filter()
    return q

@app.route('/post', methods=['POST'])
def post():
    content = request.get_json(force=True)
    
    worktask = Worktasks(content['task'],content['location'])
    db.session.add(worktask)
    db.session.commit()

    return worktask.id
  
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
