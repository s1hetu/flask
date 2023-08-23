from datetime import datetime

from QA import db

question_tags = db.Table('question_tag',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    asked_date = db.Column(db.DateTime(), default=datetime.now())
    up_vote = db.Column(db.Integer, nullable=False, default=0)
    down_vote = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='questions_asked', lazy=True)
    tags = db.relationship('Tag', secondary=question_tags, lazy=True, backref='questions')

    def __repr__(self):
        return f"<User - {self.user}, Question - {self.question}>"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref='answers', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='answers', lazy=True)
    answered_date = db.Column(db.DateTime(), default=datetime.now)
    up_vote = db.Column(db.Integer, default=0)
    down_vote = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Q: {self.question.question} A:{self.answer}"