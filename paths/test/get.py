from flask import render_template, abort

from paths.test import test
from paths.test.utils import get_test_info, get_all_test_info
from errors import HTTPErrors

@test.route("/", methods=["GET"])
def get_dashboard():
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
    print(tests)
    return render_template('test/dashboard.html', tests=tests)


@test.route("/<int:test_id>", methods=["GET"])
def get_test(test_id):
    test_in_db = get_test_info(test_id)
    print(test_in_db)
    if not test_in_db:
        print("test with id {} not found".format(test_id))
        abort(HTTPErrors.NotFoundError.value, 'Test not found')
    return render_template("test/test-info.html")
