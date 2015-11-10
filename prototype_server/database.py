from flask import jsonify
'''
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
    inMotion = db.Column(db.Boolean, nullable=True)
    edited = db.Column(db.Boolean, nullable=True)

    def __init__(self, task, location, starttime, gps, notes):
        self.task = task
        self.location = location
        self.starttime = starttime
        self.gps = gps
        self.notes = notes

    def to_json(wt):
        return jsonify(task=wt.task,
                   location=wt.location,
                   starttime=wt.starttime,
                   gps=wt.gps,
                   notes=wt.notes)
    '''
