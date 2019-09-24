from sqlalchemy import func, and_

from models import Test, Problem, Question


def get_test_info(test_id):
    test_info = Question.query.\
        join(Problem, Problem.problem_id == Question.problem_id and Problem.test_id == Question.test_id).\
        filter(Problem.test_id == test_id).group_by(Problem.test_id).\
        with_entities(
            func.sum(Question.marks).label("total_marks"),
            func.avg(Question.difficulty).label("difficulty"),
            Problem.test_id.label("test_id")).subquery()
    test_in_db = Problem.query.join(Test, Problem.test_id == Test.test_id).group_by(Test.test_id).\
        join(test_info, Test.test_id == test_info.c.test_id).\
        with_entities(
            Test.test_id,
            Test.name.label("test_name"),
            func.count(Test.test_id).label("problem_count"),
            test_info.c.total_marks.label("total_marks"),
            test_info.c.difficulty.label("difficulty")).first()
    
    return test_in_db


def get_all_test_info():
    test_info = Question.query.\
        join(Problem, and_(Problem.problem_id == Question.problem_id, Problem.test_id == Question.test_id)).\
        group_by(Problem.test_id).\
        with_entities(
            func.sum(Question.marks).label("total_marks"),
            func.avg(Question.difficulty).label("difficulty"),
            Problem.test_id.label("test_id")).subquery()
    tests_in_db = Problem.query.join(Test, Problem.test_id == Test.test_id).group_by(Test.test_id).\
        join(test_info, Test.test_id == test_info.c.test_id).\
        with_entities(
            Test.test_id,
            Test.name.label("test_name"),
            func.count(Test.test_id).label("problem_count"),
            test_info.c.total_marks.label("total_marks"),
            test_info.c.difficulty.label("difficulty")).all()
    return tests_in_db


def get_problem_and_questions(test_id, problem_id):
    questions = Question.query.filter_by(problem_id=problem_id, test_id=test_id).\
        order_by(Question.question_id).all()
    problem = Problem.query.filter_by(problem_id=problem_id, test_id=test_id).first()
    
    return problem, questions
