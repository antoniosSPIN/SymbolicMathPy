from flask import render_template, abort

from paths.test import test
from paths.test.utils import get_test_info, get_all_test_info, get_problem_and_questions
from errors import HTTPErrors


@test.route("/", methods=["GET"])
def get_dashboard():
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
            "test_id": test_id,
            "name": name,
            "problem_count": problem_count,
            "total_marks": total_marks,
            "difficulty": difficulty
        }
        tests[i] = test
    return render_template('test/dashboard.html', tests=tests)


@test.route("/<int:test_id>", methods=["GET"])
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
        print("test with id {} not found".format(test_id))
        abort(HTTPErrors.NotFoundError.value, 'Test not found')
    return render_template("test/test-info.html")


@test.route("/<int:test_id>/problem/<int:problem_id>", methods=["GET"])
def get_test_problem(test_id, problem_id):
    """
        Get problem of test
        Arguments:
            - test_id (Integer) The id of the test
            - problem_id (Integer) The id of the problem
        Renders: test/problem.html
        Parameters:
            
    """
    problem, questions = get_problem_and_questions(test_id, problem_id)
    problem_obj = {
        "problem_id": problem.problem_id,
        "problem_statement": problem.problem_statement,
        "test_id": problem.test_id,
        "questions": [{}] * len(questions)
    }
    for i, question in enumerate(questions):
        problem_obj['questions'][i] = {
            "question_id": question.question_id,
            "question": question.question,
            "difficulty": question.difficulty.value,
            "marks": question.marks
        }

    return render_template("test/problem.html", problem=problem_obj, answered=False)
