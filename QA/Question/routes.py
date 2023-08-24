from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.views import View
from flask_login import current_user, login_required

from .models import Question, Answer
from QA import db
from QA.User.models import User
from .forms import AskQuestionForm, AnswerForm
from ..User.models import Tag

question_blueprint = Blueprint("question", __name__)


@question_blueprint.route("/ask", methods=['GET', 'POST'])
@login_required
def ask_question():
    form = AskQuestionForm()
    if form.validate_on_submit():

        question = form.question.data
        tags = form.tags.data

        question = Question(question=question, user=current_user)
        db.session.add(question)
        for tag_id in tags:
            tag = Tag.query.filter_by(id=tag_id).first()
            question.tags.append(tag)
        db.session.commit()
        flash("Question added successfully.", 'success')
        return redirect('questions')
    return render_template('question/ask.html', form=form)


@question_blueprint.route('/questions', methods=['GET'])
@login_required
def view_questions():
    page = request.args.get('page', 1, type=int)

    return render_template('question/view_questions.html',
                           questions=Question.query.order_by(Question.asked_date.desc()).paginate(page=page,
                                                                                                  per_page=3))


@question_blueprint.route('/my_questions', methods=['GET', 'POST'])
def my_questions():
    # q1 = Question.query.filter_by(user=current_user).with_entities(Question.question, Question.asked_date,
    #                                                                Question.up_vote, Question.id, Question.user_id)

    """Problem with q1 is it will load data from one model only"""
    q2 = db.session.query(Question.id, Question.question, User.username, User.email).join(User,
                                                                                          User.id == Question.user_id).filter(
        Question.user == current_user)
    """This will only load columns given in query() and apply join on user_id from User, Question where user=current user."""

    # q3 = current_user.questions_asked
    """Problem with q3 is it will load all data from both tables"""
    return render_template('question/my_questions.html', questions=q2)


@question_blueprint.route('/update_question/<int:question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if current_user == question.user:
        if request.method == 'GET':
            form = AskQuestionForm(question=question.question)
        else:
            form = AskQuestionForm()
            if form.validate_on_submit():
                updated_question = form.question.data
                question.question = updated_question
                db.session.commit()
                flash("Question updated successfully.", 'success')
                return redirect(url_for('question.my_questions'))
        return render_template('question/ask.html', form=form)
    else:
        print("You cant update this question as you are not th creator of it.")
        return redirect(url_for('question.my_questions'))


class MyAnswers(View):
    methods = ['GET']

    def dispatch_request(self):
        ans = db.session.query(Answer.answer, Question.question, Answer.answered_date).join(Question, Question.id == Answer.question_id).filter(Question.user==current_user)
        # ans2 = current_user.answers
        return render_template('question/my_answers.html', answers=ans)


question_blueprint.add_url_rule('/my_answers', view_func=MyAnswers.as_view('my_answers'))


class PostAnswer(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, question_id):
        form = AnswerForm()
        if form.validate_on_submit():
            answer = Answer(answer=form.answer.data, user=current_user,
                            question=Question.query.filter_by(id=question_id).first())
            db.session.add(answer)
            db.session.commit()
            flash("Answer added successfully.", 'success')
            return redirect(url_for('question.update_question', question_id=question_id))
        return render_template('question/post_answer.html', form=form)


question_blueprint.add_url_rule("/answer/<int:question_id>", view_func=PostAnswer.as_view('answer'))
