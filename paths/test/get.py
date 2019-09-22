from flask import render_template
from sqlalchemy import func

from paths.test import test
from models import Test, Problem, Question


@test.route("/", methods=["GET"])
def get_dashboard():
    test_info = Question.query.join(Problem, Problem.problem_id == Question.problem_id)\
        .group_by(Problem.test_id).\
        with_entities(
            func.sum(Question.marks).label("total_marks"),
            func.avg(Question.difficulty).label("difficulty"),
            Problem.test_id.label("test_id")).subquery()
    testsdb = Problem.query.join(Test, Problem.test_id == Test.test_id).group_by(Test.test_id).\
        join(test_info, Test.test_id == test_info.c.test_id).\
        with_entities(
            Test.test_id,
            Test.name.label("test_name"),
            func.count(Test.test_id).label("problem_count"),
            test_info.c.total_marks.label("total_marks"),
            test_info.c.difficulty.label("difficulty")).all()
    
    tests = [{}] * len(testsdb)
    for i, (test_id, name, problem_count, total_marks, difficulty) in enumerate(testsdb):
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
