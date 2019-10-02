from flask import render_template, abort, session, redirect, url_for

from app import db
from models import Problem, HasFinishedTest
from paths.authorization import login_required
from paths.test import test
from paths.test.utils import (
    get_test_info, get_all_test_info, get_problem_and_questions,
    get_problem_history
)
from errors import HTTPErrors


@test.route('/', methods=['GET'])
@login_required
def get_test_dashboard():
    """
        Get test Dashboard
        Renders: test/dashboard.html
        Parameters:
            - tests (Object[]) All the tests in db
                - tests.test_id (Integer) The id of the test
                - tests.name (String) The name of the test
                - tests.problem_count (Integer) The number of problems in test
                - tests.total_marks (Integer) The total marks received from the test
                - tests.difficulty (Integer) The difficulty of the test
    """
    tests_in_db = get_all_test_info()
    tests = [{}] * len(tests_in_db)
    for i, (test_id, name, problem_count, total_marks, difficulty) in enumerate(tests_in_db):
        test = {
            'test_id': test_id,
            'name': name,
            'problem_count': problem_count,
            'total_marks': total_marks,
            'difficulty': difficulty
        }
        tests[i] = test
    return render_template('test/dashboard.html', tests=tests)


@test.route('/<int:test_id>', methods=['GET'])
@login_required
def get_test(test_id):
    """
        Get test info
        Arguments:
            - test_id (Integer) The id of the test
        Renders: test/test_info.html
        Parameters:
            - test_id (Integer) The id of the test
            - name (String) The name of the test
            - problem_count (Integer) The number of problems in test
            - total_marks (Integer) The total marks received from the test
            - difficulty (Integer) The difficulty of the test
        Throws:
            404 Not Found: Test id was not found in the database
    """
    test_in_db = get_test_info(test_id)
    if not test_in_db:
        print('test with id {} not found'.format(test_id))
        abort(HTTPErrors.NotFoundError.value, 'Test not found')
    return render_template('test/test-info.html')


@test.route('/<int:test_id>/problem/<int:problem_id>', methods=['GET'])
@login_required
def get_test_problem(test_id, problem_id):
    """
        Get problem of test
        Arguments:
            - test_id (Integer) The id of the test
            - problem_id (Integer) The id of the problem
        Renders: test/problem.html
        Parameters:
            
    """
    student_id = session['user_id']
    problem, questions = get_problem_and_questions(test_id, problem_id)
    is_finished = not not (HasFinishedTest.query.filter_by(student_id=student_id, test_id=test_id).first())
    print(not not is_finished)
    if not problem or not questions:
        print('Problem with id {}, {} was not found'.format(test_id, problem_id))
        abort(HTTPErrors.NotFoundError.value)
    next_problem = Problem.query.filter_by(test_id=test_id, problem_id=(problem_id + 1)).first()
    prev_problem = Problem.query.filter_by(test_id=test_id, problem_id=(problem_id - 1)).first()
    problem_history = get_problem_history(student_id, test_id, problem_id)
    problem_obj = {
        'problem_id': problem.problem_id,
        'problem_statement': problem.problem_statement,
        'test_id': problem.test_id,
        'questions': [{}] * len(questions),
        'has_next': not not next_problem,
        'has_prev': not not prev_problem,
    }
    for i, question in enumerate(questions):
        problem_obj['questions'][i] = {
            'question_id': question.question_id,
            'question': question.question,
            'difficulty': question.difficulty.value,
            'marks': question.marks,
            'is_answered': problem_history[i].is_answered,
            'submitted_answer': problem_history[i].answer,
            'is_correct': ('correct' if problem_history[i].is_correct else 'incorrect') if is_finished else '',
            'answer': question.answer,
            'solution': question.solution,
        }

    return render_template('test/problem.html', problem=problem_obj, is_finished=is_finished)


@test.route("/<int:test_id>/end", methods=["GET"])
@login_required
def finish_test(test_id):
    """
        Finish Test
        Description: Finished a test and calculate results
        Renders: test/end.html
        Throws:
            - BadRequest error if test has already been finished
    """
    student_id = session['user_id']
    is_finished = HasFinishedTest.query.filter_by(test_id=test_id, student_id=student_id).first()
    if is_finished:
        print('Student with id {} has already finished test {}'.format(student_id, test_id))
        abort(HTTPErrors.BadRequest.value)
    test_finished = HasFinishedTest(test_id, student_id)
    db.session.add(test_finished)
    db.session.commit()
    return redirect(url_for('test.get_test_dashboard'))
