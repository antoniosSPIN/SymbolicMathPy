from flask import request, abort
from app import db

from models import TestHistory, Problem, Question
from paths.test import test
from paths.test.utils import get_question_asnwer, checkAnswer


@test.route("/<int:test_id>/problem/<int:problem_id>", methods=["POST"])
def post_answer(test_id, problem_id):
    submitted_answer = request.form['answer']
    answer, solution = get_question_asnwer(test_id, problem_id, request.form['question_id'])
    is_equal = checkAnswer(answer, submitted_answer)
    return {
        'answer': answer,
        'solution': solution,
        'isCorrect': is_equal
    }


@test.route("/<int:test_id>/start", methods=["POST"])
def start_test(test_id):
    student_id = 2
    has_taken_test = TestHistory.query.filter_by(student_id=student_id, test_id=test_id).all()
    if len(has_taken_test) != 0:
        print('User has already taken this test')
        abort(400)
    test_problems = Problem.query.filter_by(test_id=test_id).all()
    for problem in test_problems:
        questions = Question.query.filter_by(test_id=test_id, problem_id=problem.problem_id).all()
        for question in questions:
            new_test_history = TestHistory(student_id, test_id, problem.problem_id, question.question_id, None, None, False)
            db.session.add(new_test_history)
    db.session.commit()
    start = Problem.query.filter_by(test_id=test_id).order_by(Problem.problem_id).first()
    return {'start': start.problem_id}
