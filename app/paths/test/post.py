from flask import request, abort, session
from app import db

from app.models import TestHistory, Problem, Question
from app.paths.authorization import login_required
from app.paths.test import test
from app.paths.test.utils import get_question_asnwer, checkAnswer
from app.errors import HTTPErrors


@test.route('/<int:test_id>/start', methods=['POST'])
@login_required
def start_test(test_id):
    """
        Start test
        Description: Start a test for user
        Returns: The id of the first problem
        Throws:
            - BadRequest error if test has been started before
    """
    student_id = session['user_id']
    has_taken_test = TestHistory.query.filter_by(student_id=student_id, test_id=test_id).all()
    if len(has_taken_test) != 0:
        print('User {} has already started test {}'.format(student_id, test_id))
    else:
        test_problems = Problem.query.filter_by(test_id=test_id).all()
        for problem in test_problems:
            questions = Question.query.filter_by(test_id=test_id, problem_id=problem.problem_id).all()
            for question in questions:
                new_test_history = TestHistory(student_id, test_id, problem.problem_id, question.question_id, None, None, False)
                db.session.add(new_test_history)
        db.session.commit()
    start = Problem.query.filter_by(test_id=test_id).order_by(Problem.problem_id).first()
    return {'start': start.problem_id}


@test.route('/<int:test_id>/problem/<int:problem_id>', methods=['POST'])
@login_required
def post_answer(test_id, problem_id):
    """
        Post test answer
        Returns: 200 OK
        Throws: 
            - BadRequest error if answer has already been sumbitted
    """
    submitted_answer = request.form['answer']
    question_id = request.form['question_id']
    student_id = session['user_id']
    question_history = TestHistory.query.\
        filter_by(student_id=student_id, test_id=test_id, problem_id=problem_id, question_id=question_id).first()
    if question_history.is_answered:
        print('Student {} tried to re-submit answer'.format(student_id))
        abort(HTTPErrors.BadRequest.value)
    answer, solution = get_question_asnwer(test_id, problem_id, question_id)
    is_equal = checkAnswer(answer, submitted_answer)
    TestHistory.query.\
        filter_by(student_id=student_id, test_id=test_id, problem_id=problem_id, question_id=question_id).\
        update({'answer': submitted_answer, 'is_correct': is_equal, 'is_answered': True})
    db.session.commit()
    return {}, 200
