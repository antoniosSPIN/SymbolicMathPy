from flask import request

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
