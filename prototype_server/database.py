from flask_sqlalchemy import SQLAlchemy

class worktask(db.Model):
    __tablename__ = 'worktasks'
    id = db.Column('id', db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    time = db.Column(db.String(100))

    def __init__(self, task, time):
        self.task = task
        self.time = time
