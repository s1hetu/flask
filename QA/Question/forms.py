from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError

from QA.Question.models import Question
from QA.User.models import Tag


class AskQuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    tag_list = [(tag.id, tag.name) for tag in Tag.query.all()]
    tags = SelectMultipleField(choices=tag_list, coerce=int)
    post = SubmitField('Ask Question')

    def validate_question(self, question):
        if Question.query.filter_by(question=question.data).first():
            raise ValidationError("Question already exists. Please check it.")


class AnswerForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    post_answer = SubmitField('Answer')